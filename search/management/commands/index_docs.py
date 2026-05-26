"""
python manage.py index_docs [--rebuild]

Builds (or rebuilds) the inverted index for all documents.
"""

from django.core.management.base import BaseCommand
from search.indexing import InvertedIndexBuilder
from search.models import Document, IndexEntry


class Command(BaseCommand):
    help = 'Build / rebuild the inverted index stored in SQLite'

    def add_arguments(self, parser):
        parser.add_argument(
            '--rebuild', action='store_true',
            help='Delete existing index and re-index all documents'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== IR Index Builder ==='))

        if options['rebuild']:
            self.stdout.write('Clearing existing index…')
            IndexEntry.objects.all().delete()
            Document.objects.all().update(is_indexed=False)
            documents = Document.objects.all()
        else:
            documents = Document.objects.filter(is_indexed=False)

        count = documents.count()
        if count == 0:
            self.stdout.write(self.style.WARNING(
                'No documents to index.  '
                'Add documents via admin or run: python manage.py create_sample_docs'
            ))
            return

        self.stdout.write(f'Indexing {count} document(s)…')

        try:
            indexer   = InvertedIndexBuilder()
            num_terms = indexer.build_index(documents)
            self.stdout.write(self.style.SUCCESS(
                f'✓  Indexed {count} documents  |  {num_terms} unique terms'
            ))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'Error: {exc}'))
            raise
