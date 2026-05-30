"""
AI / Machine Learning Features
================================
All implemented using only scikit-learn + numpy (already installed).
No external API or heavy model download required.

Features:
  1. TF-IDF based document summarisation
  2. Concept / topic extraction
  3. Related documents (cosine similarity between doc vectors)
  4. Query expansion (find related terms from index)
  5. Document clustering (K-Means on TF-IDF vectors)
  6. Readability scoring
  7. Language-aware keyword highlighting
"""

import math
import re
from collections import Counter
from typing import List, Dict, Tuple, Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

from .preprocessing import TextPreprocessor, ExtractiveSummarizer, ConceptExtractor
from .models import Document, IndexEntry


# ─────────────────────────────────────────────────────────────────────────
# 1. DOCUMENT SUMMARISER
# ─────────────────────────────────────────────────────────────────────────
class DocumentSummarizer:
    """
    Generates extractive summaries using TF-IDF sentence scoring.
    Works for all languages including Amharic, Tigrinya, Afan Oromo.
    """

    def __init__(self):
        self._summarizer = ExtractiveSummarizer()

    def summarize(self, text: str, num_sentences: int = 3,
                  language: str = 'english') -> str:
        """Return an extractive summary."""
        return self._summarizer.summarize(text, num_sentences, language)

    def summarize_document(self, doc_id: int,
                           num_sentences: int = 3) -> Optional[str]:
        """Summarize a document by ID."""
        try:
            doc = Document.objects.get(id=doc_id)
            return self.summarize(doc.raw_text, num_sentences, doc.language)
        except Document.DoesNotExist:
            return None


# ─────────────────────────────────────────────────────────────────────────
# 2. CONCEPT RETRIEVAL
# ─────────────────────────────────────────────────────────────────────────
class ConceptRetriever:
    """
    Extracts key concepts from documents and enables concept-based search.
    """

    def __init__(self):
        self._extractor = ConceptExtractor()

    def get_concepts(self, text: str, top_k: int = 8) -> List[str]:
        return self._extractor.extract_concepts(text, top_k)

    def get_document_concepts(self, doc_id: int,
                              top_k: int = 8) -> List[str]:
        try:
            doc = Document.objects.get(id=doc_id)
            return self.get_concepts(doc.raw_text, top_k)
        except Document.DoesNotExist:
            return []

    def search_by_concept(self, concept: str,
                          top_k: int = 10) -> List[Tuple[int, float]]:
        """
        Find documents most related to a concept using TF-IDF.
        Returns list of (doc_id, score).
        """
        docs = list(Document.objects.filter(is_indexed=True))
        if not docs:
            return []

        preprocessor = TextPreprocessor()
        concept_tokens = preprocessor.preprocess(concept, apply_stemming=True)
        if not concept_tokens:
            return []

        scores = []
        for doc in docs:
            doc_tokens = preprocessor.preprocess(doc.raw_text, apply_stemming=True)
            if not doc_tokens:
                continue
            # Jaccard similarity between concept tokens and doc tokens
            concept_set = set(concept_tokens)
            doc_set     = set(doc_tokens)
            intersection = concept_set & doc_set
            union        = concept_set | doc_set
            if union:
                score = len(intersection) / len(union)
                if score > 0:
                    scores.append((doc.id, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


# ─────────────────────────────────────────────────────────────────────────
# 3. RELATED DOCUMENTS
# ─────────────────────────────────────────────────────────────────────────
class RelatedDocumentFinder:
    """
    Finds documents similar to a given document using TF-IDF cosine similarity.
    """

    def find_related(self, doc_id: int,
                     top_k: int = 5) -> List[Tuple[int, float, str]]:
        """
        Returns list of (doc_id, similarity_score, title) for related docs.
        """
        docs = list(Document.objects.filter(is_indexed=True))
        if len(docs) < 2:
            return []

        # Find target document
        target = next((d for d in docs if d.id == doc_id), None)
        if not target:
            return []

        preprocessor = TextPreprocessor()

        # Build processed texts
        texts    = [preprocessor.preprocess_to_string(d.raw_text) for d in docs]
        doc_ids  = [d.id for d in docs]
        titles   = [d.title for d in docs]

        if not any(texts):
            return []

        try:
            vectorizer = TfidfVectorizer(
                max_features=500,
                ngram_range=(1, 2),
                min_df=1,
            )
            tfidf_matrix = vectorizer.fit_transform(texts)

            # Find index of target document
            target_idx = doc_ids.index(doc_id)
            target_vec = tfidf_matrix[target_idx]

            # Compute cosine similarity with all docs
            sims = cosine_similarity(target_vec, tfidf_matrix).flatten()

            # Get top-k (excluding the document itself)
            results = []
            for i, sim in enumerate(sims):
                if doc_ids[i] != doc_id and sim > 0:
                    results.append((doc_ids[i], round(float(sim), 4), titles[i]))

            results.sort(key=lambda x: x[1], reverse=True)
            return results[:top_k]

        except Exception:
            return []


# ─────────────────────────────────────────────────────────────────────────
# 4. QUERY EXPANSION
# ─────────────────────────────────────────────────────────────────────────
class QueryExpander:
    """
    Expands a query with related terms found in the index.
    Uses co-occurrence in the inverted index.
    """

    def expand_query(self, query: str,
                     max_expansions: int = 3) -> List[str]:
        """
        Return a list of expansion terms for the query.
        """
        preprocessor = TextPreprocessor()
        query_terms  = preprocessor.preprocess(query, apply_stemming=True)

        if not query_terms:
            return []

        # Find documents containing query terms
        related_doc_ids = set()
        for term in query_terms:
            try:
                entry = IndexEntry.objects.get(term=term)
                for posting in entry.get_postings():
                    related_doc_ids.add(posting['doc_id'])
            except IndexEntry.DoesNotExist:
                pass

        if not related_doc_ids:
            return []

        # Collect all terms from those documents
        term_freq: Counter = Counter()
        for doc_id in list(related_doc_ids)[:10]:  # limit to 10 docs
            try:
                doc    = Document.objects.get(id=doc_id)
                tokens = preprocessor.preprocess(doc.raw_text, apply_stemming=True)
                term_freq.update(tokens)
            except Document.DoesNotExist:
                pass

        # Remove original query terms
        for t in query_terms:
            del term_freq[t]

        # Return top expansion terms
        expansions = [term for term, _ in term_freq.most_common(max_expansions * 3)
                      if len(term) > 2]
        return expansions[:max_expansions]


# ─────────────────────────────────────────────────────────────────────────
# 5. DOCUMENT CLUSTERING
# ─────────────────────────────────────────────────────────────────────────
class DocumentClusterer:
    """
    Groups documents into clusters using K-Means on TF-IDF vectors.
    Useful for topic discovery.
    """

    def cluster(self, n_clusters: int = 3) -> Dict[int, List[Dict]]:
        """
        Cluster all indexed documents.
        Returns dict: {cluster_id: [{'id', 'title', 'language'}]}
        """
        docs = list(Document.objects.filter(is_indexed=True))
        if len(docs) < n_clusters:
            return {0: [{'id': d.id, 'title': d.title,
                         'language': d.language} for d in docs]}

        preprocessor = TextPreprocessor()
        texts   = [preprocessor.preprocess_to_string(d.raw_text) for d in docs]
        doc_ids = [d.id for d in docs]

        try:
            vectorizer   = TfidfVectorizer(max_features=200, min_df=1)
            tfidf_matrix = vectorizer.fit_transform(texts)

            km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            labels = km.fit_predict(tfidf_matrix)

            clusters: Dict[int, List[Dict]] = {i: [] for i in range(n_clusters)}
            for i, doc in enumerate(docs):
                clusters[int(labels[i])].append({
                    'id':       doc.id,
                    'title':    doc.title,
                    'language': doc.language,
                })

            return clusters

        except Exception:
            return {0: [{'id': d.id, 'title': d.title,
                         'language': d.language} for d in docs]}

    def get_cluster_labels(self, n_clusters: int = 3) -> Dict[int, str]:
        """
        Generate a label for each cluster based on top TF-IDF terms.
        """
        docs = list(Document.objects.filter(is_indexed=True))
        if len(docs) < n_clusters:
            return {0: 'All Documents'}

        preprocessor = TextPreprocessor()
        texts = [preprocessor.preprocess_to_string(d.raw_text) for d in docs]

        try:
            vectorizer   = TfidfVectorizer(max_features=200, min_df=1)
            tfidf_matrix = vectorizer.fit_transform(texts)
            feature_names = vectorizer.get_feature_names_out()

            km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            km.fit(tfidf_matrix)

            labels = {}
            for i, center in enumerate(km.cluster_centers_):
                top_indices = center.argsort()[-3:][::-1]
                top_terms   = [feature_names[j] for j in top_indices]
                labels[i]   = ' · '.join(top_terms)

            return labels

        except Exception:
            return {i: f'Cluster {i+1}' for i in range(n_clusters)}


# ─────────────────────────────────────────────────────────────────────────
# 6. READABILITY SCORER
# ─────────────────────────────────────────────────────────────────────────
class ReadabilityScorer:
    """
    Computes a simple readability score for English text.
    Uses Flesch Reading Ease approximation.
    For non-English text returns a word/sentence ratio.
    """

    def score(self, text: str, language: str = 'english') -> Dict:
        sentences = re.split(r'[.!?።፡]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        words     = text.split()

        if not sentences or not words:
            return {'score': 0, 'level': 'Unknown', 'sentences': 0, 'words': 0}

        avg_sentence_len = len(words) / len(sentences)

        if language == 'english':
            # Approximate syllable count
            syllables = sum(self._count_syllables(w) for w in words)
            avg_syllables = syllables / len(words) if words else 1

            # Flesch Reading Ease
            flesch = 206.835 - 1.015 * avg_sentence_len - 84.6 * avg_syllables
            flesch = max(0, min(100, flesch))

            if flesch >= 70:
                level = 'Easy'
            elif flesch >= 50:
                level = 'Moderate'
            else:
                level = 'Difficult'
        else:
            # For other languages: use sentence length as proxy
            flesch = max(0, 100 - avg_sentence_len * 2)
            level  = 'Easy' if flesch > 60 else 'Moderate' if flesch > 30 else 'Difficult'

        return {
            'score':     round(flesch, 1),
            'level':     level,
            'sentences': len(sentences),
            'words':     len(words),
            'avg_sentence_len': round(avg_sentence_len, 1),
        }

    def _count_syllables(self, word: str) -> int:
        word = word.lower().strip(".,!?;:")
        if not word:
            return 0
        count   = 0
        vowels  = 'aeiouy'
        prev_v  = False
        for ch in word:
            is_v = ch in vowels
            if is_v and not prev_v:
                count += 1
            prev_v = is_v
        if word.endswith('e') and count > 1:
            count -= 1
        return max(1, count)
