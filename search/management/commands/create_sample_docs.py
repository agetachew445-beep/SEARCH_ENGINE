"""
Management command to create sample documents for testing.
Usage: python manage.py create_sample_docs
"""
from django.core.management.base import BaseCommand
from search.models import Document
from django.utils import timezone


class Command(BaseCommand):
    help = 'Create sample documents for testing the search engine'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample documents...')

        sample_docs = [
            {
                'title': 'Introduction to Information Retrieval',
                'raw_text': (
                    'Information retrieval is the process of obtaining information '
                    'system resources that are relevant to an information need from a collection '
                    'of those resources. Searches can be based on full-text or other content-based '
                    'indexing. Information retrieval is the science of searching for information '
                    'in a document, searching for documents themselves, and also searching for '
                    'metadata that describe data, and for databases of texts, images or sounds.'
                ),
                'language': 'english',
            },
            {
                'title': 'Vector Space Model in IR',
                'raw_text': (
                    'The vector space model is an algebraic model for representing '
                    'text documents as vectors of identifiers. It is used in information filtering, '
                    'information retrieval, indexing and relevancy rankings. Documents are '
                    'represented as vectors. Each dimension corresponds to a separate term. '
                    'If a term occurs in the document, its value in the vector is non-zero.'
                ),
                'language': 'english',
            },
            {
                'title': 'TF-IDF Weighting Scheme',
                'raw_text': (
                    'TF-IDF stands for term frequency-inverse document frequency. '
                    'It is a numerical statistic that reflects how important a word is to a '
                    'document in a collection. The tf-idf value increases proportionally to '
                    'the number of times a word appears in the document and is offset by the '
                    'number of documents in the corpus that contain the word.'
                ),
                'language': 'english',
            },
            {
                'title': 'BM25 Ranking Function',
                'raw_text': (
                    'BM25 is a ranking function used by search engines to estimate '
                    'the relevance of documents to a given search query. It is based on the '
                    'probabilistic retrieval framework. BM25 is a bag-of-words retrieval function '
                    'that ranks documents based on the query terms appearing in each document.'
                ),
                'language': 'english',
            },
            {
                'title': 'Natural Language Processing',
                'raw_text': (
                    'Natural language processing is a subfield of linguistics, '
                    'computer science, and artificial intelligence concerned with the interactions '
                    'between computers and human language. NLP is used to apply machine learning '
                    'algorithms to text and speech. Common NLP tasks include tokenization, '
                    'stemming, lemmatization, and named entity recognition.'
                ),
                'language': 'english',
            },
            {
                'title': 'Text Preprocessing Techniques',
                'raw_text': (
                    'Text preprocessing is an essential step in natural language processing. '
                    'It includes tokenization, which breaks text into words or tokens. '
                    'Stopword removal eliminates common words that do not carry much meaning. '
                    'Stemming reduces words to their root form. These techniques help improve '
                    'the quality of text analysis and information retrieval.'
                ),
                'language': 'english',
            },
            {
                'title': 'Inverted Index Structure',
                'raw_text': (
                    'An inverted index is a database index storing a mapping from '
                    'content to its locations in a document or set of documents. It is the most '
                    'popular data structure used in document retrieval systems. The inverted index '
                    'maps terms to the documents that contain them. This allows for fast full-text searches.'
                ),
                'language': 'english',
            },
            {
                'title': 'Evaluation Metrics in IR',
                'raw_text': (
                    'Precision and recall are fundamental metrics for evaluating '
                    'information retrieval systems. Precision measures the fraction of retrieved '
                    'documents that are relevant. Recall measures the fraction of relevant '
                    'documents that are retrieved. F-measure combines precision and recall into '
                    'a single metric.'
                ),
                'language': 'english',
            },
        ]

        created_count = 0
        for doc_data in sample_docs:
            doc, created = Document.objects.get_or_create(
                title=doc_data['title'],
                defaults={
                    'raw_text': doc_data['raw_text'],
                    'language': doc_data['language'],
                    'pub_date': timezone.now(),
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'  Created: {doc.title}')
            else:
                self.stdout.write(f'  Already exists: {doc.title}')

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} new documents!')
        )
        self.stdout.write(
            self.style.WARNING('\nNext step: Run "python manage.py index_docs" to build the index.')
        )
