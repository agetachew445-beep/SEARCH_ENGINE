# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-05-06

### Added
- Initial release of IR Search Engine
- Text preprocessing module with multi-language support
- Inverted index builder with TF-IDF computation
- Vector Space Model (Cosine Similarity) ranking
- BM25 ranking algorithm
- Evaluation metrics (Precision@K, Recall, F-measure)
- Web interface with Bootstrap styling
- Django admin interface for document management
- Management commands (index_docs, create_sample_docs, evaluate_search)
- Support for Amharic, Tigrinya, Afan Oromo, and English
- Comprehensive documentation
- Unit and integration tests
- Sample documents for testing

### Features
- Multi-language tokenization with Ge'ez script support
- Custom stopword lists per language
- Basic stemming functionality
- Position-aware inverted index
- Configurable BM25 parameters (k1, b)
- Snippet extraction with query term highlighting
- Model comparison (VSM vs BM25)
- Evaluation result tracking in database
- Responsive web design
- Admin interface for all models

### Documentation
- README.md - Project overview
- INSTALLATION.md - Setup guide
- USAGE.md - Usage instructions
- DEVELOPER_GUIDE.md - Development documentation
- QUICK_START.md - 5-minute setup
- FEATURES.md - Feature documentation
- CONTRIBUTING.md - Contribution guidelines
- LICENSE - MIT License

### Technical Details
- Django 4.2.7
- Python 3.8+
- SQLite (development) / PostgreSQL (production ready)
- NLTK for NLP utilities
- Scikit-learn for vector operations
- Bootstrap 5.3 for UI

## [Future Releases]

### Planned Features
- Query expansion with synonyms
- Relevance feedback mechanism
- Spell correction
- Auto-complete suggestions
- REST API
- Real-time indexing
- Advanced NLP features
- Machine learning ranking
- Distributed indexing
- Performance optimizations

---

Format based on [Keep a Changelog](https://keepachangelog.com/)
