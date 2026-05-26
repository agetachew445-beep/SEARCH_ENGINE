# Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 2. Setup Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 3. Add Sample Data
```bash
python manage.py create_sample_docs
python manage.py index_docs
```

### 4. Run Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## First Search

1. Go to http://127.0.0.1:8000/
2. Enter: "information retrieval"
3. Select: "Vector Space Model (Cosine Similarity)"
4. Click "Search"

## Compare Ranking Models

Try the same query with both models:
- **VSM (Cosine Similarity)**: Traditional TF-IDF based
- **BM25**: Probabilistic ranking with length normalization

## Add Your Own Documents

1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Click "Documents" → "Add Document"
4. Fill in title and text
5. Save
6. Run: `python manage.py index_docs`

## Evaluate Performance

```bash
python manage.py evaluate_search
```

View results in admin: http://127.0.0.1:8000/admin/search/evaluationmetric/

## Next Steps

- Read [USAGE.md](USAGE.md) for detailed usage
- Read [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for customization
- Add your own documents and test queries
- Customize stopwords for your language
- Tune BM25 parameters for your corpus

## Common Commands

```bash
# Create sample documents
python manage.py create_sample_docs

# Build index
python manage.py index_docs

# Rebuild entire index
python manage.py index_docs --rebuild

# Run evaluation
python manage.py evaluate_search

# Start server
python manage.py runserver

# Access Django shell
python manage.py shell
```

## Project Structure

```
search_engine/
├── manage.py              # Django CLI
├── search_engine/         # Settings
└── search/                # Main app
    ├── models.py         # Database
    ├── views.py          # Web interface
    ├── preprocessing.py  # Text processing
    ├── indexing.py       # Index builder
    ├── ranking.py        # Search algorithms
    └── evaluation.py     # Metrics
```

## Key Features

✅ Multi-language support (Amharic, Tigrinya, Afan Oromo, English)
✅ Two ranking models (VSM and BM25)
✅ Inverted index with TF-IDF
✅ Evaluation metrics (Precision@K, Recall)
✅ Web interface with Bootstrap
✅ Admin panel for document management
✅ Management commands for automation

## Support

- Check [README.md](README.md) for overview
- Check [INSTALLATION.md](INSTALLATION.md) for detailed setup
- Check [USAGE.md](USAGE.md) for usage examples
- Check [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for development
