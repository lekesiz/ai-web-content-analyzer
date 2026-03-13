"""Web scraping engine for extracting and parsing web page content."""

import time
from urllib.parse import urlparse, urljoin

import certifi
import requests
from bs4 import BeautifulSoup


class ScraperError(Exception):
    """Base exception for scraper errors."""
    pass


class InvalidURLError(ScraperError):
    """Raised when URL is invalid."""
    pass


class FetchError(ScraperError):
    """Raised when fetching fails."""
    pass


class WebScraper:
    """Fetches and parses web pages into structured data."""

    TIMEOUT = 15
    USER_AGENT = 'AIWebAnalyzer/1.0 (Academic Project - Universite de Strasbourg)'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

    def __init__(self, url):
        self.url = url.strip()
        self.html = None
        self.soup = None
        self.response = None
        self._parsed_url = None

    def validate_url(self):
        """Validate URL format and scheme."""
        if not self.url:
            raise InvalidURLError('URL is required')

        # Add scheme if missing
        if not self.url.startswith(('http://', 'https://')):
            self.url = 'https://' + self.url

        try:
            parsed = urlparse(self.url)
            if parsed.scheme not in ('http', 'https'):
                raise InvalidURLError(f'Invalid scheme: {parsed.scheme}. Only HTTP/HTTPS allowed.')
            if not parsed.netloc:
                raise InvalidURLError('Invalid URL: no domain found')
            self._parsed_url = parsed
        except ValueError as e:
            raise InvalidURLError(f'Invalid URL: {e}')

        return True

    def fetch(self):
        """Fetch the web page. Returns metadata dict."""
        headers = {
            'User-Agent': self.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        }

        start_time = time.time()

        try:
            self.response = requests.get(
                self.url,
                headers=headers,
                timeout=self.TIMEOUT,
                allow_redirects=True,
                verify=certifi.where(),
            )
            response_time = time.time() - start_time

            # Check content length
            content_length = len(self.response.content)
            if content_length > self.MAX_CONTENT_LENGTH:
                raise FetchError(f'Content too large: {content_length} bytes (max {self.MAX_CONTENT_LENGTH})')

            # Check content type
            content_type = self.response.headers.get('Content-Type', '')
            if not any(ct in content_type.lower() for ct in ('text/html', 'application/xhtml')):
                raise FetchError(f'Not an HTML page: {content_type}')

            self.response.raise_for_status()
            self.html = self.response.text

            return {
                'status_code': self.response.status_code,
                'response_time': round(response_time, 3),
                'content_type': content_type,
                'content_length': content_length,
                'final_url': self.response.url,
            }

        except requests.exceptions.Timeout:
            raise FetchError(f'Request timed out after {self.TIMEOUT} seconds')
        except requests.exceptions.ConnectionError:
            raise FetchError(f'Could not connect to {self.url}')
        except requests.exceptions.HTTPError as e:
            raise FetchError(f'HTTP error: {e.response.status_code}')
        except requests.exceptions.RequestException as e:
            raise FetchError(f'Request failed: {str(e)}')

    def parse(self):
        """Parse the fetched HTML into structured data."""
        if not self.html:
            raise ScraperError('No HTML to parse. Call fetch() first.')

        self.soup = BeautifulSoup(self.html, 'lxml')

        # Remove script and style elements for text extraction
        text_soup = BeautifulSoup(self.html, 'lxml')
        for tag in text_soup(['script', 'style', 'noscript']):
            tag.decompose()

        text_content = text_soup.get_text(separator=' ', strip=True)
        words = text_content.split()

        return {
            'title': self._extract_title(),
            'meta_description': self._extract_meta('description'),
            'meta_keywords': self._extract_meta('keywords'),
            'canonical_url': self._extract_canonical(),
            'og_tags': self._extract_og_tags(),
            'headings': self._extract_headings(),
            'paragraphs': self._extract_paragraphs(),
            'links': self._extract_links(),
            'images': self._extract_images(),
            'text_content': text_content,
            'word_count': len(words),
            'robots_meta': self._extract_meta('robots'),
            'lang': self._extract_lang(),
            'scripts_count': len(self.soup.find_all('script')),
            'stylesheets_count': len(self.soup.find_all('link', rel='stylesheet')),
        }

    def extract_all(self):
        """Full pipeline: validate -> fetch -> parse."""
        self.validate_url()
        fetch_meta = self.fetch()
        parsed = self.parse()
        return {**fetch_meta, **parsed, 'url': self.url}

    # --- Private extraction methods ---

    def _extract_title(self):
        tag = self.soup.find('title')
        return tag.get_text(strip=True) if tag else ''

    def _extract_meta(self, name):
        tag = self.soup.find('meta', attrs={'name': name})
        if not tag:
            tag = self.soup.find('meta', attrs={'name': name.capitalize()})
        return tag.get('content', '') if tag else ''

    def _extract_canonical(self):
        tag = self.soup.find('link', rel='canonical')
        return tag.get('href', '') if tag else ''

    def _extract_og_tags(self):
        og_tags = {}
        for tag in self.soup.find_all('meta', attrs={'property': True}):
            prop = tag.get('property', '')
            if prop.startswith('og:'):
                og_tags[prop] = tag.get('content', '')
        return og_tags

    def _extract_headings(self):
        headings = []
        for level in range(1, 7):
            for tag in self.soup.find_all(f'h{level}'):
                text = tag.get_text(strip=True)
                if text:
                    headings.append({'tag': f'h{level}', 'text': text})
        return headings

    def _extract_paragraphs(self):
        return [
            p.get_text(strip=True)
            for p in self.soup.find_all('p')
            if p.get_text(strip=True)
        ]

    def _extract_links(self):
        base_domain = self._parsed_url.netloc if self._parsed_url else ''
        links = []

        for a in self.soup.find_all('a', href=True):
            href = a.get('href', '')
            if not href or href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                continue

            full_url = urljoin(self.url, href)
            parsed = urlparse(full_url)
            is_internal = parsed.netloc == base_domain

            rel = a.get('rel', [])
            has_nofollow = 'nofollow' in rel if isinstance(rel, list) else 'nofollow' in str(rel)

            links.append({
                'href': full_url,
                'text': a.get_text(strip=True),
                'is_internal': is_internal,
                'has_nofollow': has_nofollow,
            })

        return links

    def _extract_images(self):
        images = []
        for img in self.soup.find_all('img'):
            src = img.get('src', '')
            alt = img.get('alt', '')
            images.append({
                'src': urljoin(self.url, src) if src else '',
                'alt': alt,
                'has_alt': bool(alt.strip()),
            })
        return images

    def _extract_lang(self):
        html_tag = self.soup.find('html')
        if html_tag:
            return html_tag.get('lang', '')
        return ''
