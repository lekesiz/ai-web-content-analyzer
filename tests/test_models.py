"""Tests for database models."""

import json
from datetime import datetime, timezone
from app.models import Analysis, SEODetail, AIRecommendation


class TestAnalysisModel:
    """Tests for the Analysis model."""

    def test_create_analysis(self, app):
        """Test creating a new analysis record."""
        from app import db
        analysis = Analysis(
            url='https://example.com',
            domain='example.com',
            status='completed',
            overall_score=75.5,
            seo_score=80.0,
            content_score=70.0,
            technical_score=90.0,
            page_title='Example Domain',
            meta_description='An example domain for testing.',
            word_count=150,
            language='en',
            response_time=0.5,
        )
        db.session.add(analysis)
        db.session.commit()

        saved = db.session.get(Analysis, analysis.id)
        assert saved is not None
        assert saved.url == 'https://example.com'
        assert saved.domain == 'example.com'
        assert saved.overall_score == 75.5
        assert saved.status == 'completed'

    def test_analysis_default_values(self, app):
        """Test default values for Analysis model."""
        from app import db
        analysis = Analysis(url='https://test.com')
        db.session.add(analysis)
        db.session.commit()

        assert analysis.status == 'pending'
        assert analysis.overall_score == 0.0
        assert analysis.seo_score == 0.0
        assert analysis.content_score == 0.0
        assert analysis.technical_score == 0.0
        assert analysis.word_count == 0
        assert analysis.timestamp is not None

    def test_analysis_to_dict(self, app):
        """Test the to_dict serialization method."""
        from app import db
        analysis = Analysis(
            url='https://example.com',
            domain='example.com',
            status='completed',
            overall_score=85.0,
            seo_score=90.0,
            content_score=80.0,
            technical_score=85.0,
            page_title='Test Page',
            word_count=200,
            language='en',
            response_time=0.3,
        )
        db.session.add(analysis)
        db.session.commit()

        data = analysis.to_dict()
        assert data['url'] == 'https://example.com'
        assert data['overall_score'] == 85.0
        assert data['seo_score'] == 90.0
        assert 'timestamp' in data
        assert data['seo_details'] is None  # No SEO details attached
        assert data['ai_recommendations'] == []

    def test_analysis_with_seo_details(self, app):
        """Test Analysis with related SEODetail."""
        from app import db
        analysis = Analysis(url='https://example.com', domain='example.com', status='completed')
        db.session.add(analysis)
        db.session.flush()

        seo = SEODetail(
            analysis_id=analysis.id,
            title_length=45,
            title_score=100.0,
            meta_desc_length=150,
            meta_desc_score=100.0,
            h1_count=1,
            h2_count=3,
            headings_score=100.0,
            img_total=5,
            img_without_alt=1,
            images_score=80.0,
            internal_links=10,
            external_links=3,
            links_score=90.0,
            has_canonical=True,
            has_og_tags=True,
            has_robots_meta=True,
            url_score=95.0,
            keyword_density=json.dumps([{'word': 'test', 'count': 5, 'density': 2.1}]),
            heading_structure=json.dumps([{'tag': 'h1', 'text': 'Title'}]),
            issues_json=json.dumps([]),
        )
        db.session.add(seo)
        db.session.commit()

        data = analysis.to_dict()
        assert data['seo_details'] is not None
        assert data['seo_details']['title_length'] == 45
        assert data['seo_details']['title_score'] == 100.0

    def test_cascade_delete(self, app):
        """Test cascade deletion of related records."""
        from app import db
        analysis = Analysis(url='https://example.com', domain='example.com')
        db.session.add(analysis)
        db.session.flush()

        seo = SEODetail(analysis_id=analysis.id, title_length=50)
        rec = AIRecommendation(
            analysis_id=analysis.id,
            category='seo',
            priority='high',
            title='Add meta description',
            description='Your page is missing a meta description.',
        )
        db.session.add_all([seo, rec])
        db.session.commit()

        analysis_id = analysis.id
        db.session.delete(analysis)
        db.session.commit()

        assert db.session.get(SEODetail, seo.id) is None
        assert db.session.get(AIRecommendation, rec.id) is None


class TestSEODetailModel:
    """Tests for the SEODetail model."""

    def test_to_dict_with_json_fields(self, app):
        """Test SEODetail serialization with JSON fields."""
        from app import db
        analysis = Analysis(url='https://example.com')
        db.session.add(analysis)
        db.session.flush()

        keywords = [{'word': 'python', 'count': 10, 'density': 3.5}]
        structure = [{'tag': 'h1', 'text': 'Main Title'}]
        issues = [{'severity': 'high', 'category': 'Title', 'message': 'Missing title'}]

        seo = SEODetail(
            analysis_id=analysis.id,
            keyword_density=json.dumps(keywords),
            heading_structure=json.dumps(structure),
            issues_json=json.dumps(issues),
        )
        db.session.add(seo)
        db.session.commit()

        data = seo.to_dict()
        assert data['keyword_density'] == keywords
        assert data['heading_structure'] == structure
        assert data['issues'] == issues

    def test_to_dict_empty_json_fields(self, app):
        """Test SEODetail with empty/null JSON fields."""
        from app import db
        analysis = Analysis(url='https://example.com')
        db.session.add(analysis)
        db.session.flush()

        seo = SEODetail(analysis_id=analysis.id)
        db.session.add(seo)
        db.session.commit()

        data = seo.to_dict()
        assert data['keyword_density'] == []
        assert data['heading_structure'] == []
        assert data['issues'] == []


class TestAIRecommendationModel:
    """Tests for the AIRecommendation model."""

    def test_create_recommendation(self, app):
        """Test creating an AI recommendation."""
        from app import db
        analysis = Analysis(url='https://example.com')
        db.session.add(analysis)
        db.session.flush()

        rec = AIRecommendation(
            analysis_id=analysis.id,
            category='seo',
            priority='high',
            title='Optimize title tag',
            description='Your title tag should be between 30-60 characters.',
            ai_model='gpt-4',
        )
        db.session.add(rec)
        db.session.commit()

        data = rec.to_dict()
        assert data['category'] == 'seo'
        assert data['priority'] == 'high'
        assert data['title'] == 'Optimize title tag'
        assert data['ai_model'] == 'gpt-4'
