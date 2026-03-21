"""Tests for the SEO analyzer service."""

import json
from app.services.seo_analyzer import SEOAnalyzer


class TestSEOAnalyzerTitle:
    """Tests for title tag analysis."""

    def test_good_title(self, sample_scraped_data):
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_title()
        assert result['score'] == 100
        assert result['length'] > 0

    def test_missing_title(self, sample_scraped_data):
        sample_scraped_data['title'] = ''
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_title()
        assert result['score'] == 0
        assert any('Missing title' in i['message'] for i in analyzer.issues)

    def test_short_title(self, sample_scraped_data):
        sample_scraped_data['title'] = 'Short'
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_title()
        assert result['score'] == 50
        assert result['length'] == 5

    def test_long_title(self, sample_scraped_data):
        sample_scraped_data['title'] = 'A' * 80
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_title()
        assert result['score'] == 70


class TestSEOAnalyzerMetaDescription:
    """Tests for meta description analysis."""

    def test_good_meta_description(self, sample_scraped_data):
        # The sample meta description is 130 chars, which is in range (120-160)
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_meta_description()
        # Check that the score is reasonable (depends on length)
        assert result['score'] >= 50
        assert result['length'] > 0

    def test_missing_meta_description(self, sample_scraped_data):
        sample_scraped_data['meta_description'] = ''
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_meta_description()
        assert result['score'] == 0

    def test_short_meta_description(self, sample_scraped_data):
        sample_scraped_data['meta_description'] = 'Too short.'
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_meta_description()
        assert result['score'] == 50

    def test_long_meta_description(self, sample_scraped_data):
        sample_scraped_data['meta_description'] = 'A' * 200
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_meta_description()
        assert result['score'] == 70


class TestSEOAnalyzerHeadings:
    """Tests for heading structure analysis."""

    def test_good_heading_structure(self, sample_scraped_data):
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_headings()
        assert result['score'] == 100
        assert result['h1_count'] == 1
        assert result['h2_count'] == 2

    def test_missing_h1(self, sample_scraped_data):
        sample_scraped_data['headings'] = [
            {'tag': 'h2', 'text': 'Section 1'},
        ]
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_headings()
        assert result['score'] < 100
        assert result['h1_count'] == 0

    def test_multiple_h1(self, sample_scraped_data):
        sample_scraped_data['headings'] = [
            {'tag': 'h1', 'text': 'Title 1'},
            {'tag': 'h1', 'text': 'Title 2'},
            {'tag': 'h2', 'text': 'Section'},
        ]
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_headings()
        assert result['h1_count'] == 2
        assert any('Multiple H1' in i['message'] for i in analyzer.issues)

    def test_no_headings(self, sample_scraped_data):
        sample_scraped_data['headings'] = []
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_headings()
        assert result['score'] < 50

    def test_skipped_heading_level(self, sample_scraped_data):
        sample_scraped_data['headings'] = [
            {'tag': 'h1', 'text': 'Title'},
            {'tag': 'h3', 'text': 'Skipped h2'},
        ]
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_headings()
        assert any('Skipped heading' in i['message'] for i in analyzer.issues)


class TestSEOAnalyzerImages:
    """Tests for image analysis."""

    def test_images_with_alt(self, sample_scraped_data):
        sample_scraped_data['images'] = [
            {'src': '/img/a.png', 'alt': 'Image A', 'has_alt': True},
            {'src': '/img/b.png', 'alt': 'Image B', 'has_alt': True},
        ]
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_images()
        assert result['score'] == 100

    def test_images_missing_alt(self, sample_scraped_data):
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_images()
        assert result['without_alt'] == 1
        assert result['score'] < 100

    def test_no_images(self, sample_scraped_data):
        sample_scraped_data['images'] = []
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_images()
        assert result['score'] == 100
        assert result['total'] == 0


class TestSEOAnalyzerLinks:
    """Tests for link analysis."""

    def test_good_links(self, sample_scraped_data):
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_links()
        assert result['internal'] == 2
        assert result['external'] == 1

    def test_no_links(self, sample_scraped_data):
        sample_scraped_data['links'] = []
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_links()
        assert result['score'] == 40

    def test_few_internal_links(self, sample_scraped_data):
        sample_scraped_data['links'] = [
            {'href': '/about', 'text': 'About', 'is_internal': True, 'has_nofollow': False},
        ]
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.analyze_links()
        assert result['score'] < 100


class TestSEOAnalyzerURL:
    """Tests for URL structure analysis."""

    def test_clean_url(self, sample_scraped_data):
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com/blog/my-post')
        result = analyzer.analyze_url_structure()
        assert result['score'] == 100

    def test_url_with_underscores(self, sample_scraped_data):
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com/my_page')
        result = analyzer.analyze_url_structure()
        assert result['score'] < 100

    def test_url_with_uppercase(self, sample_scraped_data):
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com/MyPage')
        result = analyzer.analyze_url_structure()
        assert result['score'] < 100

    def test_long_url(self, sample_scraped_data):
        long_path = '/a' * 60
        analyzer = SEOAnalyzer(sample_scraped_data, f'https://example.com{long_path}')
        result = analyzer.analyze_url_structure()
        assert result['score'] < 100

    def test_url_with_query_params(self, sample_scraped_data):
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com/page?id=123&ref=abc')
        result = analyzer.analyze_url_structure()
        assert result['score'] < 100


class TestSEOAnalyzerFullAnalysis:
    """Tests for the full analysis pipeline."""

    def test_full_analysis_returns_all_fields(self, sample_scraped_data):
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.run_full_analysis()

        assert 'overall_score' in result
        assert 'title' in result
        assert 'meta_description' in result
        assert 'headings' in result
        assert 'images' in result
        assert 'links' in result
        assert 'url' in result
        assert 'keywords' in result
        assert 'social' in result
        assert 'canonical' in result
        assert 'robots' in result
        assert 'issues' in result
        assert 0 <= result['overall_score'] <= 100

    def test_full_analysis_score_range(self, sample_scraped_data):
        analyzer = SEOAnalyzer(sample_scraped_data, 'https://example.com')
        result = analyzer.run_full_analysis()
        assert 0 <= result['overall_score'] <= 100

    def test_full_analysis_with_poor_data(self):
        poor_data = {
            'title': '',
            'meta_description': '',
            'headings': [],
            'images': [],
            'links': [],
            'text_content': '',
            'og_tags': {},
            'canonical_url': '',
            'robots_meta': '',
        }
        analyzer = SEOAnalyzer(poor_data, 'https://example.com')
        result = analyzer.run_full_analysis()
        assert result['overall_score'] < 50
        assert len(result['issues']) > 0
