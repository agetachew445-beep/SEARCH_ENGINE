"""
Advanced Text Preprocessing Pipeline
=====================================
Features:
  - Unicode normalisation (Ge'ez / Ethiopic + Latin)
  - Multi-language tokenisation (Amharic, Tigrinya, Afan Oromo, English)
  - Custom stopword removal per language
  - Suffix-stripping stemmer
  - Language auto-detection (heuristic)
  - N-gram extraction (bigrams / trigrams)
  - Keyword extraction (TF-based)
  - Sentence segmentation
  - Text cleaning (HTML tags, URLs, numbers, punctuation)
"""

import re
import unicodedata
import math
from collections import Counter
from pathlib import Path
from typing import List, Set, Dict, Tuple


# ─────────────────────────────────────────────────────────────────────────
# LANGUAGE DETECTOR  (heuristic — no external library needed)
# ─────────────────────────────────────────────────────────────────────────
def detect_language(text: str) -> str:
    """
    Heuristic language detection based on Unicode block frequencies.
    Returns: 'amharic' | 'tigrinya' | 'afan_oromo' | 'english' | 'mixed'
    """
    ethiopic = len(re.findall(r'[\u1200-\u137F]', text))
    latin    = len(re.findall(r'[a-zA-Z]', text))
    total    = ethiopic + latin

    if total == 0:
        return 'english'

    ethiopic_ratio = ethiopic / total

    if ethiopic_ratio > 0.6:
        # Distinguish Amharic vs Tigrinya by common words
        amharic_markers  = ['ነው', 'ናቸው', 'ይህ', 'እና', 'ላይ', 'ውስጥ', 'ስለ']
        tigrinya_markers = ['እዩ', 'ኢዩ', 'ኣብ', 'ካብ', 'ናብ', 'ምስ', 'ብ']
        am_count = sum(1 for m in amharic_markers if m in text)
        ti_count = sum(1 for m in tigrinya_markers if m in text)
        return 'tigrinya' if ti_count > am_count else 'amharic'

    if ethiopic_ratio > 0.1:
        return 'mixed'

    # Latin — check for Afan Oromo markers
    oromo_markers = ['fi', 'kan', 'keessa', 'irraa', 'itti', 'akka', 'yoo',
                     'barbaadaa', 'galmee', 'Itoophiyaa']
    if sum(1 for m in oromo_markers if m.lower() in text.lower()) >= 2:
        return 'afan_oromo'

    return 'english'


# ─────────────────────────────────────────────────────────────────────────
# MAIN PREPROCESSOR
# ─────────────────────────────────────────────────────────────────────────
class TextPreprocessor:

    def __init__(self, language: str = 'english'):
        self.language  = language
        self.stopwords = self._load_stopwords(language)

    # ── stopwords ──────────────────────────────────────────────────────
    def _load_stopwords(self, language: str) -> Set[str]:
        sw_file = Path(__file__).parent / 'stopwords' / f'{language}.txt'
        if sw_file.exists():
            with open(sw_file, encoding='utf-8') as f:
                return {ln.strip().lower() for ln in f if ln.strip()}
        # English fallback
        return {
            'a','an','and','are','as','at','be','by','for','from',
            'has','he','in','is','it','its','of','on','that','the',
            'to','was','will','with','this','but','they','have','had',
            'what','when','where','who','which','their','if','or',
            'because','been','were','can','could','would','should',
            'also','more','about','into','than','then','there','these',
            'those','after','before','between','through','during',
        }

    # ── text cleaning ──────────────────────────────────────────────────
    def clean_text(self, text: str) -> str:
        """Remove HTML tags, URLs, excessive whitespace."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
        # Remove email addresses
        text = re.sub(r'\S+@\S+', ' ', text)
        # Normalise whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    # ── unicode normalise ──────────────────────────────────────────────
    def normalize_unicode(self, text: str) -> str:
        return unicodedata.normalize('NFD', text)

    # ── sentence segmentation ─────────────────────────────────────────
    def split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        text = self.clean_text(text)
        # Split on sentence-ending punctuation
        sentences = re.split(r'(?<=[.!?።፡])\s+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]

    # ── tokenise ──────────────────────────────────────────────────────
    def tokenize(self, text: str) -> List[str]:
        """
        Tokeniser supporting:
          • Ethiopic / Ge'ez  U+1200–U+137F
          • Ethiopic Extended  U+2D80–U+2DDF
          • Latin \w
        """
        text = self.normalize_unicode(text).lower()
        text = self.clean_text(text)
        return re.findall(r'[\u1200-\u137F\u2D80-\u2DDF\w]+', text)

    # ── stopword removal ──────────────────────────────────────────────
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        return [t for t in tokens if t not in self.stopwords and len(t) > 1]

    # ── stemmer ───────────────────────────────────────────────────────
    def stem(self, token: str) -> str:
        """
        Suffix-stripping stemmer for English.
        Ethiopic tokens are returned unchanged (morphology is complex).
        """
        # Skip Ethiopic tokens
        if re.search(r'[\u1200-\u137F]', token):
            return token
        # English suffixes (ordered longest-first)
        for suffix in ('ational','tional','enci','anci','izer','ising',
                       'izing','ation','ator','alism','ness','ment',
                       'ing','tion','ous','ive','ful','ise','ize',
                       'ed','es','ly','er','al','s'):
            if token.endswith(suffix) and len(token) > len(suffix) + 2:
                return token[:-len(suffix)]
        return token

    # ── n-gram extraction ─────────────────────────────────────────────
    def get_ngrams(self, tokens: List[str], n: int = 2) -> List[str]:
        """Return n-grams as underscore-joined strings."""
        return ['_'.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

    # ── keyword extraction ────────────────────────────────────────────
    def extract_keywords(self, text: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """
        Extract top-K keywords using TF score.
        Returns list of (keyword, score) tuples.
        """
        tokens = self.preprocess(text, apply_stemming=False)
        if not tokens:
            return []

        tf = Counter(tokens)
        total = len(tokens)
        scored = [(word, count / total) for word, count in tf.most_common(top_k * 2)]

        # Prefer longer, more meaningful words
        scored = [(w, s * (1 + len(w) * 0.05)) for w, s in scored
                  if len(w) >= 3]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    # ── full pipeline ─────────────────────────────────────────────────
    def preprocess(self, text: str, apply_stemming: bool = True,
                   include_bigrams: bool = False) -> List[str]:
        tokens = self.tokenize(text)
        tokens = self.remove_stopwords(tokens)
        if apply_stemming:
            tokens = [self.stem(t) for t in tokens]
        if include_bigrams:
            bigrams = self.get_ngrams(tokens, 2)
            tokens  = tokens + bigrams
        return tokens

    def preprocess_to_string(self, text: str, apply_stemming: bool = True) -> str:
        return ' '.join(self.preprocess(text, apply_stemming))


# ─────────────────────────────────────────────────────────────────────────
# EXTRACTIVE SUMMARISER  (no external ML library needed)
# ─────────────────────────────────────────────────────────────────────────
class ExtractiveSummarizer:
    """
    Extractive summarisation using TF-IDF sentence scoring.
    Works for all languages including Amharic, Tigrinya, Afan Oromo.
    """

    def __init__(self):
        self.preprocessor = TextPreprocessor()

    def _score_sentences(self, sentences: List[str],
                         word_freq: Dict[str, float]) -> List[Tuple[int, float]]:
        """Score each sentence by sum of word TF-IDF weights."""
        scored = []
        for i, sent in enumerate(sentences):
            tokens = self.preprocessor.tokenize(sent)
            tokens = self.preprocessor.remove_stopwords(tokens)
            if not tokens:
                scored.append((i, 0.0))
                continue
            score = sum(word_freq.get(t, 0) for t in tokens) / len(tokens)
            # Slight bonus for sentences in the first 30% of the document
            position_bonus = 1.2 if i < max(1, len(sentences) * 0.3) else 1.0
            scored.append((i, score * position_bonus))
        return scored

    def summarize(self, text: str, num_sentences: int = 3,
                  language: str = 'english') -> str:
        """
        Return an extractive summary of *text*.

        Args:
            text:          Full document text
            num_sentences: Number of sentences in summary
            language:      Document language

        Returns:
            Summary string
        """
        preprocessor = TextPreprocessor(language=language)
        sentences    = preprocessor.split_sentences(text)

        if len(sentences) <= num_sentences:
            return text.strip()

        # Build word frequency table
        all_tokens = preprocessor.preprocess(text, apply_stemming=True)
        if not all_tokens:
            return ' '.join(sentences[:num_sentences])

        tf = Counter(all_tokens)
        max_freq = max(tf.values()) or 1
        word_freq = {w: c / max_freq for w, c in tf.items()}

        # Score and select top sentences
        scored = self._score_sentences(sentences, word_freq)
        top_indices = sorted(
            sorted(scored, key=lambda x: x[1], reverse=True)[:num_sentences],
            key=lambda x: x[0]   # restore original order
        )

        summary = ' '.join(sentences[i] for i, _ in top_indices)
        return summary.strip()


# ─────────────────────────────────────────────────────────────────────────
# CONCEPT EXTRACTOR  (key concepts / topics from a document)
# ─────────────────────────────────────────────────────────────────────────
class ConceptExtractor:
    """
    Extracts key concepts using:
      1. High-frequency unigrams
      2. Meaningful bigrams (noun phrases approximation)
      3. Named-entity-like patterns (capitalised phrases)
    """

    def __init__(self):
        self.preprocessor = TextPreprocessor()

    def extract_concepts(self, text: str, top_k: int = 8) -> List[str]:
        """Return top-K concepts from text."""
        concepts = []

        # 1. Top keywords
        kw = self.preprocessor.extract_keywords(text, top_k=top_k * 2)
        concepts += [w for w, _ in kw]

        # 2. Capitalised multi-word phrases (English named entities)
        cap_phrases = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b', text)
        concepts += cap_phrases[:top_k]

        # 3. Ethiopic frequent phrases (2-word sequences)
        ethiopic_words = re.findall(r'[\u1200-\u137F]+', text)
        if ethiopic_words:
            bigrams = [f'{ethiopic_words[i]} {ethiopic_words[i+1]}'
                       for i in range(len(ethiopic_words)-1)]
            bg_freq = Counter(bigrams)
            concepts += [bg for bg, _ in bg_freq.most_common(top_k // 2)]

        # Deduplicate while preserving order
        seen, unique = set(), []
        for c in concepts:
            c_clean = c.strip()
            if c_clean and c_clean.lower() not in seen and len(c_clean) > 2:
                seen.add(c_clean.lower())
                unique.append(c_clean)

        return unique[:top_k]


# ─────────────────────────────────────────────────────────────────────────
# SNIPPET EXTRACTOR  (used by views)
# ─────────────────────────────────────────────────────────────────────────
def extract_snippet(text: str, query_terms: List[str],
                    max_length: int = 250) -> str:
    """
    Return a short excerpt centred on the first query term found.
    Highlights are added with ** markers (rendered in template).
    """
    text = text.strip()
    if len(text) <= max_length:
        return text

    text_lower = text.lower()
    best_pos   = -1

    for term in query_terms:
        pos = text_lower.find(term.lower())
        if pos != -1 and (best_pos == -1 or pos < best_pos):
            best_pos = pos

    if best_pos == -1:
        return text[:max_length] + '…'

    half    = max_length // 2
    start   = max(0, best_pos - half)
    end     = min(len(text), start + max_length)
    snippet = text[start:end]

    if start > 0:
        snippet = '…' + snippet
    if end < len(text):
        snippet = snippet + '…'

    return snippet
