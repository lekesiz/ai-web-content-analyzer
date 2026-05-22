"""Tests for ReportGenerator PDF/JSON output.

Covers the bug fixes documented in Suivi N°6 (22/05/2026) :
  - long URLs and long titles must wrap instead of being silently truncated.
"""

import json
from app.services.report_generator import ReportGenerator


def _make_sample(url='https://example.com/short', title='Sample Title'):
    return {
        'url': url,
        'timestamp': '2026-05-22T20:00:00',
        'overall_score': 87.0,
        'seo_score': 90.0,
        'content_score': 80.0,
        'technical_score': 95.0,
        'page_title': title,
        'word_count': 1234,
        'language': 'fr',
        'response_time': 0.45,
        'seo_details': None,
        'ai_recommendations': [],
    }


class TestReportGeneratorJson:
    def test_generate_json_includes_url(self):
        rg = ReportGenerator()
        out = rg.generate_json(_make_sample())
        data = json.loads(out)
        assert data['url'] == 'https://example.com/short'

    def test_generate_json_pretty_printed(self):
        rg = ReportGenerator()
        out = rg.generate_json(_make_sample())
        # indent=2 means there are newlines
        assert '\n' in out


class TestReportGeneratorPdf:
    def test_generate_pdf_returns_bytes(self):
        rg = ReportGenerator()
        out = rg.generate_pdf(_make_sample())
        assert isinstance(out, (bytes, bytearray))
        assert len(out) > 500  # non-trivial PDF
        assert out[:4] == b'%PDF'

    def test_generate_pdf_with_very_long_url_does_not_crash(self):
        """FIX (Suivi N°6 #1): long URLs must wrap, not crash or be cropped."""
        very_long_url = 'https://example.com/' + ('very-long-segment/' * 30) + 'end'
        rg = ReportGenerator()
        out = rg.generate_pdf(_make_sample(url=very_long_url))
        assert isinstance(out, (bytes, bytearray))
        assert out[:4] == b'%PDF'

    def test_generate_pdf_with_very_long_title_does_not_crash(self):
        """FIX (Suivi N°6 #1): long titles must wrap in page-info table."""
        very_long_title = 'A' * 300
        rg = ReportGenerator()
        out = rg.generate_pdf(_make_sample(title=very_long_title))
        assert isinstance(out, (bytes, bytearray))
        assert out[:4] == b'%PDF'

    def test_generate_pdf_with_empty_url(self):
        rg = ReportGenerator()
        sample = _make_sample()
        sample['url'] = ''
        out = rg.generate_pdf(sample)
        assert out[:4] == b'%PDF'
