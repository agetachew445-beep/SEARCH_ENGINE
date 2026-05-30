"""
Indexing module.

Offline phase:
  1. Tokenise + preprocess every document
  2. Build in-memory inverted index  { term → { doc_id → [positions] } }
  3. Compute TF-IDF (IDF stored per term; TF stored per posting)
  4. Persist to SQLite via IndexEntry model
"""

import math
from collections import defaultdict
from typing import Dict, List

from .models import Document, IndexEntry
from .preprocessing import TextPreprocessor, ExtractiveSummarizer, ConceptExtractor


class InvertedIndexBuilder:

    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.summarizer   = ExtractiveSummarizer()
        self.concept_ext  = ConceptExtractor()

    # ─────────────────────────────────────────
    # BUILD
    # ─────────────────────────────────────────
    def build_index(self, documents=None) -> int:
        """
        Index *documents* (QuerySet).  If None, index all un-indexed docs.
        Returns the number of unique terms added.
        """
        if documents is None:
            documents = Document.objects.filter(is_indexed=False)

        doc_list = list(documents)          # evaluate once
        if not doc_list:
            print("No documents to index.")
            return 0

        # If we are re-indexing everything, wipe the old index first
        if Document.objects.count() == len(doc_list):
            IndexEntry.objects.all().delete()

        # ── pass 1: build in-memory index ──
        # index_data[term][doc_id] = [pos0, pos1, …]
        index_data: Dict[str, Dict[int, List[int]]] = defaultdict(
            lambda: defaultdict(list)
        )

        print(f"Indexing {len(doc_list)} documents…")
        for doc in doc_list:
            tokens = self.preprocessor.preprocess(doc.raw_text, apply_stemming=True)
            doc.processed_text = ' '.join(tokens)

            # Generate summary and concepts
            if not doc.summary:
                doc.summary = self.summarizer.summarize(
                    doc.raw_text, num_sentences=3, language=doc.language
                )
            concepts = self.concept_ext.extract_concepts(doc.raw_text, top_k=8)
            doc.set_concepts_list(concepts)

            for pos, term in enumerate(tokens):
                index_data[term][doc.id].append(pos)

            doc.is_indexed = True
            doc.save(update_fields=['processed_text', 'is_indexed',
                                    'summary', 'concepts', 'updated_at'])

        # ── pass 2: compute IDF + persist ──
        total_docs = Document.objects.filter(is_indexed=True).count()
        print(f"Saving {len(index_data)} terms to SQLite…")

        for term, doc_postings in index_data.items():
            df  = len(doc_postings)
            idf = math.log((total_docs + 1) / (df + 1)) + 1   # smoothed IDF

            postings = [
                {
                    'doc_id':    doc_id,
                    'term_freq': len(positions),
                    'positions': positions[:20],   # keep first 20 positions
                }
                for doc_id, positions in doc_postings.items()
            ]

            entry, _ = IndexEntry.objects.get_or_create(term=term)
            entry.document_frequency = df
            entry.idf                = idf
            entry.set_postings(postings)
            entry.save()

        print(f"Done — {len(index_data)} unique terms indexed.")
        return len(index_data)

    # ─────────────────────────────────────────
    # QUERY HELPERS
    # ─────────────────────────────────────────
    def get_term_postings(self, term: str) -> List[Dict]:
        """Return postings list for a (pre-processed) term."""
        processed = self.preprocessor.preprocess(term, apply_stemming=True)
        if not processed:
            return []
        try:
            return IndexEntry.objects.get(term=processed[0]).get_postings()
        except IndexEntry.DoesNotExist:
            return []

    def get_document_vector(self, doc_id: int) -> Dict[str, float]:
        """Return TF-IDF vector {term: weight} for a document."""
        vector: Dict[str, float] = {}
        for entry in IndexEntry.objects.all():
            for posting in entry.get_postings():
                if posting['doc_id'] == doc_id:
                    vector[entry.term] = posting['term_freq'] * entry.idf
                    break
        return vector

    def get_collection_stats(self) -> Dict:
        """Return basic corpus statistics."""
        docs = Document.objects.filter(is_indexed=True)
        total_docs  = docs.count()
        total_terms = IndexEntry.objects.count()

        avg_doc_length = 0.0
        if total_docs:
            total_tokens   = sum(len(d.processed_text.split()) for d in docs)
            avg_doc_length = total_tokens / total_docs

        return {
            'total_documents': total_docs,
            'total_terms':     total_terms,
            'avg_doc_length':  avg_doc_length,
        }
