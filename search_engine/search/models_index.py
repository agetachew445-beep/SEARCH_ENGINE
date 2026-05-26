from django.db import models
import json


class IndexEntry(models.Model):
    """
    Represents an entry in the inverted index.
    Maps terms to documents with frequency information.
    """
    term = models.CharField(max_length=200, unique=True, db_index=True)
    document_frequency = models.IntegerField(default=0)
    postings_list = models.TextField(
        help_text="JSON: [{doc_id, term_freq, positions}, ...]"
    )
    idf = models.FloatField(default=0.0, help_text="Inverse Document Frequency")
    
    class Meta:
        ordering = ['term']
        verbose_name = 'Index Entry'
        verbose_name_plural = 'Index Entries'
    
    def get_postings(self):
        """Parse and return postings list as Python object."""
        if self.postings_list:
            return json.loads(self.postings_list)
        return []
    
    def set_postings(self, postings):
        """Set postings list from Python object."""
        self.postings_list = json.dumps(postings)
    
    def __str__(self):
        return f"{self.term} (DF: {self.document_frequency})"
