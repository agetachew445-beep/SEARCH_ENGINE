"""
Evaluation module.

Metrics implemented:
  • Precision@K  (default K = 5 and 10)
  • Recall
  • F1-score
  • Mean Average Precision (MAP)
  • Model comparison (VSM vs BM25)
"""

import time
from typing import Dict, List, Set

from .models import EvaluationMetric
from .ranking import RankingEngine


class IREvaluator:

    def __init__(self):
        self._engines = {
            'cosine': RankingEngine(ranking_model='cosine'),
            'bm25':   RankingEngine(ranking_model='bm25'),
        }

    # ─────────────────────────────────────────
    # CORE METRICS
    # ─────────────────────────────────────────
    def precision_at_k(self, retrieved: List[int],
                       relevant: Set[int], k: int) -> float:
        if k == 0 or not retrieved:
            return 0.0
        hits = sum(1 for d in retrieved[:k] if d in relevant)
        return hits / k

    def recall(self, retrieved: List[int], relevant: Set[int]) -> float:
        if not relevant:
            return 0.0
        hits = sum(1 for d in retrieved if d in relevant)
        return hits / len(relevant)

    def f1(self, precision: float, recall: float) -> float:
        if precision + recall == 0:
            return 0.0
        return 2 * precision * recall / (precision + recall)

    def average_precision(self, retrieved: List[int],
                          relevant: Set[int]) -> float:
        """Area under the precision-recall curve (AP)."""
        if not relevant:
            return 0.0
        hits, total = 0, 0.0
        for rank, did in enumerate(retrieved, start=1):
            if did in relevant:
                hits  += 1
                total += hits / rank
        return total / len(relevant)

    # ─────────────────────────────────────────
    # SINGLE QUERY EVALUATION
    # ─────────────────────────────────────────
    def evaluate_query(self, query: str, relevant_docs: Set[int],
                       ranking_model: str = 'cosine',
                       k_values: List[int] = None) -> Dict:
        if k_values is None:
            k_values = [5, 10]

        engine = self._engines.get(ranking_model,
                                   self._engines['cosine'])

        t0      = time.time()
        results = engine.search(query, top_k=50)
        elapsed = time.time() - t0

        retrieved = [did for did, _ in results]
        p5  = self.precision_at_k(retrieved, relevant_docs, 5)
        p10 = self.precision_at_k(retrieved, relevant_docs, 10)
        r   = self.recall(retrieved, relevant_docs)

        metrics = {
            'query':         query,
            'ranking_model': ranking_model,
            'num_results':   len(retrieved),
            'query_time':    elapsed,
            'precision_at_5':  p5,
            'precision_at_10': p10,
            'recall':          r,
            'f1_score':        self.f1(p5, r),
            'avg_precision':   self.average_precision(retrieved, relevant_docs),
        }
        for k in k_values:
            metrics[f'precision_at_{k}'] = self.precision_at_k(
                retrieved, relevant_docs, k)

        return metrics

    # ─────────────────────────────────────────
    # COMPARE VSM vs BM25
    # ─────────────────────────────────────────
    def compare_ranking_models(self, test_queries: List[Dict]) -> Dict:
        """
        test_queries = [
            {'query': 'information retrieval', 'relevant_docs': [1, 3]},
            ...
        ]
        """
        all_results = {'cosine': [], 'bm25': []}

        for tc in test_queries:
            q    = tc['query']
            rel  = set(tc['relevant_docs'])
            for model in ('cosine', 'bm25'):
                all_results[model].append(
                    self.evaluate_query(q, rel, ranking_model=model)
                )

        def avg(lst, key):
            vals = [r[key] for r in lst if key in r]
            return sum(vals) / len(vals) if vals else 0.0

        summary = {}
        for model in ('cosine', 'bm25'):
            lst = all_results[model]
            summary[model] = {
                'avg_precision_at_5':  avg(lst, 'precision_at_5'),
                'avg_precision_at_10': avg(lst, 'precision_at_10'),
                'avg_recall':          avg(lst, 'recall'),
                'avg_f1':              avg(lst, 'f1_score'),
                'map':                 avg(lst, 'avg_precision'),
                'avg_query_time':      avg(lst, 'query_time'),
            }

        return {**summary, 'detailed': all_results}

    # ─────────────────────────────────────────
    # SAVE TO DB
    # ─────────────────────────────────────────
    def save_metrics(self, metrics: Dict) -> EvaluationMetric:
        return EvaluationMetric.objects.create(
            query           = metrics['query'],
            ranking_model   = metrics['ranking_model'],
            precision_at_5  = metrics.get('precision_at_5',  0.0),
            precision_at_10 = metrics.get('precision_at_10', 0.0),
            recall          = metrics.get('recall',          0.0),
            f1_score        = metrics.get('f1_score',        0.0),
            num_results     = metrics.get('num_results',     0),
            query_time      = metrics.get('query_time',      0.0),
        )
