"""Tests for the web scraper service."""

import pytest
from app.services.scraper import WebScraper, InvalidURLError, FetchError


class TestWebScraperValidation:
    """Tests for URL validation."""

    def test_valid_https_url(self):
        scraper = WebScraper('https://example.com')
        assert scraper.validate_url() is True

    def test_valid_http_url(self):
        scraper = WebScraper('http://example.com')
        assert scraper.validate_url() is True

    def test_url_without_scheme(self):
        scraper = WebScraper('example.com')
        scraper.validate_url()
        assert scraper.url == 'https://example.com'

    def test_empty_url(self):
        scraper = WebScraper('')
        with pytest.raises(InvalidURLError, match='URL is required'):
            scraper.validate_url()

    def test_invalid_scheme(self):
        """FTP URLs get https:// prepended since they don't start with http/https."""
        scraper = WebScraper('ftp://example.com')
        scraper.validate_url()
        # The scraper adds https:// prefix since ftp:// doesn't match http/https
        assert scraper.url.startswith('https://')

    def test_url_with_whitespace(self):
        scraper = WebScraper('  https://example.com  ')
        assert scraper.validate_url() is True
        assert scraper.url == 'https://example.com'

    def test_url_with_path(self):
        scraper = WebScraper('https://example.com/path/to/page')
        assert scraper.validate_url() is True

    def test_url_with_query_params(self):
        scraper = WebScraper('https://example.com/page?q=test&lang=en')
        assert scraper.validate_url() is True


    # ----- FIX (Suivi N°6): URL validation hardening (SSRF / DoS) -----

    def test_blocks_localhost(self):
        from app.services.scraper import InvalidURLError
        scraper = WebScraper('http://localhost/admin')
        with pytest.raises(InvalidURLError):
            scraper.validate_url()

    def test_blocks_127_loopback(self):
        from app.services.scraper import InvalidURLError
        scraper = WebScraper('http://127.0.0.1:8000')
        with pytest.raises(InvalidURLError):
            scraper.validate_url()

    def test_blocks_aws_metadata(self):
        from app.services.scraper import InvalidURLError
        scraper = WebScraper('http://169.254.169.254/latest/meta-data/')
        with pytest.raises(InvalidURLError):
            scraper.validate_url()

    def test_blocks_private_network_10(self):
        from app.services.scraper import InvalidURLError
        scraper = WebScraper('http://10.0.0.1/')
        with pytest.raises(InvalidURLError):
            scraper.validate_url()

    def test_blocks_private_network_192_168(self):
        from app.services.scraper import InvalidURLError
        scraper = WebScraper('http://192.168.1.1/router')
        with pytest.raises(InvalidURLError):
            scraper.validate_url()

    def test_blocks_overly_long_url(self):
        from app.services.scraper import InvalidURLError
        scraper = WebScraper('https://example.com/' + 'a' * 3000)
        with pytest.raises(InvalidURLError):
            scraper.validate_url()

    def test_public_url_still_works_after_hardening(self):
        scraper = WebScraper('https://example.com/path?q=1')
        assert scraper.validate_url() is True


class TestWebScraperParse:
    """Tests for HTML parsing (no network calls)."""

    def _make_scraper_with_html(self, html, url='https://example.com'):
        from bs4 import BeautifulSoup
        from urllib.parse import urlparse
        scraper = WebScraper(url)
        scraper.url = url
        scraper._parsed_url = urlparse(url)
        scraper.html = html
        scraper.soup = BeautifulSoup(html, 'lxml')
        return scraper

    def test_extract_title(self):
        html = '<html><head><title>Test Page Title</title></head><body></body></html>'
        scraper = self._make_scraper_with_html(html)
        result = scraper.parse()
        assert result['title'] == 'Test Page Title'

    def test_extract_meta_description(self):
        html = '<html><head><meta name="description" content="A test description"></head><body></body></html>'
        scraper = self._make_scraper_with_html(html)
        result = scraper.parse()
        assert result['meta_description'] == 'A test description'

    def test_extract_headings(self):
        html = '''
        <html><body>
            <h1>Main Title</h1>
            <h2>Section 1</h2>
            <h2>Section 2</h2>
            <h3>Subsection</h3>
        </body></html>
        '''
        scraper = self._make_scraper_with_html(html)
        result = scraper.parse()
        h1s = [h for h in result['headings'] if h['tag'] == 'h1']
        h2s = [h for h in result['headings'] if h['tag'] == 'h2']
        assert len(h1s) == 1
        assert len(h2s) == 2
        assert h1s[0]['text'] == 'Main Title'

    def test_extract_images(self):
        html = '''
        <html><body>
            <img src="/img/logo.png" alt="Logo">
            <img src="/img/hero.jpg" alt="">
        </body></html>
        '''
        scraper = self._make_scraper_with_html(html)
        result = scraper.parse()
        assert len(result['images']) == 2
        assert result['images'][0]['has_alt'] is True
        assert result['images'][1]['has_alt'] is False

    def test_extract_links(self):
        html = '''
        <html><body>
            <a href="/about">About</a>
            <a href="https://external.com">External</a>
            <a href="mailto:test@test.com">Email</a>
        </body></html>
        '''
        scraper = self._make_scraper_with_html(html)
        result = scraper.parse()
        # mailto should be filtered out
        assert len(result['links']) == 2
        internal = [l for l in result['links'] if l['is_internal']]
        external = [l for l in result['links'] if not l['is_internal']]
        assert len(internal) == 1
        assert len(external) == 1

    def test_extract_og_tags(self):
        html = '''
        <html><head>
            <meta property="og:title" content="OG Title">
            <meta property="og:description" content="OG Description">
        </head><body></body></html>
        '''
        scraper = self._make_scraper_with_html(html)
        result = scraper.parse()
        assert result['og_tags']['og:title'] == 'OG Title'
        assert result['og_tags']['og:description'] == 'OG Description'

    def test_extract_canonical(self):
        html = '<html><head><link rel="canonical" href="https://example.com/page"></head><body></body></html>'
        scraper = self._make_scraper_with_html(html)
        result = scraper.parse()
        assert result['canonical_url'] == 'https://example.com/page'

    def test_extract_language(self):
        html = '<html lang="fr"><body><p>Bonjour le monde</p></body></html>'
        scraper = self._make_scraper_with_html(html)
        result = scraper.parse()
        assert result['lang'] == 'fr'

    def test_word_count(self):
        html = '<html><body><p>One two three four five</p></body></html>'
        scraper = self._make_scraper_with_html(html)
        result = scraper.parse()
        assert result['word_count'] >= 5

    def test_robots_meta(self):
        html = '<html><head><meta name="robots" content="noindex, nofollow"></head><body></body></html>'
        scraper = self._make_scraper_with_html(html)
        result = scraper.parse()
        assert 'noindex' in result['robots_meta']

    def test_scripts_and_stylesheets_count(self):
        html = '''
        <html><head>
            <script src="a.js"></script>
            <script src="b.js"></script>
            <link rel="stylesheet" href="style.css">
        </head><body></body></html>
        '''
        scraper = self._make_scraper_with_html(html)
        result = scraper.parse()
        assert result['scripts_count'] == 2
        assert result['stylesheets_count'] == 1

    def test_empty_html(self):
        html = '<html><body></body></html>'
        scraper = self._make_scraper_with_html(html)
        result = scraper.parse()
        assert result['title'] == ''
        assert result['word_count'] == 0

    def test_parse_without_fetch_raises(self):
        scraper = WebScraper('https://example.com')
        with pytest.raises(Exception):
            scraper.parse()
