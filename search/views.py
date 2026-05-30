"""
Views for the IR Search Engine.

  /              → home (public)
  /search/       → search results (public)
  /document/<id> → document detail (public)
  /login/        → admin login
  /logout/       → logout
  /upload/       → add documents  [admin only]
  /documents/    → list documents [admin only]
  /delete/<id>/  → delete doc     [admin only]
  /stats/        → JSON stats     (public)
"""

import time
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.views.decorators.http import require_POST

from .models import Document, IndexEntry, SearchLog
from .ranking import RankingEngine
from .preprocessing import extract_snippet, TextPreprocessor, detect_language
from .indexing import InvertedIndexBuilder
from .crawler import WebPageFetcher
from .ai_features import (
    DocumentSummarizer, ConceptRetriever,
    RelatedDocumentFinder, QueryExpander, ReadabilityScorer
)


# ── helper: protect admin views ───────────────────────────────────────────
def _admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_staff):
            return redirect(f'/login/?next={request.path}')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ── AUTH ──────────────────────────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('search:index')
    error = None
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username', '').strip(),
            password=request.POST.get('password', ''),
        )
        if user and user.is_staff:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        error = 'Invalid username or password.'
    return render(request, 'search/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('search:index')


# ── PUBLIC ────────────────────────────────────────────────────────────────
def index(request):
    return render(request, 'search/index.html')


def search_view(request):
    query         = request.GET.get('q', '').strip()
    ranking_model = request.GET.get('model', 'cosine')
    if ranking_model not in ('cosine', 'bm25'):
        ranking_model = 'cosine'

    context = {
        'query': query, 'ranking_model': ranking_model,
        'results': [], 'query_time': '0.000', 'total_results': 0,
        'expanded_terms': [],
    }
    if not query:
        return render(request, 'search/results.html', context)

    t0      = time.time()
    engine  = RankingEngine(ranking_model=ranking_model)

    # Query expansion
    expander       = QueryExpander()
    expanded_terms = expander.expand_query(query, max_expansions=3)

    # Search with original query
    ranked  = engine.search(query, top_k=settings.IR_SETTINGS.get('MAX_RESULTS', 50))

    # If few results, also search with expanded query
    if len(ranked) < 3 and expanded_terms:
        expanded_query = query + ' ' + ' '.join(expanded_terms)
        extra_ranked   = engine.search(expanded_query, top_k=10)
        existing_ids   = {doc_id for doc_id, _ in ranked}
        for doc_id, score in extra_ranked:
            if doc_id not in existing_ids:
                ranked.append((doc_id, score * 0.8))  # slight penalty

    elapsed = time.time() - t0

    preprocessor = TextPreprocessor()
    query_terms  = preprocessor.preprocess(query, apply_stemming=False)
    snippet_len  = settings.IR_SETTINGS.get('SNIPPET_LENGTH', 250)

    results = []
    for doc_id, score in ranked:
        try:
            doc = Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            continue
        results.append({
            'id':       doc.id,
            'title':    doc.title,
            'snippet':  extract_snippet(doc.raw_text, query_terms, snippet_len),
            'summary':  doc.summary[:200] + '…' if doc.summary and len(doc.summary) > 200 else doc.summary,
            'concepts': doc.get_concepts_list()[:4],
            'score':    round(score, 4),
            'url':      doc.url or '',
            'language': doc.get_language_display(),
            'pub_date': doc.pub_date,
        })

    SearchLog.objects.create(
        query=query, ranking_model=ranking_model,
        num_results=len(results), query_time=elapsed,
    )

    context.update({
        'results':        results,
        'query_time':     f'{elapsed:.3f}',
        'total_results':  len(results),
        'expanded_terms': expanded_terms,
    })
    return render(request, 'search/results.html', context)


def document_detail(request, doc_id):
    """Full document view with AI features."""
    doc   = get_object_or_404(Document, id=doc_id)
    query = request.GET.get('q', '')

    # AI features
    summarizer    = DocumentSummarizer()
    concept_ret   = ConceptRetriever()
    related_finder = RelatedDocumentFinder()
    readability   = ReadabilityScorer()

    # Generate summary if not already stored
    if not doc.summary:
        doc.summary = summarizer.summarize(doc.raw_text, num_sentences=3,
                                           language=doc.language)
        doc.save(update_fields=['summary'])

    # Get concepts
    concepts = doc.get_concepts_list()
    if not concepts:
        concepts = concept_ret.get_concepts(doc.raw_text, top_k=8)
        doc.set_concepts_list(concepts)
        doc.save(update_fields=['concepts'])

    # Related documents
    related_docs = related_finder.find_related(doc_id, top_k=4)

    # Readability
    readability_info = readability.score(doc.raw_text, doc.language)

    return render(request, 'search/document_detail.html', {
        'doc':             doc,
        'query':           query,
        'concepts':        concepts,
        'related_docs':    related_docs,
        'readability':     readability_info,
    })


def stats_view(request):
    indexer = InvertedIndexBuilder()
    stats   = indexer.get_collection_stats()
    recent  = list(
        SearchLog.objects
        .values('query', 'ranking_model', 'num_results', 'searched_at')
        .order_by('-searched_at')[:5]
    )
    return JsonResponse({
        'total_documents': stats['total_documents'],
        'total_terms':     stats['total_terms'],
        'avg_doc_length':  round(stats['avg_doc_length'], 1),
        'recent_queries':  recent,
    })


# ── ADMIN-ONLY ────────────────────────────────────────────────────────────
@_admin_required
def crawl_view(request):
    """Web crawler — fetch a URL and add it as a document."""
    stats = InvertedIndexBuilder().get_collection_stats()

    examples = [
        {'flag': '🌐', 'title': 'Information Retrieval - Wikipedia',
         'url': 'https://en.wikipedia.org/wiki/Information_retrieval'},
        {'flag': '🌐', 'title': 'TF-IDF - Wikipedia',
         'url': 'https://en.wikipedia.org/wiki/Tf%E2%80%93idf'},
        {'flag': '🌐', 'title': 'BM25 - Wikipedia',
         'url': 'https://en.wikipedia.org/wiki/Okapi_BM25'},
        {'flag': '🇪🇹', 'title': 'Ethiopia - Wikipedia',
         'url': 'https://en.wikipedia.org/wiki/Ethiopia'},
        {'flag': '🌐', 'title': 'Natural Language Processing - Wikipedia',
         'url': 'https://en.wikipedia.org/wiki/Natural_language_processing'},
    ]

    if request.method == 'POST':
        url      = request.POST.get('url', '').strip()
        language = request.POST.get('language', 'auto')
        title    = request.POST.get('title', '').strip()

        if not url:
            messages.error(request, 'URL is required.')
        else:
            fetcher = WebPageFetcher()
            page    = fetcher.fetch(url)

            if page and page.get('error'):
                messages.error(request, f"Crawl failed: {page['error']}")
            elif page:
                detected_lang = page['language'] if language == 'auto' else language
                doc_title     = title or page['title'] or url

                doc = Document.objects.create(
                    title    = doc_title,
                    raw_text = page['text'],
                    url      = page['url'],
                    language = detected_lang,
                    doc_type = 'html',
                )
                InvertedIndexBuilder().build_index(
                    Document.objects.filter(id=doc.id)
                )
                messages.success(
                    request,
                    f'✅ Crawled and indexed: "{doc_title}" '
                    f'({page["word_count"]} words, language: {detected_lang})'
                )
                return redirect('search:documents')
            else:
                messages.error(request, 'Failed to fetch the URL.')

    return render(request, 'search/crawl.html', {'stats': stats, 'examples': examples})


# ── ADMIN-ONLY ────────────────────────────────────────────────────────────
@_admin_required
def upload_view(request):
    stats = InvertedIndexBuilder().get_collection_stats()

    if request.method == 'POST':
        title         = request.POST.get('title', '').strip()
        language      = request.POST.get('language', 'english')
        raw_text      = request.POST.get('raw_text', '').strip()
        url           = request.POST.get('url', '').strip()
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            ext     = os.path.splitext(uploaded_file.name)[1].lower()
            content = uploaded_file.read()
            if ext == '.txt':
                raw_text = content.decode('utf-8', errors='ignore')
                if not title:
                    title = os.path.splitext(uploaded_file.name)[0]
            elif ext == '.pdf':
                try:
                    import PyPDF2, io
                    reader   = PyPDF2.PdfReader(io.BytesIO(content))
                    raw_text = ' '.join(p.extract_text() or '' for p in reader.pages)
                    if not title:
                        title = os.path.splitext(uploaded_file.name)[0]
                except Exception as e:
                    messages.error(request, f'PDF error: {e}')
                    return render(request, 'search/upload.html', {'stats': stats})
            elif ext in ('.html', '.htm'):
                try:
                    from bs4 import BeautifulSoup
                    soup     = BeautifulSoup(content, 'html.parser')
                    raw_text = soup.get_text(separator=' ')
                    if not title:
                        t     = soup.find('title')
                        title = t.get_text() if t else os.path.splitext(uploaded_file.name)[0]
                except Exception as e:
                    messages.error(request, f'HTML error: {e}')
                    return render(request, 'search/upload.html', {'stats': stats})
            else:
                messages.error(request, 'Unsupported file. Use .txt, .pdf, or .html')
                return render(request, 'search/upload.html', {'stats': stats})

        if not title:
            messages.error(request, 'Title is required.')
            return render(request, 'search/upload.html', {'stats': stats})
        if not raw_text:
            messages.error(request, 'Document text is required.')
            return render(request, 'search/upload.html', {'stats': stats})

        doc = Document.objects.create(
            title=title, raw_text=raw_text,
            language=language, url=url or None,
        )
        InvertedIndexBuilder().build_index(Document.objects.filter(id=doc.id))
        messages.success(request, f'✅ "{title}" added and indexed!')
        return redirect('search:documents')

    return render(request, 'search/upload.html', {'stats': stats})


@_admin_required
def documents_view(request):
    docs  = Document.objects.all().order_by('-created_at')
    stats = InvertedIndexBuilder().get_collection_stats()
    return render(request, 'search/documents.html',
                  {'documents': docs, 'stats': stats})


@_admin_required
@require_POST
def delete_document(request, doc_id):
    doc   = get_object_or_404(Document, id=doc_id)
    title = doc.title
    doc.delete()
    IndexEntry.objects.all().delete()
    Document.objects.all().update(is_indexed=False)
    InvertedIndexBuilder().build_index(Document.objects.all())
    messages.success(request, f'🗑️ "{title}" deleted.')
    return redirect('search:documents')
