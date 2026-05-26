"""
Demo script to showcase IR Search Engine functionality.
Run with: python demo_script.py
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'search_engine.settings')
django.setup()

from search.models import Document, IndexEntry
from search.preprocessing import TextPreprocessor
from search.indexing import InvertedIndexBuilder
from search.ranking import RankingEngine
from search.evaluation import IREvaluator
from django.utils import timezone


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def demo_preprocessing():
    """Demonstrate text preprocessing."""
    print_section("1. TEXT PREPROCESSING DEMO")
    
    preprocessor = TextPreprocessor(language='english')
    
    text = "The Information Retrieval System is working efficiently!"
    print(f"Original text: {text}")
    
    # Tokenization
    tokens = preprocessor.tokenize(text)
    print(f"Tokens: {tokens}")
    
    # Stopword removal
    filtered = preprocessor.remove_stopwords(tokens)
    print(f"After stopword removal: {filtered}")
    
    # Full preprocessing
    processed = preprocessor.preprocess(text)
    print(f"Fully processed: {processed}")


def demo_indexing():
    """Demonstrate indexing."""
    print_section("2. INDEXING DEMO")
    
    # Check if documents exist
    doc_count = Document.objects.count()
    print(f"Documents in database: {doc_count}")
    
    if doc_count == 0:
        print("Creating sample documents...")
        docs = [
            {
                'title': 'Information Retrieval Basics',
                'text': 'Information retrieval is the process of obtaining relevant information from a collection of documents.',
            },
            {
                'title': 'Search Engines',
                'text': 'Search engines use information retrieval techniques to find relevant web pages.',
            },
        ]
        
        for doc_data in docs:
            Document.objects.create(
                title=doc_data['title'],
                raw_text=doc_data['text'],
                language='english',
                pub_date=timezone.now()
            )
        print(f"Created {len(docs)} sample documents")
    
    # Build index
    print("\nBuilding inverted index...")
    indexer = InvertedIndexBuilder()
    term_count = indexer.build_index()
    print(f"Index built with {term_count} unique terms")
    
    # Show sample index entries
    print("\nSample index entries:")
    for entry in IndexEntry.objects.all()[:5]:
        print(f"  Term: '{entry.term}' | DF: {entry.document_frequency} | IDF: {entry.idf:.4f}")


def demo_search():
    """Demonstrate search functionality."""
    print_section("3. SEARCH DEMO")
    
    query = "information retrieval"
    print(f"Query: '{query}'")
    
    # VSM Search
    print("\n--- Vector Space Model (Cosine Similarity) ---")
    engine_vsm = RankingEngine(ranking_model='cosine')
    results_vsm = engine_vsm.search(query, top_k=5)
    
    if results_vsm:
        for rank, (doc_id, score) in enumerate(results_vsm, 1):
            try:
                doc = Document.objects.get(id=doc_id)
                print(f"{rank}. {doc.title} (Score: {score:.4f})")
            except Document.DoesNotExist:
                pass
    else:
        print("No results found")
    
    # BM25 Search
    print("\n--- BM25 Ranking ---")
    engine_bm25 = RankingEngine(ranking_model='bm25')
    results_bm25 = engine_bm25.search(query, top_k=5)
    
    if results_bm25:
        for rank, (doc_id, score) in enumerate(results_bm25, 1):
            try:
                doc = Document.objects.get(id=doc_id)
                print(f"{rank}. {doc.title} (Score: {score:.4f})")
            except Document.DoesNotExist:
                pass
    else:
        print("No results found")


def demo_evaluation():
    """Demonstrate evaluation metrics."""
    print_section("4. EVALUATION DEMO")
    
    evaluator = IREvaluator()
    
    # Example evaluation
    retrieved = [1, 2, 3, 4, 5]
    relevant = {1, 3, 5}
    
    print(f"Retrieved documents: {retrieved}")
    print(f"Relevant documents: {relevant}")
    
    p_at_5 = evaluator.precision_at_k(retrieved, relevant, k=5)
    recall = evaluator.recall(retrieved, relevant)
    f1 = evaluator.f_measure(p_at_5, recall)
    
    print(f"\nPrecision@5: {p_at_5:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")


def demo_statistics():
    """Show system statistics."""
    print_section("5. SYSTEM STATISTICS")
    
    indexer = InvertedIndexBuilder()
    stats = indexer.get_collection_stats()
    
    print(f"Total documents: {stats['total_documents']}")
    print(f"Total unique terms: {stats['total_terms']}")
    print(f"Average document length: {stats['avg_doc_length']:.2f} tokens")
    
    # Language distribution
    print("\nDocument distribution by language:")
    from django.db.models import Count
    lang_dist = Document.objects.values('language').annotate(count=Count('id'))
    for item in lang_dist:
        print(f"  {item['language']}: {item['count']} documents")


def main():
    """Run all demos."""
    print("\n" + "="*60)
    print("  IR SEARCH ENGINE - DEMONSTRATION")
    print("="*60)
    
    try:
        demo_preprocessing()
        demo_indexing()
        demo_search()
        demo_evaluation()
        demo_statistics()
        
        print_section("DEMO COMPLETE")
        print("✓ All demonstrations completed successfully!")
        print("\nNext steps:")
        print("  1. Run: python manage.py runserver")
        print("  2. Visit: http://127.0.0.1:8000/")
        print("  3. Try searching with different queries")
        print("  4. Compare VSM vs BM25 results")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        print("\nMake sure you have:")
        print("  1. Run migrations: python manage.py migrate")
        print("  2. Created documents or run: python manage.py create_sample_docs")


if __name__ == '__main__':
    main()
