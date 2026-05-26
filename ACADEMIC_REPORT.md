# Academic Report Template

## Information Retrieval System - Project Report

### Student Information
- **Name**: [Your Name]
- **ID**: [Your Student ID]
- **Course**: Information Storage and Retrieval
- **Semester**: [Semester/Year]
- **Institution**: [University Name]

---

## 1. Executive Summary

This project implements a domain-specific web search engine supporting local languages (Amharic, Tigrinya, Afan Oromo) and English. The system demonstrates core IR concepts including text preprocessing, inverted indexing, TF-IDF weighting, and two ranking models (Vector Space Model and BM25).

**Key Achievements:**
- Functional search engine with web interface
- Multi-language support with custom preprocessing
- Two ranking algorithms implemented and compared
- Comprehensive evaluation framework
- Extensible architecture for future enhancements

---

## 2. Introduction

### 2.1 Background
Information Retrieval (IR) systems are essential for accessing relevant information from large document collections. This project addresses the need for search capabilities in local languages, which are often underserved by mainstream search engines.

### 2.2 Objectives
1. Implement core IR algorithms (indexing, ranking, evaluation)
2. Support multiple languages including Ethiopian languages
3. Compare ranking models (VSM vs BM25)
4. Provide user-friendly web interface
5. Evaluate system performance using standard metrics

### 2.3 Scope
- Text-based document search
- Offline indexing, online query processing
- Support for .txt, .pdf, .html documents
- Evaluation using Precision@K and Recall

---

## 3. System Architecture

### 3.1 Overview
The system follows a two-phase IR pipeline:

**Offline Phase:**
1. Document ingestion
2. Text preprocessing
3. Inverted index construction
4. TF-IDF computation

**Online Phase:**
1. Query preprocessing
2. Index lookup
3. Scoring and ranking
4. Result presentation

### 3.2 Technology Stack
- **Backend**: Django 4.2.7 (Python web framework)
- **Database**: SQLite (development), PostgreSQL-ready
- **IR Libraries**: NLTK, Scikit-learn
- **Frontend**: HTML, CSS, Bootstrap 5.3
- **Deployment**: Gunicorn, Nginx-ready

### 3.3 Component Diagram
```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│   Web Interface     │
│  (Django Views)     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Ranking Engine     │
│  (VSM / BM25)       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Inverted Index     │
│  (IndexEntry Model) │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Document Store     │
│  (Document Model)   │
└─────────────────────┘
```

---

## 4. Implementation Details

### 4.1 Text Preprocessing

**Tokenization:**
- Regex-based pattern matching
- Unicode normalization for Ge'ez script
- Support for characters U+1200–U+137F (Ethiopian scripts)

**Stopword Removal:**
- Language-specific stopword lists
- Custom lists for Amharic, Tigrinya, Afan Oromo
- Standard English stopwords

**Stemming:**
- Basic suffix removal algorithm
- Extensible for language-specific stemmers

### 4.2 Indexing

**Inverted Index Structure:**
```
term → [
  {doc_id: 1, term_freq: 3, positions: [5, 12, 45]},
  {doc_id: 5, term_freq: 1, positions: [23]},
  ...
]
```

**TF-IDF Computation:**
- TF: Raw term frequency in document
- IDF: log((N+1)/(df+1)) + 1
- Weight: TF × IDF

### 4.3 Ranking Models

**Vector Space Model (Cosine Similarity):**
```
similarity(q, d) = (q · d) / (||q|| × ||d||)
```

**Advantages:**
- Simple and intuitive
- Fast computation
- Works well for short queries

**BM25:**
```
score(q, d) = Σ IDF(qi) × (f(qi,d) × (k1+1)) / (f(qi,d) + k1×(1-b+b×|d|/avgdl))
```

**Parameters:**
- k1 = 1.5 (term frequency saturation)
- b = 0.75 (length normalization)

**Advantages:**
- Better term frequency saturation
- Document length normalization
- Probabilistic foundation

### 4.4 Evaluation Metrics

**Precision@K:**
```
P@K = |{relevant docs} ∩ {retrieved docs at K}| / K
```

**Recall:**
```
Recall = |{relevant docs} ∩ {retrieved docs}| / |{relevant docs}|
```

**F1-Score:**
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

---

## 5. Experimental Results

### 5.1 Test Setup
- **Document Collection**: 8 sample IR documents
- **Test Queries**: 10 queries covering IR concepts
- **Evaluation**: Precision@5, Precision@10, Recall
- **Models Compared**: VSM (Cosine) vs BM25

### 5.2 Results

#### Table 1: Average Performance Metrics

| Metric          | VSM (Cosine) | BM25   | Winner |
|-----------------|--------------|--------|--------|
| Precision@5     | [Fill in]    | [Fill in] | [Fill in] |
| Precision@10    | [Fill in]    | [Fill in] | [Fill in] |
| Recall          | [Fill in]    | [Fill in] | [Fill in] |
| Avg Query Time  | [Fill in]    | [Fill in] | [Fill in] |

*Note: Run `python manage.py evaluate_search` to generate actual results*

### 5.3 Analysis

**Observations:**
1. [Describe which model performed better]
2. [Discuss query time differences]
3. [Analyze precision vs recall trade-offs]

**Insights:**
- BM25 typically performs better on longer documents
- VSM is faster for short queries
- Both models benefit from good preprocessing

---

## 6. Challenges and Solutions

### 6.1 Multi-language Support
**Challenge**: Supporting Ge'ez script and multiple languages
**Solution**: Unicode normalization and regex patterns for Ethiopian scripts

### 6.2 Index Efficiency
**Challenge**: Fast index lookup for large collections
**Solution**: Database indexing on term field, JSON storage for postings

### 6.3 Snippet Generation
**Challenge**: Extracting relevant snippets with query terms
**Solution**: Position-aware search and context extraction

---

## 7. Conclusions

### 7.1 Achievements
- ✅ Functional search engine with multi-language support
- ✅ Two ranking algorithms implemented
- ✅ Comprehensive evaluation framework
- ✅ User-friendly web interface
- ✅ Extensible architecture

### 7.2 Limitations
- Basic stemming (could use advanced stemmers)
- Limited to text documents
- No query expansion or spell correction
- Single-server deployment

### 7.3 Future Work
1. **Query Expansion**: Add synonym support
2. **Relevance Feedback**: Learn from user interactions
3. **Advanced NLP**: Named entity recognition
4. **Machine Learning**: Learning-to-rank algorithms
5. **Scalability**: Distributed indexing
6. **Real-time**: Incremental index updates

---

## 8. References

1. Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.

2. Baeza-Yates, R., & Ribeiro-Neto, B. (2011). *Modern Information Retrieval*. Addison Wesley.

3. Robertson, S., & Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond. *Foundations and Trends in Information Retrieval*.

4. Salton, G., & McGill, M. J. (1983). *Introduction to Modern Information Retrieval*. McGraw-Hill.

5. Django Documentation. (2024). https://docs.djangoproject.com/

6. NLTK Documentation. (2024). https://www.nltk.org/

---

## 9. Appendices

### Appendix A: Installation Instructions
See [INSTALLATION.md](INSTALLATION.md)

### Appendix B: Usage Guide
See [USAGE.md](USAGE.md)

### Appendix C: Code Structure
See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)

### Appendix D: Test Queries
```
1. information retrieval
2. vector space model
3. tf-idf weighting
4. bm25 ranking
5. text preprocessing
6. inverted index
7. precision recall
8. natural language processing
9. search engine
10. document ranking
```

### Appendix E: Sample Output
[Include screenshots of search interface and results]

---

## Declaration

I declare that this project is my own work and has been completed in accordance with academic integrity guidelines.

**Signature**: ________________
**Date**: ________________

---

*This report template should be customized with your actual results and analysis.*
