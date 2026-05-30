"""
Database models for the IR Search Engine.
Uses SQLite via Django ORM.

Models:
  - Document        : stores raw + processed text
  - IndexEntry      : inverted index (term → postings)
  - SearchLog       : every query the user runs
  - EvaluationMetric: precision / recall results
"""

import json
from django.db import models
from django.utils import timezone


# ─────────────────────────────────────────────
# 1. DOCUMENT
# ─────────────────────────────────────────────
class Document(models.Model):
    LANGUAGE_CHOICES = [
        ('amharic',   'Amharic'),
        ('tigrinya',  'Tigrinya'),
        ('afan_oromo','Afan Oromo'),
        ('english',   'English'),
        ('mixed',     'Mixed'),
    ]
    DOCTYPE_CHOICES = [
        ('txt',  'Text'),
        ('pdf',  'PDF'),
        ('html', 'HTML'),
    ]

    title          = models.CharField(max_length=500)
    raw_text       = models.TextField(help_text="Original document text")
    processed_text = models.TextField(blank=True, help_text="Preprocessed / tokenised text")
    summary        = models.TextField(blank=True, help_text="Auto-generated extractive summary")
    concepts       = models.TextField(blank=True, default='[]', help_text="JSON list of key concepts")
    url            = models.URLField(blank=True, null=True)
    pub_date       = models.DateTimeField(default=timezone.now)
    doc_type       = models.CharField(max_length=10, choices=DOCTYPE_CHOICES, default='txt')
    file           = models.FileField(upload_to='documents/', blank=True, null=True)
    language       = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='english')
    is_indexed     = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pub_date']
        indexes  = [
            models.Index(fields=['language']),
            models.Index(fields=['is_indexed']),
        ]

    def __str__(self):
        return self.title

    def word_count(self):
        return len(self.raw_text.split())

    def get_concepts_list(self):
        try:
            return json.loads(self.concepts)
        except (json.JSONDecodeError, TypeError):
            return []

    def set_concepts_list(self, concepts):
        self.concepts = json.dumps(concepts)


# ─────────────────────────────────────────────
# 2. INVERTED INDEX ENTRY
# ─────────────────────────────────────────────
class IndexEntry(models.Model):
    """
    One row per unique term.
    postings_list is stored as JSON:
      [ {"doc_id": 1, "term_freq": 3, "positions": [0, 5, 12]}, ... ]
    """
    term               = models.CharField(max_length=200, unique=True, db_index=True)
    document_frequency = models.IntegerField(default=0)
    idf                = models.FloatField(default=0.0)
    postings_list      = models.TextField(default='[]')

    class Meta:
        ordering = ['term']

    # ── helpers ──
    def get_postings(self):
        try:
            return json.loads(self.postings_list)
        except (json.JSONDecodeError, TypeError):
            return []

    def set_postings(self, postings):
        self.postings_list = json.dumps(postings)

    def __str__(self):
        return f"{self.term}  (df={self.document_frequency}, idf={self.idf:.3f})"


# ─────────────────────────────────────────────
# 3. SEARCH LOG  (every query is recorded)
# ─────────────────────────────────────────────
class SearchLog(models.Model):
    query         = models.CharField(max_length=500)
    ranking_model = models.CharField(max_length=20, default='cosine')
    num_results   = models.IntegerField(default=0)
    query_time    = models.FloatField(default=0.0, help_text="Seconds")
    searched_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-searched_at']

    def __str__(self):
        return f'"{self.query}" [{self.ranking_model}] → {self.num_results} results'


# ─────────────────────────────────────────────
# 4. EVALUATION METRIC
# ─────────────────────────────────────────────
class EvaluationMetric(models.Model):
    query          = models.CharField(max_length=500)
    ranking_model  = models.CharField(
        max_length=20,
        choices=[('cosine', 'Cosine Similarity'), ('bm25', 'BM25')]
    )
    precision_at_5  = models.FloatField(default=0.0)
    precision_at_10 = models.FloatField(default=0.0)
    recall          = models.FloatField(default=0.0)
    f1_score        = models.FloatField(default=0.0)
    num_results     = models.IntegerField(default=0)
    query_time      = models.FloatField(default=0.0)
    relevant_docs   = models.TextField(blank=True, default='[]')
    retrieved_docs  = models.TextField(blank=True, default='[]')
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_relevant_docs(self):
        try:
            return json.loads(self.relevant_docs)
        except (json.JSONDecodeError, TypeError):
            return []

    def set_relevant_docs(self, docs):
        self.relevant_docs = json.dumps(docs)

    def get_retrieved_docs(self):
        try:
            return json.loads(self.retrieved_docs)
        except (json.JSONDecodeError, TypeError):
            return []

    def set_retrieved_docs(self, docs):
        self.retrieved_docs = json.dumps(docs)

    def __str__(self):
        return (f'"{self.query}" [{self.ranking_model}] '
                f'P@5={self.precision_at_5:.2f} R={self.recall:.2f}')
