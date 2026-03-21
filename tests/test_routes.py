"""Tests for API routes."""

import json
from unittest.mock import patch, MagicMock
from app import db
from app.models import Analysis, SEODetail


class TestAnalyzeEndpoint:
    """Tests for the POST /api/analyze endpoint."""

    def test_analyze_missing_url(self, client):
        response = client.post('/api/analyze', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'URL is required' in data['error']

    def test_analyze_empty_url(self, client):
        response = client.post('/api/analyze', json={'url': ''})
        assert response.status_code == 400

    def test_analyze_no_json_body(self, client):
        response = client.post('/api/analyze', content_type='application/json', data='{}')
        data = response.get_json()
        assert data['success'] is False


class TestGetAnalysisEndpoint:
    """Tests for the GET /api/analysis/<id> endpoint."""

    def test_get_existing_analysis(self, app, client):
        analysis = Analysis(
            url='https://example.com',
            domain='example.com',
            status='completed',
            overall_score=75.0,
            seo_score=80.0,
            content_score=70.0,
            technical_score=90.0,
        )
        db.session.add(analysis)
        db.session.commit()

        response = client.get(f'/api/analysis/{analysis.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['analysis']['url'] == 'https://example.com'
        assert data['analysis']['overall_score'] == 75.0

    def test_get_nonexistent_analysis(self, client):
        response = client.get('/api/analysis/99999')
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] is False


class TestDeleteAnalysisEndpoint:
    """Tests for the DELETE /api/analysis/<id> endpoint."""

    def test_delete_existing_analysis(self, app, client):
        analysis = Analysis(url='https://example.com', domain='example.com')
        db.session.add(analysis)
        db.session.commit()
        aid = analysis.id

        response = client.delete(f'/api/analysis/{aid}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

        # Verify it's gone
        assert db.session.get(Analysis, aid) is None

    def test_delete_nonexistent_analysis(self, client):
        response = client.delete('/api/analysis/99999')
        assert response.status_code == 404


class TestExportEndpoints:
    """Tests for export endpoints."""

    def test_export_json(self, app, client):
        analysis = Analysis(
            url='https://example.com',
            domain='example.com',
            status='completed',
            overall_score=75.0,
        )
        db.session.add(analysis)
        db.session.commit()

        response = client.get(f'/api/analysis/{analysis.id}/export/json')
        assert response.status_code == 200
        assert 'application/json' in response.content_type

    def test_export_json_not_found(self, client):
        response = client.get('/api/analysis/99999/export/json')
        assert response.status_code == 404

    def test_export_pdf(self, app, client):
        analysis = Analysis(
            url='https://example.com',
            domain='example.com',
            status='completed',
            overall_score=75.0,
        )
        db.session.add(analysis)
        db.session.commit()

        response = client.get(f'/api/analysis/{analysis.id}/export/pdf')
        assert response.status_code == 200
        assert 'application/pdf' in response.content_type


class TestHistoryEndpoint:
    """Tests for the GET /api/history endpoint."""

    def test_empty_history(self, client):
        response = client.get('/api/history')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['analyses'] == []
        assert data['total'] == 0

    def test_history_with_data(self, app, client):
        for i in range(5):
            analysis = Analysis(
                url=f'https://example{i}.com',
                domain=f'example{i}.com',
                status='completed',
                overall_score=60.0 + i * 5,
            )
            db.session.add(analysis)
        db.session.commit()

        response = client.get('/api/history')
        data = response.get_json()
        assert data['total'] == 5
        assert len(data['analyses']) == 5

    def test_history_pagination(self, app, client):
        for i in range(25):
            db.session.add(Analysis(url=f'https://site{i}.com', domain=f'site{i}.com'))
        db.session.commit()

        response = client.get('/api/history?page=1&limit=10')
        data = response.get_json()
        assert len(data['analyses']) == 10
        assert data['total'] == 25
        assert data['page'] == 1

    def test_history_search(self, app, client):
        db.session.add(Analysis(url='https://python.org', domain='python.org'))
        db.session.add(Analysis(url='https://javascript.com', domain='javascript.com'))
        db.session.commit()

        response = client.get('/api/history?search=python')
        data = response.get_json()
        assert data['total'] == 1
        assert 'python' in data['analyses'][0]['url']

    def test_history_sorting(self, app, client):
        a1 = Analysis(url='https://a.com', domain='a.com', overall_score=90.0)
        a2 = Analysis(url='https://b.com', domain='b.com', overall_score=50.0)
        db.session.add_all([a1, a2])
        db.session.commit()

        response = client.get('/api/history?sort=overall_score&order=desc')
        data = response.get_json()
        scores = [a['overall_score'] for a in data['analyses']]
        assert scores[0] >= scores[1]

    def test_history_limit_cap(self, app, client):
        """Ensure limit is capped at 100."""
        response = client.get('/api/history?limit=500')
        data = response.get_json()
        assert data['per_page'] == 100
