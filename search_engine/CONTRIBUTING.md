# Contributing Guide

## How to Contribute

This is an educational IR project. Contributions are welcome!

## Areas for Contribution

### 1. Language Support
- Add new language stopwords
- Improve tokenization for specific languages
- Add language-specific stemmers

### 2. Ranking Algorithms
- Implement additional ranking models (e.g., Language Models, Neural IR)
- Optimize existing algorithms
- Add query expansion techniques

### 3. Evaluation
- Add more evaluation metrics (MAP, NDCG, MRR)
- Create comprehensive test query sets
- Implement cross-validation

### 4. User Interface
- Improve search result presentation
- Add advanced search options
- Create visualization dashboards

### 5. Performance
- Optimize indexing speed
- Improve query processing time
- Add caching mechanisms

### 6. Documentation
- Add more code examples
- Create video tutorials
- Translate documentation

## Development Setup

1. Fork the repository
2. Clone your fork
3. Create a virtual environment
4. Install dependencies
5. Create a feature branch
6. Make your changes
7. Run tests
8. Submit a pull request

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic
- Keep functions focused and small

## Testing

Always add tests for new features:

```python
# search/tests.py
class MyFeatureTests(TestCase):
    def test_my_feature(self):
        # Test code here
        pass
```

Run tests:
```bash
python manage.py test
```

## Commit Messages

Use clear, descriptive commit messages:

```
Add BM25 ranking algorithm

- Implement BM25 scoring function
- Add k1 and b parameters
- Update tests
```

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR with clear description

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Questions about the code
- Documentation improvements

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn
- Focus on the code, not the person

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
