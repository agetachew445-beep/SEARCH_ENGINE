# Developer Guide

## Architecture Overview

### Two-Phase IR Pipeline

#### Offline Phase (Indexing)
1. Document ingestion
2. Text preprocessing (tokenization, stopword removal, stemming)
3. Inverted index construction
4. TF-IDF weight computation

#### Online Phase (Query Processing)
1. Query preprocessing
2. Term lookup in inverted index
3. Scoring (Cosine Similarity or BM25)
4. Result ranking and retrieval

## Core Components

### 1. Text Preprocessing (`preprocessing.py`)

**TextPreprocessor Class**
- Handles multiple languages (Amharic, Tigrinya, Afan Oromo, English)
- Unicode normalization for Ge'ez script
- Tokenization with regex patterns
- Stopword removal
- Basic stemming

**Key Methods:**
- `tokenize(text)`: Split text into tokens
- `remove_stopwords(tokens)`: Filter stopwords
- `stem(token)`: Reduce to root form
- `preprocess(text)`: Complete pipeline

### 2. Indexing (`indexing.py`)

**InvertedIndexBuilder Class**
- Builds inverted index: term → {doc_id: [positions]}
- Computes TF-IDF weights
- Stores in database (IndexEntry model)

**Key Methods:**
- `build_index(documents)`: Build index from documents
- `get_term_postings(term)`: Retrieve postings list
- `get_document_vector(doc_id)`: Get TF-IDF vector
- `get_collection_stats()`: Collection statistics

### 3. Ranking (`ranking.py`)

**RankingEngine Class**
- Implements VSM and BM25 ranking

**Cosine Similarity (VSM):**
```
similarity = (query_vector · doc_vector) / (|query_vector| × |doc_vector|)
```

**BM25:**
```
score = Σ IDF(qi) × (f(qi,D) × (k1+1)) / (f(qi,D) + k1×(1-b+b×|D|/avgdl))
```

**Key Methods:**
- `search(query, top_k)`: Main search interface
- `cosine_similarity_search()`: VSM ranking
- `bm25_search()`: BM25 ranking

### 4. Evaluation (`evaluation.py`)

**IREvaluator Class**
- Computes IR metrics

**Metrics:**
- Precision@K: Relevant docs in top K / K
- Recall: Retrieved relevant / Total relevant
- F-measure: Harmonic mean of P and R

**Key Methods:**
- `precision_at_k(retrieved, relevant, k)`
- `recall(retrieved, relevant)`
- `evaluate_query(query, relevant_docs)`
- `compare_ranking_models(test_queries)`

## Database Models

### Document
```python
- title: CharField
- raw_text: TextField
- processed_text: TextField
- language: CharField (choices)
- doc_type: CharField (txt/pdf/html)
- is_indexed: BooleanField
- pub_date: DateTimeField
```

### IndexEntry
```python
- term: CharField (unique, indexed)
- document_frequency: IntegerField
- idf: FloatField
- postings_list: TextField (JSON)
```

### EvaluationMetric
```python
- query: CharField
- ranking_model: CharField
- precision_at_5: FloatField
- precision_at_10: FloatField
- recall: FloatField
- query_time: FloatField
```

## Extending the System

### Adding New Language

1. Create stopword file:
```bash
touch search/stopwords/new_language.txt
```

2. Update models.py:
```python
language = models.CharField(
    choices=[
        ...
        ('new_language', 'New Language'),
    ]
)
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Custom Ranking Algorithm

1. Add method to RankingEngine:
```python
def custom_ranking(self, query, top_k=50):
    # Your algorithm here
    return results
```

2. Update search method:
```python
def search(self, query, top_k=50):
    if self.ranking_model == 'custom':
        return self.custom_ranking(query, top_k)
```

### Adding Document Formats

1. Install parser (e.g., python-docx for DOCX)
2. Add parsing logic in admin or management command
3. Extract text and save to Document.raw_text

## Performance Optimization

### Indexing
- Batch database operations
- Use bulk_create() for IndexEntry
- Cache frequently accessed data

### Search
- Limit postings list size
- Use database indexes
- Cache IDF values
- Implement query caching

### Database
- Add indexes on frequently queried fields
- Use select_related() and prefetch_related()
- Consider PostgreSQL for production

## Testing

### Unit Tests
```python
from django.test import TestCase
from search.preprocessing import TextPreprocessor

class PreprocessingTests(TestCase):
    def test_tokenization(self):
        preprocessor = TextPreprocessor()
        tokens = preprocessor.tokenize("test text")
        self.assertEqual(tokens, ['test', 'text'])
```

### Integration Tests
```python
from django.test import TestCase
from search.models import Document
from search.indexing import InvertedIndexBuilder

class IndexingTests(TestCase):
    def test_index_building(self):
        doc = Document.objects.create(
            title="Test",
            raw_text="test document"
        )
        indexer = InvertedIndexBuilder()
        indexer.build_index()
        # Assert index created
```

## Deployment

### Production Settings

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'search_db',
        'USER': 'search_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Using Gunicorn

```bash
gunicorn search_engine.wsgi:application --bind 0.0.0.0:8000
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/staticfiles/;
    }
}
```

## Troubleshooting

### Index not updating
```bash
python manage.py index_docs --rebuild
```

### Slow searches
- Check database indexes
- Reduce MAX_RESULTS
- Optimize postings list storage

### Memory issues
- Process documents in batches
- Limit postings list size
- Use database pagination

## Best Practices

1. **Always preprocess consistently**: Use same preprocessing for indexing and querying
2. **Rebuild index after changes**: Changes to preprocessing require reindexing
3. **Monitor performance**: Use evaluation metrics regularly
4. **Version control**: Track changes to stopwords and parameters
5. **Document customizations**: Comment code changes clearly
