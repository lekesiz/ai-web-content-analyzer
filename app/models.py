from datetime import datetime, timezone
from app import db


class Analysis(db.Model):
    __tablename__ = 'analyses'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    domain = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.Text, default='pending')
    overall_score = db.Column(db.Float, default=0.0)
    seo_score = db.Column(db.Float, default=0.0)
    content_score = db.Column(db.Float, default=0.0)
    technical_score = db.Column(db.Float, default=0.0)
    page_title = db.Column(db.Text)
    meta_description = db.Column(db.Text)
    word_count = db.Column(db.Integer, default=0)
    language = db.Column(db.Text)
    response_time = db.Column(db.Float)
    error_message = db.Column(db.Text)

    seo_details = db.relationship('SEODetail', backref='analysis', cascade='all, delete-orphan', uselist=False)
    ai_recommendations = db.relationship('AIRecommendation', backref='analysis', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'domain': self.domain,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'status': self.status,
            'overall_score': self.overall_score,
            'seo_score': self.seo_score,
            'content_score': self.content_score,
            'technical_score': self.technical_score,
            'page_title': self.page_title,
            'meta_description': self.meta_description,
            'word_count': self.word_count,
            'language': self.language,
            'response_time': self.response_time,
            'error_message': self.error_message,
            'seo_details': self.seo_details.to_dict() if self.seo_details else None,
            'ai_recommendations': [r.to_dict() for r in self.ai_recommendations],
        }


class SEODetail(db.Model):
    __tablename__ = 'seo_details'

    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analyses.id'), nullable=False)
    title_length = db.Column(db.Integer, default=0)
    title_score = db.Column(db.Float, default=0.0)
    meta_desc_length = db.Column(db.Integer, default=0)
    meta_desc_score = db.Column(db.Float, default=0.0)
    h1_count = db.Column(db.Integer, default=0)
    h2_count = db.Column(db.Integer, default=0)
    headings_score = db.Column(db.Float, default=0.0)
    img_total = db.Column(db.Integer, default=0)
    img_without_alt = db.Column(db.Integer, default=0)
    images_score = db.Column(db.Float, default=0.0)
    internal_links = db.Column(db.Integer, default=0)
    external_links = db.Column(db.Integer, default=0)
    links_score = db.Column(db.Float, default=0.0)
    has_canonical = db.Column(db.Boolean, default=False)
    has_og_tags = db.Column(db.Boolean, default=False)
    has_robots_meta = db.Column(db.Boolean, default=False)
    url_score = db.Column(db.Float, default=0.0)
    keyword_density = db.Column(db.Text)
    heading_structure = db.Column(db.Text)
    issues_json = db.Column(db.Text)

    def to_dict(self):
        import json
        return {
            'title_length': self.title_length,
            'title_score': self.title_score,
            'meta_desc_length': self.meta_desc_length,
            'meta_desc_score': self.meta_desc_score,
            'h1_count': self.h1_count,
            'h2_count': self.h2_count,
            'headings_score': self.headings_score,
            'img_total': self.img_total,
            'img_without_alt': self.img_without_alt,
            'images_score': self.images_score,
            'internal_links': self.internal_links,
            'external_links': self.external_links,
            'links_score': self.links_score,
            'has_canonical': self.has_canonical,
            'has_og_tags': self.has_og_tags,
            'has_robots_meta': self.has_robots_meta,
            'url_score': self.url_score,
            'keyword_density': json.loads(self.keyword_density) if self.keyword_density else [],
            'heading_structure': json.loads(self.heading_structure) if self.heading_structure else [],
            'issues': json.loads(self.issues_json) if self.issues_json else [],
        }


class AIRecommendation(db.Model):
    __tablename__ = 'ai_recommendations'

    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analyses.id'), nullable=False)
    category = db.Column(db.Text)
    priority = db.Column(db.Text)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    ai_model = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'category': self.category,
            'priority': self.priority,
            'title': self.title,
            'description': self.description,
            'ai_model': self.ai_model,
        }
