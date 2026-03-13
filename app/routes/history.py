"""History API routes for browsing past analyses."""

from flask import Blueprint, request, jsonify
from app import db
from app.models import Analysis

history_bp = Blueprint('history', __name__)


@history_bp.route('/api/history')
def history_api():
    """Get paginated analysis history."""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    sort = request.args.get('sort', 'timestamp')
    order = request.args.get('order', 'desc')
    search = request.args.get('search', '').strip()

    limit = min(limit, 100)

    query = Analysis.query

    if search:
        query = query.filter(Analysis.url.ilike(f'%{search}%'))

    # Sorting
    sort_column = getattr(Analysis, sort, Analysis.timestamp)
    if order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    total = query.count()
    analyses = query.offset((page - 1) * limit).limit(limit).all()

    return jsonify({
        'success': True,
        'analyses': [
            {
                'id': a.id,
                'url': a.url,
                'domain': a.domain,
                'timestamp': a.timestamp.isoformat() if a.timestamp else None,
                'status': a.status,
                'overall_score': a.overall_score,
                'seo_score': a.seo_score,
                'content_score': a.content_score,
            }
            for a in analyses
        ],
        'total': total,
        'page': page,
        'per_page': limit,
    })
