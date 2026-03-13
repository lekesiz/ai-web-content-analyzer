import pytest
from app import create_app, db as _db


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_scraped_data():
    return {
        'url': 'https://example.com',
        'status_code': 200,
        'response_time': 0.5,
        'content_type': 'text/html',
        'title': 'Example Domain - Best Practices for Web Development',
        'meta_description': 'Learn about web development best practices with our comprehensive guide covering HTML, CSS, and JavaScript.',
        'meta_keywords': 'web development, HTML, CSS, JavaScript',
        'canonical_url': 'https://example.com',
        'og_tags': {
            'og:title': 'Example Domain',
            'og:description': 'A comprehensive guide',
        },
        'headings': [
            {'tag': 'h1', 'text': 'Example Domain'},
            {'tag': 'h2', 'text': 'Getting Started'},
            {'tag': 'h2', 'text': 'Best Practices'},
            {'tag': 'h3', 'text': 'HTML Tips'},
        ],
        'paragraphs': [
            'This is the first paragraph with enough content to analyze properly.',
            'The second paragraph discusses web development best practices in detail.',
            'Another paragraph covering important topics for developers.',
        ],
        'links': [
            {'href': '/about', 'text': 'About', 'is_internal': True, 'has_nofollow': False},
            {'href': '/contact', 'text': 'Contact', 'is_internal': True, 'has_nofollow': False},
            {'href': 'https://external.com', 'text': 'External', 'is_internal': False, 'has_nofollow': False},
        ],
        'images': [
            {'src': '/img/hero.jpg', 'alt': 'Hero image', 'has_alt': True},
            {'src': '/img/logo.png', 'alt': '', 'has_alt': False},
        ],
        'text_content': 'This is the full text content of the page. It contains multiple sentences about web development. Best practices include proper HTML structure, semantic markup, and accessible design. The content should be informative and well-organized.',
        'word_count': 150,
        'robots_meta': 'index, follow',
        'lang': 'en',
        'scripts_count': 3,
        'stylesheets_count': 2,
    }
