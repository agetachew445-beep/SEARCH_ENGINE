"""
Web Crawler Module
==================
Crawls a URL and extracts clean text content for indexing.

Features:
  - Fetch any web page (HTML)
  - Extract clean text (removes nav, ads, scripts)
  - Extract page title automatically
  - Detect language of crawled content
  - Respect robots.txt (basic)
  - Timeout and error handling
  - Support for crawling multiple pages from a seed URL
"""

import re
import time
import urllib.robotparser
from urllib.parse import urljoin, urlparse
from typing import Optional, Dict, List

import requests
from bs4 import BeautifulSoup

from .preprocessing import detect_language


# ─────────────────────────────────────────────────────────────────────────
# SINGLE PAGE FETCHER
# ─────────────────────────────────────────────────────────────────────────
class WebPageFetcher:

    HEADERS = {
        'User-Agent': (
            'IRSearchBot/1.0 (Educational IR Project; '
            'compatible with robots.txt)'
        ),
        'Accept-Language': 'en,am,ti;q=0.9',
    }
    TIMEOUT = 15  # seconds

    # Tags whose content we discard entirely
    NOISE_TAGS = ['script', 'style', 'nav', 'footer', 'header',
                  'aside', 'advertisement', 'noscript', 'iframe',
                  'form', 'button', 'input', 'select', 'textarea']

    def fetch(self, url: str) -> Optional[Dict]:
        """
        Fetch a URL and return a dict with:
          title, text, url, language, word_count, status
        Returns None on failure.
        """
        try:
            resp = requests.get(
                url,
                headers=self.HEADERS,
                timeout=self.TIMEOUT,
                allow_redirects=True,
            )
            resp.raise_for_status()

            content_type = resp.headers.get('Content-Type', '')
            if 'text/html' not in content_type and 'text/plain' not in content_type:
                return {'error': f'Unsupported content type: {content_type}'}

            if 'text/plain' in content_type:
                text  = resp.text
                title = urlparse(url).path.split('/')[-1] or url
            else:
                title, text = self._parse_html(resp.text, url)

            if not text.strip():
                return {'error': 'No text content found on page'}

            language = detect_language(text)

            return {
                'title':      title,
                'text':       text,
                'url':        resp.url,   # final URL after redirects
                'language':   language,
                'word_count': len(text.split()),
                'status':     resp.status_code,
                'error':      None,
            }

        except requests.exceptions.Timeout:
            return {'error': f'Timeout fetching {url}'}
        except requests.exceptions.ConnectionError:
            return {'error': f'Cannot connect to {url}'}
        except requests.exceptions.HTTPError as e:
            return {'error': f'HTTP {e.response.status_code}: {url}'}
        except Exception as e:
            return {'error': str(e)}

    def _parse_html(self, html: str, base_url: str) -> tuple:
        """Parse HTML and return (title, clean_text)."""
        soup = BeautifulSoup(html, 'html.parser')

        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else ''

        # Try og:title or h1 if <title> is empty
        if not title:
            og = soup.find('meta', property='og:title')
            title = og['content'] if og and og.get('content') else ''
        if not title:
            h1 = soup.find('h1')
            title = h1.get_text(strip=True) if h1 else urlparse(base_url).netloc

        # Remove noise tags
        for tag in soup(self.NOISE_TAGS):
            tag.decompose()

        # Try to find main content area
        main = (soup.find('main') or
                soup.find('article') or
                soup.find(id=re.compile(r'content|main|article', re.I)) or
                soup.find(class_=re.compile(r'content|main|article|post', re.I)) or
                soup.find('body') or
                soup)

        # Extract text
        text = main.get_text(separator=' ', strip=True)

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return title, text

    def check_robots(self, url: str) -> bool:
        """Return True if crawling is allowed by robots.txt."""
        try:
            parsed   = urlparse(url)
            base_url = f'{parsed.scheme}://{parsed.netloc}'
            rp       = urllib.robotparser.RobotFileParser()
            rp.set_url(f'{base_url}/robots.txt')
            rp.read()
            return rp.can_fetch(self.HEADERS['User-Agent'], url)
        except Exception:
            return True  # Allow if robots.txt is unreachable


# ─────────────────────────────────────────────────────────────────────────
# MULTI-PAGE CRAWLER
# ─────────────────────────────────────────────────────────────────────────
class WebCrawler:
    """
    Crawl multiple pages from a seed URL.
    Stays within the same domain.
    """

    def __init__(self, max_pages: int = 5, delay: float = 1.0):
        self.max_pages = max_pages
        self.delay     = delay          # seconds between requests
        self.fetcher   = WebPageFetcher()

    def crawl(self, seed_url: str) -> List[Dict]:
        """
        Crawl up to max_pages pages starting from seed_url.
        Returns list of page dicts.
        """
        parsed_seed = urlparse(seed_url)
        base_domain = f'{parsed_seed.scheme}://{parsed_seed.netloc}'

        visited = set()
        queue   = [seed_url]
        results = []

        while queue and len(results) < self.max_pages:
            url = queue.pop(0)
            if url in visited:
                continue
            visited.add(url)

            # Respect robots.txt
            if not self.fetcher.check_robots(url):
                continue

            page = self.fetcher.fetch(url)
            if page and not page.get('error'):
                results.append(page)

                # Find links on this page (stay on same domain)
                if len(results) < self.max_pages:
                    links = self._extract_links(page.get('_html', ''),
                                                base_domain, url)
                    queue.extend(l for l in links if l not in visited)

            # Polite delay
            if queue:
                time.sleep(self.delay)

        return results

    def _extract_links(self, html: str, base_domain: str,
                       current_url: str) -> List[str]:
        """Extract same-domain links from HTML."""
        if not html:
            return []
        soup  = BeautifulSoup(html, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = urljoin(current_url, a['href'])
            parsed = urlparse(href)
            # Same domain, HTTP/HTTPS only, no fragments
            if (parsed.scheme in ('http', 'https') and
                    href.startswith(base_domain) and
                    not parsed.fragment):
                links.append(href.split('#')[0])
        return list(set(links))
