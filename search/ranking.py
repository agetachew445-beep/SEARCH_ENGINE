"""
Ranking module.

Implements two IR ranking algorithms:
  1. Vector Space Model  — cosine similarity with TF-IDF vectors
  2. Okapi BM25          — probabilistic ranking with length normalisation
"""

import math
from collections import defaultdict
from typing import Dict, List, Tuple

from .models import Document, IndexEntry
from .preprocessing import TextPreprocessor
from .indexing import InvertedIndexBuilder


class RankingEngine:

    def __init__(self, ranking_model: str = 'cosine'):
        self.ranking_model = ranking_model
        self.preprocessor  = TextPreprocessor()
        self.indexer       = InvertedIndexBuilder()
        # BM25 hyper-parameters (standard defaults)
        self.k1 = 1.5
        self.b  = 0.75

    # ─────────────────────────────────────────
    # PUBLIC ENTRY POINT
    # ─────────────────────────────────────────
    def search(self, query: str, top_k: int = 50) -> List[Tuple[int, float]]:
        """
        Returns a list of (doc_id, score) sorted by score descending.
        """
        if self.ranking_model == 'cosine':
            return self.cosine_similarity_search(query, top_k)
        elif self.ranking_model == 'bm25':
            return self.bm25_search(query, top_k)
        else:
            raise ValueError(f"Unknown ranking model: {self.ranking_model!r}")

    # ─────────────────────────────────────────
    # 1. VECTOR SPACE MODEL — COSINE SIMILARITY
    # ─────────────────────────────────────────
    def cosine_similarity_search(self, query: str,
                                 top_k: int = 50) -> List[Tuple[int, float]]:
        """
        TF-IDF weighted cosine similarity.

        score(q, d) = (q⃗ · d⃗) / (‖q⃗‖ · ‖d⃗‖)
        """
        query_terms = self.preprocessor.preprocess(query, apply_stemming=True)
        if not query_terms:
            return []

        # ── build query TF-IDF vector ──
        term_counts: Dict[str, int] = defaultdict(int)
        for t in query_terms:
            term_counts[t] += 1

        query_vec: Dict[str, float] = {}
        for term, tf in term_counts.items():
            try:
                entry = IndexEntry.objects.get(term=term)
                query_vec[term] = tf * entry.idf
            except IndexEntry.DoesNotExist:
                pass

        if not query_vec:
            return []

        q_mag = math.sqrt(sum(w * w for w in query_vec.values()))

        # ── accumulate dot-products and doc magnitudes ──
        dot:   Dict[int, float] = defaultdict(float)
        d_sq:  Dict[int, float] = defaultdict(float)

        for term, q_w in query_vec.items():
            try:
                entry    = IndexEntry.objects.get(term=term)
                idf      = entry.idf
                for p in entry.get_postings():
                    did   = p['doc_id']
                    d_w   = p['term_freq'] * idf
                    dot[did]  += q_w * d_w
                    d_sq[did] += d_w * d_w
            except IndexEntry.DoesNotExist:
                pass

        # ── cosine scores ──
        results = []
        for did, dp in dot.items():
            d_mag = math.sqrt(d_sq[did])
            if d_mag > 0 and q_mag > 0:
                results.append((did, dp / (q_mag * d_mag)))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    # ─────────────────────────────────────────
    # 2. OKAPI BM25
    # ─────────────────────────────────────────
    def bm25_search(self, query: str,
                    top_k: int = 50) -> List[Tuple[int, float]]:
        """
        BM25 score:

        score(q, d) = Σ  IDF(t) ·  tf(t,d)·(k1+1)
                              ─────────────────────────────────────────
                              tf(t,d) + k1·(1 − b + b·|d|/avgdl)
        """
        query_terms = self.preprocessor.preprocess(query, apply_stemming=True)
        if not query_terms:
            return []

        stats      = self.indexer.get_collection_stats()
        N          = stats['total_documents']
        avgdl      = stats['avg_doc_length'] or 1.0

        if N == 0:
            return []

        # cache doc lengths to avoid repeated DB hits
        doc_lengths: Dict[int, int] = {}

        scores: Dict[int, float] = defaultdict(float)

        for term in set(query_terms):
            try:
                entry = IndexEntry.objects.get(term=term)
            except IndexEntry.DoesNotExist:
                continue

            df  = entry.document_frequency
            idf = math.log((N - df + 0.5) / (df + 0.5) + 1)

            for p in entry.get_postings():
                did = p['doc_id']
                tf  = p['term_freq']

                if did not in doc_lengths:
                    try:
                        doc = Document.objects.get(id=did)
                        doc_lengths[did] = len(doc.processed_text.split())
                    except Document.DoesNotExist:
                        doc_lengths[did] = 1

                dl  = doc_lengths[did]
                num = tf * (self.k1 + 1)
                den = tf + self.k1 * (1 - self.b + self.b * dl / avgdl)
                scores[did] += idf * (num / den)

        results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return results[:top_k]
