"""Analysis API routes - orchestrates the full analysis pipeline."""

import json
from flask import Blueprint, request, jsonify, render_template, Response, current_app
from app import db
from app.models import Analysis, SEODetail, AIRecommendation
from app.services.scraper import WebScraper, ScraperError
from app.services.seo_analyzer import SEOAnalyzer
from app.services.content_analyzer import ContentAnalyzer
from app.services.ai_analyzer import AIAnalyzer
from app.services.report_generator import ReportGenerator
from urllib.parse import urlparse

analysis_bp = Blueprint('analysis', __name__)


@analysis_bp.route('/analyze', methods=['POST'])
def analyze():
    """Run full analysis pipeline on a URL."""
    data = request.get_json()
    if not data or not data.get('url'):
        return jsonify({'success': False, 'error': 'URL is required'}), 400

    url = data['url'].strip()

    try:
        # Step 1: Scrape
        scraper = WebScraper(url)
        scraped = scraper.extract_all()

        # Step 2: SEO Analysis
        seo_analyzer = SEOAnalyzer(scraped, scraped['url'])
        seo_results = seo_analyzer.run_full_analysis()

        # Step 3: Content Analysis
        content_analyzer = ContentAnalyzer(
            scraped.get('text_content', ''),
            scraped.get('paragraphs', []),
            scraped.get('headings', []),
            len(scraper.html) if scraper.html else 0,
        )
        content_results = content_analyzer.run_full_analysis()

        # Step 4: AI Analysis
        api_key = current_app.config.get('OPENAI_API_KEY')
        ai_analyzer = AIAnalyzer(api_key)
        ai_results = ai_analyzer.run_full_ai_analysis(scraped, seo_results, content_results)

        # Step 5: Calculate scores
        seo_score = seo_results['overall_score']
        content_score = content_results['score']
        technical_score = _calculate_technical_score(scraped)
        ai_score = 50  # neutral default
        if ai_results.get('available') and ai_results.get('content_quality'):
            ai_score = ai_results['content_quality'].get('score', 50)

        overall_score = (
            seo_score * 0.40 +
            content_score * 0.30 +
            technical_score * 0.20 +
            ai_score * 0.10
        )

        # Step 6: Save to database
        parsed_url = urlparse(scraped['url'])
        analysis = Analysis(
            url=scraped['url'],
            domain=parsed_url.netloc,
            status='completed',
            overall_score=round(overall_score, 1),
            seo_score=round(seo_score, 1),
            content_score=round(content_score, 1),
            technical_score=round(technical_score, 1),
            page_title=scraped.get('title', ''),
            meta_description=scraped.get('meta_description', ''),
            word_count=scraped.get('word_count', 0),
            language=content_results.get('language', {}).get('language', ''),
            response_time=scraped.get('response_time', 0),
        )
        db.session.add(analysis)
        db.session.flush()

        # Save SEO details
        seo_detail = SEODetail(
            analysis_id=analysis.id,
            title_length=seo_results['title'].get('length', 0),
            title_score=seo_results['title'].get('score', 0),
            meta_desc_length=seo_results['meta_description'].get('length', 0),
            meta_desc_score=seo_results['meta_description'].get('score', 0),
            h1_count=seo_results['headings'].get('h1_count', 0),
            h2_count=seo_results['headings'].get('h2_count', 0),
            headings_score=seo_results['headings'].get('score', 0),
            img_total=seo_results['images'].get('total', 0),
            img_without_alt=seo_results['images'].get('without_alt', 0),
            images_score=seo_results['images'].get('score', 0),
            internal_links=seo_results['links'].get('internal', 0),
            external_links=seo_results['links'].get('external', 0),
            links_score=seo_results['links'].get('score', 0),
            has_canonical=seo_results['canonical'].get('has_canonical', False),
            has_og_tags=bool(seo_results['social'].get('og_tags')),
            has_robots_meta=seo_results['robots'].get('has_robots', False),
            url_score=seo_results['url'].get('score', 0),
            keyword_density=seo_results.get('keyword_density', '[]'),
            heading_structure=seo_results.get('heading_structure', '[]'),
            issues_json=json.dumps(seo_results.get('issues', [])),
        )
        db.session.add(seo_detail)

        # Save AI recommendations
        if ai_results.get('recommendations'):
            for rec in ai_results['recommendations']:
                ai_rec = AIRecommendation(
                    analysis_id=analysis.id,
                    category=rec.get('category', 'general'),
                    priority=rec.get('priority', 'medium'),
                    title=rec.get('title', ''),
                    description=rec.get('description', ''),
                    ai_model='gpt-4',
                )
                db.session.add(ai_rec)

        db.session.commit()

        return jsonify({
            'success': True,
            'analysis_id': analysis.id,
            'overall_score': analysis.overall_score,
        })

    except ScraperError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Analysis failed: {str(e)}'}), 500


@analysis_bp.route('/analysis/<int:analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Get full analysis results."""
    analysis = db.session.get(Analysis, analysis_id)
    if not analysis:
        return jsonify({'success': False, 'error': 'Analysis not found'}), 404

    return jsonify({'success': True, 'analysis': analysis.to_dict()})


@analysis_bp.route('/analysis/<int:analysis_id>', methods=['DELETE'])
def delete_analysis(analysis_id):
    """Delete an analysis."""
    analysis = db.session.get(Analysis, analysis_id)
    if not analysis:
        return jsonify({'success': False, 'error': 'Analysis not found'}), 404

    db.session.delete(analysis)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Analysis deleted'})


@analysis_bp.route('/analysis/<int:analysis_id>/export/json', methods=['GET'])
def export_json(analysis_id):
    """Export analysis as JSON file."""
    analysis = db.session.get(Analysis, analysis_id)
    if not analysis:
        return jsonify({'success': False, 'error': 'Analysis not found'}), 404

    generator = ReportGenerator()
    json_data = generator.generate_json(analysis.to_dict())

    return Response(
        json_data,
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename=analysis_{analysis_id}.json'},
    )


@analysis_bp.route('/analysis/<int:analysis_id>/export/pdf', methods=['GET'])
def export_pdf(analysis_id):
    """Export analysis as PDF."""
    analysis = db.session.get(Analysis, analysis_id)
    if not analysis:
        return jsonify({'success': False, 'error': 'Analysis not found'}), 404

    generator = ReportGenerator()
    pdf_bytes = generator.generate_pdf(analysis.to_dict())

    return Response(
        pdf_bytes,
        mimetype='application/pdf',
        headers={'Content-Disposition': f'attachment; filename=analysis_{analysis_id}.pdf'},
    )


def _calculate_technical_score(scraped_data):
    """Calculate technical score based on response metrics."""
    score = 100

    response_time = scraped_data.get('response_time', 0)
    if response_time > 5:
        score -= 40
    elif response_time > 3:
        score -= 20
    elif response_time > 1:
        score -= 10

    status = scraped_data.get('status_code', 200)
    if status != 200:
        score -= 30

    content_type = scraped_data.get('content_type', '')
    if 'text/html' not in content_type.lower():
        score -= 20

    return max(0, score)
