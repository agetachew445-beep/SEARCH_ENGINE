# Usage Guide

## Overview

This IR Search Engine supports:
- Multiple languages (Amharic, Tigrinya, Afan Oromo, English)
- Two ranking models (Cosine Similarity and BM25)
- Document management via admin interface
- Performance evaluation metrics

## Basic Usage

### 1. Adding Documents

#### Via Admin Interface

1. Go to http://127.0.0.1:8000/admin/
2. Login with your superuser credentials
3. Click on "Documents"
4. Click "Add Document"
5. Fill in:
   - Title
   - Raw text (or upload file)
   - Language
   - Document type
6. Save

#### Via Django Shell

```python
python manage.py shell

from search.models import Document
from django.utils import timezone

doc = Document.objects.create(
    title="My Document",
    raw_text="Document content here...",
    language="english",
    pub_date=timezone.now()
)
```

### 2. Building the Index

After adding documents, build the index:

```bash
# Index new documents only
python manage.py index_docs

# Rebuild entire index
python manage.py index_docs --rebuild
```

### 3. Searching

#### Web Interface

1. Go to http://127.0.0.1:8000/
2. Enter your query
3. Select ranking model (VSM or BM25)
4. Click "Search"

#### Programmatically

```python
from search.ranking import RankingEngine

# Using Cosine Similarity
engine = RankingEngine(ranking_model='cosine')
results = engine.search("information retrieval", top_k=10)

# Using BM25
engine = RankingEngine(ranking_model='bm25')
results = engine.search("information retrieval", top_k=10)

# Results format: [(doc_id, score), ...]
for doc_id, score in results:
    print(f"Document {doc_id}: {score:.4f}")
```

### 4. Evaluation

#### Run Evaluation

```bash
python manage.py evaluate_search
```

This compares Cosine Similarity vs BM25 on test queries.

#### View Results

1. Go to http://127.0.0.1:8000/admin/
2. Click on "Evaluation metrics"
3. View Precision@5, Precision@10, Recall for each query

#### Custom Evaluation

```python
from search.evaluation import IREvaluator

evaluator = IREvaluator()

# Define test case
test_queries = [
    {
        'query': 'information retrieval',
        'relevant_docs': [1, 2, 3]  # Document IDs
    }
]

# Compare models
comparison = evaluator.compare_ranking_models(test_queries)

print(comparison['cosine']['avg_precision_at_5'])
print(comparison['bm25']['avg_precision_at_5'])
```

## Advanced Features

### Custom Stopwords

Edit stopword files in `search/stopwords/`:
- `amharic.txt`
- `tigrinya.txt`
- `afan_oromo.txt`
- `english.txt`

Add one stopword per line.

### Adjusting BM25 Parameters

In `search/ranking.py`, modify:

```python
self.k1 = 1.5  # Term frequency saturation (1.2-2.0)
self.b = 0.75  # Length normalization (0-1)
```

Or in `settings.py`:

```python
IR_SETTINGS = {
    'BM25_K1': 1.5,
    'BM25_B': 0.75,
}
```

### Snippet Length

In `settings.py`:

```python
IR_SETTINGS = {
    'SNIPPET_LENGTH': 200,  # Characters
}
```

### Maximum Results

In `settings.py`:

```python
IR_SETTINGS = {
    'MAX_RESULTS': 50,
}
```

## Management Commands

### index_docs
Build or rebuild the search index.

```bash
python manage.py index_docs [--rebuild]
```

### create_sample_docs
Create sample documents for testing.

```bash
python manage.py create_sample_docs
```

### evaluate_search
Run evaluation on test queries.

```bash
python manage.py evaluate_search
```

## API Usage (Programmatic)

### Text Preprocessing

```python
from search.preprocessing import TextPreprocessor

preprocessor = TextPreprocessor(language='english')

# Tokenize
tokens = preprocessor.tokenize("Information retrieval system")

# Remove stopwords
filtered = preprocessor.remove_stopwords(tokens)

# Full preprocessing
processed = preprocessor.preprocess("Information retrieval system")
```

### Indexing

```python
from search.indexing import InvertedIndexBuilder

indexer = InvertedIndexBuilder()

# Build index
indexer.build_index()

# Get term postings
postings = indexer.get_term_postings("information")

# Get document vector
vector = indexer.get_document_vector(doc_id=1)

# Get collection stats
stats = indexer.get_collection_stats()
```

### Ranking

```python
from search.ranking import RankingEngine

# Cosine Similarity
engine = RankingEngine(ranking_model='cosine')
results = engine.cosine_similarity_search("query", top_k=10)

# BM25
engine = RankingEngine(ranking_model='bm25')
results = engine.bm25_search("query", top_k=10)
```

## Tips for Best Results

1. **Index regularly**: After adding documents, rebuild the index
2. **Use appropriate language**: Set correct language for documents
3. **Test both models**: Try both Cosine Similarity and BM25
4. **Adjust parameters**: Tune BM25 k1 and b for your corpus
5. **Add stopwords**: Customize stopword lists for your domain
6. **Evaluate**: Use evaluation metrics to measure performance

## Common Workflows

### Adding New Language Support

1. Create stopword file: `search/stopwords/new_language.txt`
2. Add language choice in `models.py`:
   ```python
   ('new_language', 'New Language')
   ```
3. Update preprocessing if needed
4. Run migrations: `python manage.py makemigrations && python manage.py migrate`

### Bulk Document Import

```python
import csv
from search.models import Document

with open('documents.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        Document.objects.create(
            title=row['title'],
            raw_text=row['text'],
            language=row['language']
        )
```

### Export Search Results

```python
import csv
from search.ranking import RankingEngine
from search.models import Document

engine = RankingEngine(ranking_model='cosine')
results = engine.search("query", top_k=50)

with open('results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Rank', 'Document ID', 'Title', 'Score'])
    
    for rank, (doc_id, score) in enumerate(results, 1):
        doc = Document.objects.get(id=doc_id)
        writer.writerow([rank, doc_id, doc.title, score])
```
