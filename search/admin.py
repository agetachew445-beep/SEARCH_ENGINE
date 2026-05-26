"""
Django Admin configuration for the IR Search Engine.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Document, IndexEntry, SearchLog, EvaluationMetric


# ─────────────────────────────────────────────
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display  = ['id', 'title', 'language', 'doc_type',
                     'word_count_display', 'is_indexed', 'pub_date']
    list_filter   = ['language', 'doc_type', 'is_indexed']
    search_fields = ['title', 'raw_text']
    readonly_fields = ['processed_text', 'created_at', 'updated_at']
    ordering      = ['-pub_date']

    fieldsets = (
        ('Document Info', {
            'fields': ('title', 'language', 'doc_type', 'url', 'pub_date', 'file')
        }),
        ('Content', {
            'fields': ('raw_text', 'processed_text')
        }),
        ('Index Status', {
            'fields': ('is_indexed',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Words')
    def word_count_display(self, obj):
        return obj.word_count()


# ─────────────────────────────────────────────
@admin.register(IndexEntry)
class IndexEntryAdmin(admin.ModelAdmin):
    list_display  = ['term', 'document_frequency', 'idf_display']
    search_fields = ['term']
    readonly_fields = ['postings_list']
    ordering      = ['term']

    @admin.display(description='IDF')
    def idf_display(self, obj):
        return f'{obj.idf:.4f}'


# ─────────────────────────────────────────────
@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display  = ['query', 'ranking_model', 'num_results',
                     'query_time_display', 'searched_at']
    list_filter   = ['ranking_model', 'searched_at']
    search_fields = ['query']
    readonly_fields = ['query', 'ranking_model', 'num_results',
                       'query_time', 'searched_at']

    @admin.display(description='Time (s)')
    def query_time_display(self, obj):
        return f'{obj.query_time:.3f}s'


# ─────────────────────────────────────────────
@admin.register(EvaluationMetric)
class EvaluationMetricAdmin(admin.ModelAdmin):
    list_display  = ['query', 'ranking_model', 'precision_at_5',
                     'recall', 'f1_score', 'created_at']
    list_filter   = ['ranking_model', 'created_at']
    search_fields = ['query']
    readonly_fields = ['created_at']
