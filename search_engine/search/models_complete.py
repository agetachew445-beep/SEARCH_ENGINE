# Complete models file - merge this content into models.py
from django.db import models
from django.utils import timezone
import json


class EvaluationMetric(models.Model):
    """
    Stores evaluation results for search queries.
    """
    query = models.CharField(max_length=500)
    ranking_model = models.CharField(
        max_length=20,
        choices=[('cosine', 'Cosine Similarity'), ('bm25', 'BM25')]
    )
    precision_at_5 = models.FloatField(default=0.0)
    precision_at_10 = models.FloatField(default=0.0)
    recall = models.FloatField(default=0.0)
    num_results = models.IntegerField(default=0)
    query_time = models.FloatField(default=0.0, help_text="Query time in seconds")
    relevant_docs = models.TextField(
        blank=True,
        help_text="JSON list of relevant document IDs"
    )
    retrieved_docs = models.TextField(
        blank=True,
        help_text="JSON list of retrieved document IDs"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def get_relevant_docs(self):
        if self.relevant_docs:
            return json.loads(self.relevant_docs)
        return []
    
    def set_relevant_docs(self, docs):
        self.relevant_docs = json.dumps(docs)
    
    def get_retrieved_docs(self):
        if self.retrieved_docs:
            return json.loads(self.retrieved_docs)
        return []
    
    def set_retrieved_docs(self, docs):
        self.retrieved_docs = json.dumps(docs)
    
    def __str__(self):
        return f"{self.query} - {self.ranking_model} (P@5: {self.precision_at_5:.2f})"
