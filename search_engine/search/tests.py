"""
Unit tests for IR Search Engine.
Run with: python manage.py test
"""
from django.test import TestCase, Client
from django.utils import timezone
from .models import Document, IndexEntry, EvaluationMetric
from .preprocessing import TextPreprocessor, extract_snippet
from .indexing import InvertedIndexBuilder
from .ranking import RankingEngine
from .evaluation import IREvaluator


class PreprocessingTests(TestCase):
    """Test text preprocessing functionality."""
    
    def setUp(self):
        self.preprocessor = TextPreprocessor(language='english')
    
    def test_tokenization(self):
        """Test tokenization."""
        text = "Information Retrieval System"
        tokens = self.preprocessor.tokenize(text)
        self.assertEqual(tokens, ['information', 'retrieval', 'system'])
    
    def test_stopword_removal(self):
        """Test stopword removal."""
        tokens = ['the', 'information', 'retrieval', 'is', 'important']
        filtered = self.preprocessor.remove_stopwords(tokens)
        self.assertNotIn('the', filtered)
        self.assertNotIn('is', filtered)
        self.assertIn('information', filtered)
    
    def test_preprocessing_pipeline(self):
        """Test complete preprocessing."""
        text = "The information retrieval system is working"
        tokens = self.preprocessor.preprocess(text)
        self.assertIsInstance(tokens, list)
        self.assertTrue(len(tokens) > 0)
    
    def test_snippet_extraction(self):
        """Test snippet extraction."""
        text = "This is a long document. " * 50
        query_terms = ['document']
        snippet = extract_snippet(text, query_terms, max_length=100)
        self.assertLessEqual(len(snippet), 110)  # Allow for ellipsis


class DocumentModelTests(TestCase):
    """Test Document model."""
    
    def test_document_creation(self):
        """Test creating a document."""
        doc = Document.objects.create(
            title="Test Document",
            raw_text="This is test content",
            language="english"
        )
        self.assertEqual(doc.title, "Test Document")
        self.assertFalse(doc.is_indexed)
    
    def test_document_str(self):
        """Test document string representation."""
        doc = Document.objects.create(
            title="Test Doc",
            raw_text="Content"
        )
        self.assertEqual(str(doc), "Test Doc")


class IndexingTests(TestCase):
    """Test indexing functionality."""
    
    def setUp(self):
        self.doc1 = Document.objects.create(
            title="IR Document",
            raw_text="Information retrieval is important for search engines",
            language="english"
        )
        self.doc2 = Document.objects.create(
            title="Search Systems",
            raw_text="Search engines use information retrieval techniques",
            language="english"
        )
        self.indexer = InvertedIndexBuilder()
    
    def test_index_building(self):
        """Test building inverted index."""
        term_count = self.indexer.build_index()
        self.assertGreater(term_count, 0)
        
        # Check documents are marked as indexed
        self.doc1.refresh_from_db()
        self.assertTrue(self.doc1.is_indexed)
    
    def test_index_entry_creation(self):
        """Test index entries are created."""
        self.indexer.build_index()
        entries = IndexEntry.objects.all()
        self.assertGreater(entries.count(), 0)
    
    def test_postings_list(self):
        """Test postings list structure."""
        self.indexer.build_index()
        entry = IndexEntry.objects.first()
        postings = entry.get_postings()
        self.assertIsInstance(postings, list)


class RankingTests(TestCase):
    """Test ranking algorithms."""
    
    def setUp(self):
        # Create test documents
        self.doc1 = Document.objects.create(
            title="IR Basics",
            raw_text="Information retrieval systems help find relevant documents",
            language="english"
        )
        self.doc2 = Document.objects.create(
            title="Search Engines",
            raw_text="Search engines are information retrieval systems",
            language="english"
        )
        
        # Build index
        indexer = InvertedIndexBuilder()
        indexer.build_index()
    
    def test_cosine_similarity_search(self):
        """Test VSM cosine similarity search."""
        engine = RankingEngine(ranking_model='cosine')
        results = engine.search("information retrieval", top_k=10)
        self.assertIsInstance(results, list)
    
    def test_bm25_search(self):
        """Test BM25 search."""
        engine = RankingEngine(ranking_model='bm25')
        results = engine.search("information retrieval", top_k=10)
        self.assertIsInstance(results, list)
    
    def test_ranking_order(self):
        """Test results are ranked by score."""
        engine = RankingEngine(ranking_model='cosine')
        results = engine.search("information retrieval", top_k=10)
        
        if len(results) > 1:
            # Check scores are in descending order
            scores = [score for _, score in results]
            self.assertEqual(scores, sorted(scores, reverse=True))


class EvaluationTests(TestCase):
    """Test evaluation metrics."""
    
    def setUp(self):
        self.evaluator = IREvaluator()
    
    def test_precision_at_k(self):
        """Test Precision@K calculation."""
        retrieved = [1, 2, 3, 4, 5]
        relevant = {1, 3, 5}
        
        precision = self.evaluator.precision_at_k(retrieved, relevant, k=5)
        self.assertEqual(precision, 0.6)  # 3/5
    
    def test_recall(self):
        """Test Recall calculation."""
        retrieved = [1, 2, 3]
        relevant = {1, 3, 5, 7}
        
        recall = self.evaluator.recall(retrieved, relevant)
        self.assertEqual(recall, 0.5)  # 2/4
    
    def test_f_measure(self):
        """Test F1 calculation."""
        precision = 0.6
        recall    = 0.5

        f1_score = self.evaluator.f1(precision, recall)
        expected = 2 * (0.6 * 0.5) / (0.6 + 0.5)
        self.assertAlmostEqual(f1_score, expected, places=2)


class ViewTests(TestCase):
    """Test web interface views."""
    
    def setUp(self):
        self.client = Client()
    
    def test_index_view(self):
        """Test home page loads."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search Engine')
    
    def test_search_view_empty_query(self):
        """Test search with empty query."""
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)
    
    def test_search_view_with_query(self):
        """Test search with query."""
        # Create and index a document
        doc = Document.objects.create(
            title="Test",
            raw_text="information retrieval",
            language="english"
        )
        indexer = InvertedIndexBuilder()
        indexer.build_index()
        
        response = self.client.get('/search/', {'q': 'information', 'model': 'cosine'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'results')


class EvaluationMetricModelTests(TestCase):
    """Test EvaluationMetric model."""
    
    def test_metric_creation(self):
        """Test creating evaluation metric."""
        metric = EvaluationMetric.objects.create(
            query="test query",
            ranking_model="cosine",
            precision_at_5=0.8,
            recall=0.6
        )
        self.assertEqual(metric.query, "test query")
        self.assertEqual(metric.precision_at_5, 0.8)
    
    def test_relevant_docs_json(self):
        """Test JSON serialization of relevant docs."""
        metric = EvaluationMetric.objects.create(
            query="test",
            ranking_model="cosine"
        )
        metric.set_relevant_docs([1, 2, 3])
        metric.save()
        
        metric.refresh_from_db()
        docs = metric.get_relevant_docs()
        self.assertEqual(docs, [1, 2, 3])
