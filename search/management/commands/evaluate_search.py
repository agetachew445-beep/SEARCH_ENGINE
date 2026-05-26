"""
python manage.py evaluate_search

Runs 10 test queries, computes Precision@5, Recall, F1, MAP
for both VSM and BM25, prints a comparison table, and saves
results to the EvaluationMetric table in SQLite.
"""

from django.core.management.base import BaseCommand
from search.evaluation import IREvaluator
from search.models import EvaluationMetric


TEST_QUERIES = [
    {'query': 'information retrieval',      'relevant_docs': [1, 2, 7]},
    {'query': 'vector space model',         'relevant_docs': [2]},
    {'query': 'tf-idf weighting',           'relevant_docs': [3]},
    {'query': 'bm25 ranking function',      'relevant_docs': [4]},
    {'query': 'text preprocessing',         'relevant_docs': [6]},
    {'query': 'inverted index structure',   'relevant_docs': [7]},
    {'query': 'precision recall metrics',   'relevant_docs': [8]},
    {'query': 'natural language processing','relevant_docs': [5]},
    {'query': 'search engine documents',    'relevant_docs': [1, 4, 7]},
    {'query': 'document ranking score',     'relevant_docs': [2, 4]},
]


class Command(BaseCommand):
    help = 'Evaluate VSM vs BM25 on 10 test queries and save results to SQLite'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== IR Evaluation ===\n'))

        evaluator  = IREvaluator()
        comparison = evaluator.compare_ranking_models(TEST_QUERIES)

        # ── print table ──
        header = f"{'Metric':<22} {'VSM (Cosine)':>14} {'BM25':>10}"
        self.stdout.write(header)
        self.stdout.write('-' * len(header))

        rows = [
            ('Avg Precision@5',  'avg_precision_at_5'),
            ('Avg Precision@10', 'avg_precision_at_10'),
            ('Avg Recall',       'avg_recall'),
            ('Avg F1',           'avg_f1'),
            ('MAP',              'map'),
            ('Avg Query Time',   'avg_query_time'),
        ]

        for label, key in rows:
            vsm_val  = comparison['cosine'][key]
            bm25_val = comparison['bm25'][key]
            unit     = 's' if 'time' in key else ''
            self.stdout.write(
                f"{label:<22} {vsm_val:>13.4f}{unit}  {bm25_val:>9.4f}{unit}"
            )

        # ── save to SQLite ──
        self.stdout.write('\nSaving results to SQLite…')
        for model in ('cosine', 'bm25'):
            for m in comparison['detailed'][model]:
                evaluator.save_metrics(m)

        self.stdout.write(self.style.SUCCESS(
            f'\n✓  Saved {len(TEST_QUERIES) * 2} evaluation records.'
        ))
        self.stdout.write(
            'View in admin: http://127.0.0.1:8000/admin/search/evaluationmetric/'
        )
