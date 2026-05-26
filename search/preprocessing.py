"""
Text preprocessing pipeline.
Supports Amharic / Tigrinya / Afan Oromo (Ge'ez script) and English.

Pipeline:
  raw text → unicode normalise → tokenise → lowercase
           → stopword removal → stemming → token list
"""

import re
import unicodedata
from pathlib import Path
from typing import List, Set


# ─────────────────────────────────────────────
class TextPreprocessor:
# ─────────────────────────────────────────────

    def __init__(self, language: str = 'english'):
        self.language  = language
        self.stopwords = self._load_stopwords(language)

    # ── stopwords ──────────────────────────────
    def _load_stopwords(self, language: str) -> Set[str]:
        sw_file = Path(__file__).parent / 'stopwords' / f'{language}.txt'
        if sw_file.exists():
            with open(sw_file, encoding='utf-8') as f:
                return {ln.strip().lower() for ln in f if ln.strip()}

        # built-in English fallback
        return {
            'a','an','and','are','as','at','be','by','for','from',
            'has','he','in','is','it','its','of','on','that','the',
            'to','was','will','with','this','but','they','have','had',
            'what','when','where','who','which','their','if','or',
            'because','been','were','can','could','would','should',
        }

    # ── unicode normalise ───────────────────────
    def normalize_unicode(self, text: str) -> str:
        """NFD normalisation — important for Ge'ez / Ethiopic scripts."""
        return unicodedata.normalize('NFD', text)

    # ── tokenise ───────────────────────────────
    def tokenize(self, text: str) -> List[str]:
        """
        Regex tokeniser that keeps:
          • Ethiopic / Ge'ez characters  U+1200–U+137F
          • Latin word characters  \w
        """
        text = self.normalize_unicode(text).lower()
        return re.findall(r'[\u1200-\u137F\w]+', text)

    # ── stopword removal ────────────────────────
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        return [t for t in tokens if t not in self.stopwords]

    # ── stemming ────────────────────────────────
    def stem(self, token: str) -> str:
        """
        Lightweight suffix-stripping stemmer.
        Works for English; extend per-language as needed.
        """
        for suffix in ('ing', 'tion', 'ness', 'ment', 'ed', 'es', 'ly', 's'):
            if token.endswith(suffix) and len(token) > len(suffix) + 2:
                return token[: -len(suffix)]
        return token

    # ── full pipeline ───────────────────────────
    def preprocess(self, text: str, apply_stemming: bool = True) -> List[str]:
        tokens = self.tokenize(text)
        tokens = self.remove_stopwords(tokens)
        if apply_stemming:
            tokens = [self.stem(t) for t in tokens]
        return tokens

    def preprocess_to_string(self, text: str, apply_stemming: bool = True) -> str:
        return ' '.join(self.preprocess(text, apply_stemming))


# ─────────────────────────────────────────────
# Snippet extractor (used by views)
# ─────────────────────────────────────────────
def extract_snippet(text: str, query_terms: List[str], max_length: int = 250) -> str:
    """
    Return a short excerpt from *text* centred on the first query term found.
    Falls back to the beginning of the text if no term is found.
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

    half   = max_length // 2
    start  = max(0, best_pos - half)
    end    = min(len(text), start + max_length)
    snippet = text[start:end]

    if start > 0:
        snippet = '…' + snippet
    if end < len(text):
        snippet = snippet + '…'

    return snippet
