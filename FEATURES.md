# Feature Documentation

## Core IR Features

### 1. Text Preprocessing

#### Tokenization
- **Unicode Support**: Full support for Ge'ez script (U+1200–U+137F)
- **Multi-language**: Amharic, Tigrinya, Afan Oromo, English
- **Regex-based**: Efficient pattern matching
- **Case normalization**: Lowercase conversion

#### Stopword Removal
- **Custom lists**: Language-specific stopword files
- **Extensible**: Easy to add new stopwords
- **Configurable**: Per-language stopword sets

#### Stemming
- **Basic stemming**: Suffix removal
- **Extensible**: Can integrate advanced stemmers
- **Language-aware**: Different rules per language

### 2. Indexing

#### Inverted Index
- **Structure**: term → {doc_id: [positions]}
- **Efficient lookup**: O(1) term access
- **Position tracking**: Stores term positions in documents
- **Persistent storage**: Database-backed

#### TF-IDF Computation
- **Term Frequency (TF)**: Raw count of term in document
- **Inverse Document Frequency (IDF)**: log((N+1)/(df+1)) + 1
- **Normalization**: Length-normalized vectors
- **Precomputed**: IDF stored in index

### 3. Ranking Models

#### Vector Space Model (Cosine Similarity)
```
Formula: cos(θ) = (A · B) / (||A|| × ||B||)

Where:
- A = query vector (TF-IDF)
- B = document vector (TF-IDF)
- · = dot product
- ||·|| = vector magnitude
```

**Advantages:**
- Simple and intuitive
- Works well for short queries
- Fast computation

**Use cases:**
- General web search
- Document similarity
- Content recommendation

#### Okapi BM25
```
Formula: Σ IDF(qi) × (f(qi,D) × (k1+1)) / (f(qi,D) + k1×(1-b+b×|D|/avgdl))

Where:
- qi = query term
- f(qi,D) = term frequency in document D
- |D| = document length
- avgdl = average document length
- k1 = term frequency saturation (default: 1.5)
- b = length normalization (default: 0.75)
```

**Advantages:**
- Better handling of term frequency saturation
- Length normalization
- Probabilistic foundation

**Use cases:**
- Long documents
- Varying document lengths
- Academic search

### 4. Evaluation Metrics

#### Precision@K
```
Precision@K = (Relevant docs in top K) / K
```

**Interpretation:**
- Measures accuracy of top results
- Important for user satisfaction
- K=5 typical for web search

#### Recall
```
Recall = (Retrieved relevant docs) / (Total relevant docs)
```

**Interpretation:**
- Measures completeness
- Important for comprehensive search
- Trade-off with precision

#### F-Measure
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

**Interpretation:**
- Harmonic mean of P and R
- Balanced metric
- Single-number summary

## Web Interface Features

### Search Page
- **Clean design**: Bootstrap-based UI
- **Responsive**: Mobile-friendly
- **Fast**: Optimized queries
- **Intuitive**: Simple search box

### Results Display
- **Ranked list**: Sorted by relevance score
- **Snippets**: Context preview with query terms
- **Metadata**: Document info (language, ID, score)
- **Highlighting**: Visual emphasis on results

### Model Selection
- **Toggle**: Switch between VSM and BM25
- **Comparison**: Easy A/B testing
- **Real-time**: Instant model switching

## Admin Interface Features

### Document Management
- **CRUD operations**: Create, Read, Update, Delete
- **Bulk actions**: Process multiple documents
- **Filtering**: By language, type, indexed status
- **Search**: Find documents quickly

### Index Management
- **View entries**: Browse inverted index
- **Statistics**: Document frequency, IDF
- **Debugging**: Inspect postings lists

### Evaluation Tracking
- **Query history**: All evaluated queries
- **Metrics display**: P@5, P@10, Recall
- **Model comparison**: Side-by-side results
- **Export**: Download evaluation data

## Management Commands

### index_docs
**Purpose**: Build or rebuild search index

**Usage:**
```bash
python manage.py index_docs [--rebuild]
```

**Features:**
- Incremental indexing (new docs only)
- Full rebuild option
- Progress reporting
- Error handling

### create_sample_docs
**Purpose**: Generate test documents

**Usage:**
```bash
python manage.py create_sample_docs
```

**Features:**
- 8 IR-related documents
- Diverse content
- Ready to index
- Educational examples

### evaluate_search
**Purpose**: Run evaluation on test queries

**Usage:**
```bash
python manage.py evaluate_search
```

**Features:**
- 10 test queries
- Both ranking models
- Automatic metric calculation
- Database storage

## Language Support

### Supported Languages

#### Amharic (አማርኛ)
- Ge'ez script support
- Custom stopwords
- Unicode normalization

#### Tigrinya (ትግርኛ)
- Ge'ez script support
- Custom stopwords
- Shared script with Amharic

#### Afan Oromo (Afaan Oromoo)
- Latin script
- Custom stopwords
- Tone mark handling

#### English
- Full support
- Comprehensive stopwords
- Standard stemming

### Adding New Languages

1. Create stopword file
2. Add language choice to model
3. Update preprocessing if needed
4. Test with sample documents

## Performance Features

### Optimization
- **Database indexes**: Fast lookups
- **Batch operations**: Efficient bulk processing
- **Caching**: Reduced redundant computation
- **Lazy loading**: On-demand data retrieval

### Scalability
- **Incremental indexing**: Add docs without rebuild
- **Pagination**: Handle large result sets
- **Configurable limits**: Control resource usage
- **Database backend**: SQLite or PostgreSQL

## Security Features

### Input Validation
- **Query sanitization**: Prevent injection
- **File upload validation**: Safe file handling
- **CSRF protection**: Django built-in
- **XSS prevention**: Template escaping

### Access Control
- **Admin authentication**: Login required
- **User permissions**: Role-based access
- **Session management**: Secure sessions

## Extensibility Features

### Plugin Architecture
- **Modular design**: Separate concerns
- **Clear interfaces**: Well-defined APIs
- **Easy customization**: Override methods
- **Configuration**: Settings-based

### API Access
- **Programmatic use**: Import modules
- **Django shell**: Interactive testing
- **Management commands**: Automation
- **REST potential**: Easy to add REST API

## Testing Features

### Unit Tests
- **Preprocessing tests**: Tokenization, stopwords
- **Indexing tests**: Index building, postings
- **Ranking tests**: Both algorithms
- **Evaluation tests**: Metrics calculation

### Integration Tests
- **View tests**: Web interface
- **Model tests**: Database operations
- **Command tests**: Management commands

### Test Coverage
```bash
coverage run --source='.' manage.py test
coverage report
```

## Documentation Features

### Comprehensive Guides
- **README.md**: Project overview
- **INSTALLATION.md**: Setup instructions
- **USAGE.md**: How to use
- **DEVELOPER_GUIDE.md**: Development info
- **QUICK_START.md**: 5-minute setup

### Code Documentation
- **Docstrings**: All functions documented
- **Comments**: Complex logic explained
- **Type hints**: Function signatures
- **Examples**: Usage examples

## Future Enhancement Ideas

### Potential Features
1. **Query expansion**: Synonyms, related terms
2. **Relevance feedback**: Learn from user clicks
3. **Faceted search**: Filter by metadata
4. **Spell correction**: Handle typos
5. **Auto-complete**: Suggest queries
6. **REST API**: External access
7. **Distributed indexing**: Scale horizontally
8. **Real-time indexing**: Instant updates
9. **Advanced NLP**: Named entity recognition
10. **Machine learning**: Learning to rank

### Performance Improvements
1. **Caching layer**: Redis integration
2. **Async processing**: Celery tasks
3. **Index compression**: Reduce storage
4. **Query optimization**: Faster searches
5. **Load balancing**: Multiple servers
