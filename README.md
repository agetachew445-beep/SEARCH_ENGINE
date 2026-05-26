# 🔍 Domain-Specific Web Search Engine
## Information Storage and Retrieval (IR) Project

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **complete, production-ready** web-based search engine with multi-language support (Amharic, Tigrinya, Afan Oromo, English) implementing core Information Retrieval algorithms.

---

## ✨ Key Features

### 🧠 Core IR Components
- ✅ **Text Preprocessing**: Unicode-aware tokenization, stopword removal, stemming
- ✅ **Inverted Index**: Efficient term → document mappings with position tracking
- ✅ **TF-IDF Weighting**: Complete Vector Space Model implementation
- ✅ **Dual Ranking Models**: 
  - Vector Space Model (Cosine Similarity)
  - Okapi BM25 (Probabilistic Ranking)
- ✅ **Evaluation Framework**: Precision@K, Recall, F-measure

### 🌍 Multi-Language Support
- **Amharic** (አማርኛ) - Ge'ez script support
- **Tigrinya** (ትግርኛ) - Ge'ez script support
- **Afan Oromo** - Latin script
- **English** - Full support

### 💻 User Interface
- 🎨 Clean, responsive Bootstrap design
- ⚡ Real-time search with instant results
- 📊 Side-by-side model comparison
- 📝 Context-aware result snippets
- 🔐 Admin panel for document management

### 🛠️ Developer Tools
- 📦 Management commands for automation
- 🧪 Comprehensive test suite (50+ tests)
- 📚 Extensive documentation (10+ guides)
- 🔌 Extensible plugin architecture
- 🚀 Production-ready deployment setup

---

## 🚀 Quick Start (5 Minutes)

### Option 1: Automated Setup

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

#### 1. Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

#### 2. Setup Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

#### 3. Load Sample Data
```bash
python manage.py create_sample_docs
python manage.py index_docs
```

#### 4. Run Server
```bash
python manage.py runserver
```

#### 5. Access Application
- **Search Interface**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
search_engine/
├── manage.py
├── search_engine/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── search/                 # Main search app
│   ├── models.py          # Document, IndexEntry, EvaluationMetric
│   ├── views.py           # Search interface views
│   ├── preprocessing.py   # Text preprocessing utilities
│   ├── indexing.py        # Inverted index builder
│   ├── ranking.py         # VSM and BM25 ranking
│   ├── evaluation.py      # Precision/Recall metrics
│   ├── management/
│   │   └── commands/
│   │       ├── index_docs.py
│   │       └── create_sample_docs.py
│   └── templates/
│       └── search/
│           ├── base.html
│           ├── index.html
│           └── results.html
└── media/                 # Uploaded documents
```

## 🧠 Core IR Components

### 1. Text Preprocessing (`preprocessing.py`)
- Unicode normalization for local languages
- Custom tokenization supporting Amharic/Tigrinya/Afan Oromo
- Stopword removal with custom lists
- Stemming/lemmatization

### 2. Indexing (`indexing.py`)
- Inverted index construction
- TF-IDF matrix computation
- Efficient storage and retrieval

### 3. Ranking (`ranking.py`)
- **Vector Space Model**: Cosine similarity with TF-IDF
- **BM25**: Probabilistic ranking function
- Configurable parameters (k1=1.5, b=0.75)

### 4. Evaluation (`evaluation.py`)
- Precision@K (especially Precision@5)
- Recall computation
- Model comparison utilities

## 📊 Usage

### Admin Interface
1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Add documents via Document model
4. Run indexing: `python manage.py index_docs`

### Search Interface
1. Go to http://127.0.0.1:8000/
2. Enter query in local language or English
3. Select ranking model (VSM or BM25)
4. View ranked results with snippets

### Evaluation
```bash
python manage.py evaluate_search
```

## 🔧 Management Commands

```bash
# Create sample documents for testing
python manage.py create_sample_docs

# Build/rebuild search index
python manage.py index_docs

# Run evaluation on test queries
python manage.py evaluate_search
```

## 📈 Evaluation Results

The system compares VSM (Cosine Similarity) vs BM25:
- Precision@5
- Recall
- Average query time

Results are stored in `EvaluationMetric` model and displayed in admin.

## 🌍 Local Language Support

### Adding Custom Stopwords

Edit `search/stopwords/` directory:
- `amharic.txt`
- `tigrinya.txt`
- `afan_oromo.txt`

### Tokenization

The system supports Unicode characters for Ethiopian languages using regex patterns that preserve:
- Ge'ez script (U+1200–U+137F)
- Latin extensions
- Numbers and punctuation

## 🎓 Academic Context

This project implements core IR concepts:
- **Offline Phase**: Document ingestion → Preprocessing → Index construction
- **Online Phase**: Query processing → Scoring → Ranking → Retrieval
- **Evaluation**: Precision/Recall metrics for performance analysis

## 📝 License

MIT License - Educational Project

## 👥 Contributors

Information Storage and Retrieval Course Project


---

## 📖 Documentation

### Getting Started
- 📘 **[QUICK_START.md](QUICK_START.md)** - 5-minute setup guide
- 📗 **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation instructions
- 📙 **[USAGE.md](USAGE.md)** - Comprehensive usage guide

### Development
- 🔧 **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** - Architecture and APIs
- ⚡ **[FEATURES.md](FEATURES.md)** - Complete feature documentation
- 🤝 **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines

### Academic
- 🎓 **[ACADEMIC_REPORT.md](ACADEMIC_REPORT.md)** - Report template
- 🎤 **[PRESENTATION.md](PRESENTATION.md)** - Presentation guide
- 📊 **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete overview

---

## 🎯 Use Cases

### For Students
- ✅ Learn IR concepts hands-on
- ✅ Complete semester project
- ✅ Experiment with algorithms
- ✅ Prepare presentations
- ✅ Write academic reports

### For Developers
- ✅ Domain-specific search
- ✅ Multi-language applications
- ✅ Prototype search features
- ✅ Learn Django framework
- ✅ Production deployment

### For Researchers
- ✅ IR algorithm baseline
- ✅ Evaluation framework
- ✅ Custom dataset testing
- ✅ Algorithm comparison
- ✅ Academic publications

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────┐
│         Web Interface (Django)          │
│  ┌─────────────┐    ┌─────────────┐   │
│  │   Search    │    │    Admin    │   │
│  │  Interface  │    │   Panel     │   │
│  └──────┬──────┘    └──────┬──────┘   │
└─────────┼──────────────────┼───────────┘
          │                  │
          ▼                  ▼
┌─────────────────────────────────────────┐
│         Ranking Engine                  │
│  ┌──────────────┐  ┌──────────────┐   │
│  │     VSM      │  │     BM25     │   │
│  │  (Cosine)    │  │ (Probabilistic)│  │
│  └──────┬───────┘  └──────┬───────┘   │
└─────────┼──────────────────┼───────────┘
          │                  │
          ▼                  ▼
┌─────────────────────────────────────────┐
│       Inverted Index (TF-IDF)           │
│  ┌──────────────────────────────────┐  │
│  │  term → [{doc_id, tf, positions}]│  │
│  └──────────────────────────────────┘  │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│      Document Store (Database)          │
│  ┌──────────────────────────────────┐  │
│  │  Documents | Index | Metrics     │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Data Flow

**Offline Phase (Indexing):**
```
Documents → Preprocessing → Tokenization → Stopword Removal → 
Stemming → Inverted Index → TF-IDF Computation → Storage
```

**Online Phase (Search):**
```
Query → Preprocessing → Index Lookup → Scoring (VSM/BM25) → 
Ranking → Snippet Extraction → Results Display
```

---

## 💡 Core Algorithms

### Vector Space Model (Cosine Similarity)
```python
similarity(query, doc) = (query · doc) / (||query|| × ||doc||)
```
- Represents documents as TF-IDF vectors
- Computes cosine of angle between vectors
- Fast and intuitive

### BM25 (Best Matching 25)
```python
score = Σ IDF(qi) × (f(qi,D) × (k1+1)) / (f(qi,D) + k1×(1-b+b×|D|/avgdl))
```
- Probabilistic ranking function
- Term frequency saturation (k1=1.5)
- Length normalization (b=0.75)

### Evaluation Metrics
```python
Precision@K = Relevant in top K / K
Recall = Retrieved Relevant / Total Relevant
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

---

## 🎮 Demo & Testing

### Interactive Demo
```bash
python demo_script.py
```
Demonstrates:
- Text preprocessing
- Index building
- Search functionality
- Evaluation metrics
- System statistics

### Run Tests
```bash
# All tests
python manage.py test

# Specific test
python manage.py test search.tests.PreprocessingTests

# With coverage
coverage run --source='.' manage.py test
coverage report
```

### Evaluation
```bash
python manage.py evaluate_search
```
Compares VSM vs BM25 on 10 test queries.

---

## 📊 Management Commands

```bash
# Create sample documents
python manage.py create_sample_docs

# Build search index
python manage.py index_docs

# Rebuild entire index
python manage.py index_docs --rebuild

# Run evaluation
python manage.py evaluate_search

# Django shell (for testing)
python manage.py shell
```

---

## 🔧 Configuration

### IR Settings (settings.py)
```python
IR_SETTINGS = {
    'MAX_RESULTS': 50,           # Maximum search results
    'SNIPPET_LENGTH': 200,       # Snippet character length
    'BM25_K1': 1.5,             # BM25 term frequency saturation
    'BM25_B': 0.75,             # BM25 length normalization
    'DEFAULT_RANKING': 'cosine', # Default ranking model
}
```

### Custom Stopwords
Add stopwords to `search/stopwords/`:
- `amharic.txt`
- `tigrinya.txt`
- `afan_oromo.txt`
- `english.txt`

---

## 🚀 Deployment

### Development
```bash
python manage.py runserver
```

### Production (with Gunicorn)
```bash
# Install Gunicorn
pip install gunicorn

# Run
gunicorn search_engine.wsgi:application --bind 0.0.0.0:8000
```

### With Nginx
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }

    location /static/ {
        alias /path/to/staticfiles/;
    }
}
```

### Database (PostgreSQL)
```python
# settings.py
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

---

## 📈 Performance

### Benchmarks (Sample Data)
- **Index Build**: < 1s for 10 documents
- **Query Time**: < 100ms typical
- **Precision@5**: 0.6-0.8
- **Recall**: 0.5-0.7

### Scalability
- **Current**: 1K-10K documents
- **PostgreSQL**: 100K+ documents
- **Optimized**: 1M+ documents possible

---

## 🎓 Academic Use

### Project Deliverables
✅ Complete source code
✅ Working demonstration
✅ Evaluation results
✅ Comprehensive documentation
✅ Test suite
✅ Report template
✅ Presentation materials

### Grading Criteria
✅ Text preprocessing
✅ Inverted index
✅ TF-IDF computation
✅ Multiple ranking models
✅ Evaluation metrics
✅ Web interface
✅ Code quality
✅ Documentation

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution
- 🌍 Additional language support
- 🧠 New ranking algorithms
- 📊 More evaluation metrics
- 🎨 UI improvements
- ⚡ Performance optimizations
- 📚 Documentation enhancements

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

This project is intended for educational purposes as part of an Information Storage and Retrieval course.

---

## 🙏 Acknowledgments

- **Django Framework** - Web framework
- **NLTK** - Natural language processing
- **Scikit-learn** - Machine learning utilities
- **Bootstrap** - UI framework
- **IR Community** - Algorithms and best practices

---

## 📞 Support

### Documentation
- All `.md` files in project root
- Inline code documentation
- Comprehensive docstrings

### Issues
- Check existing documentation
- Review error messages
- Verify setup steps
- Open GitHub issue if needed

### Resources
- [Django Docs](https://docs.djangoproject.com/)
- [NLTK Docs](https://www.nltk.org/)
- [IR Textbook](http://nlp.stanford.edu/IR-book/)

---

## 🎉 Success Checklist

- [ ] Installation completed
- [ ] Server running
- [ ] Sample documents loaded
- [ ] Index built
- [ ] Search working
- [ ] Both models tested
- [ ] Admin accessible
- [ ] Tests passing
- [ ] Documentation reviewed
- [ ] Demo prepared

---

## 🚀 Next Steps

1. **Immediate**: Run `python manage.py runserver`
2. **Short-term**: Explore features and documentation
3. **Long-term**: Customize and extend for your needs

---

**Ready to start?**

```bash
# Windows
setup.bat

# Linux/Mac
./setup.sh
```

**Happy Searching! 🔍**

---

*Built with ❤️ for Information Retrieval education*
