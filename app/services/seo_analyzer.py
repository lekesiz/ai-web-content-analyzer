"""SEO analysis module with scoring for web pages."""

import json
import re
from collections import Counter
from urllib.parse import urlparse

# Common stop words for English and French
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
    'with', 'by', 'from', 'is', 'was', 'are', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
    'may', 'might', 'shall', 'can', 'this', 'that', 'these', 'those', 'it', 'its',
    'not', 'no', 'nor', 'as', 'if', 'then', 'than', 'too', 'very', 'just',
    'about', 'up', 'out', 'so', 'he', 'she', 'they', 'we', 'you', 'i', 'my',
    'your', 'his', 'her', 'our', 'their', 'what', 'which', 'who', 'when', 'where',
    'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some',
    'such', 'only', 'own', 'same', 'also', 'into', 'over', 'after', 'before',
    # French stop words
    'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'et', 'est', 'en', 'que',
    'qui', 'dans', 'ce', 'il', 'ne', 'se', 'son', 'sur', 'au', 'aux', 'avec',
    'pas', 'pour', 'par', 'plus', 'nous', 'vous', 'ils', 'elle', 'mais', 'ou',
    'si', 'sa', 'ses', 'tout', 'cette', 'ces', 'ont', 'sont', 'leur', 'fait',
}


class SEOAnalyzer:
    """Analyzes scraped page data for SEO quality."""

    TITLE_MIN = 30
    TITLE_MAX = 60
    META_DESC_MIN = 120
    META_DESC_MAX = 160
    KEYWORD_DENSITY_MAX = 3.0

    def __init__(self, scraped_data, url):
        self.data = scraped_data
        self.url = url
        self.issues = []

    def analyze_title(self):
        title = self.data.get('title', '')
        length = len(title)
        score = 100

        if not title:
            score = 0
            self.issues.append({'severity': 'high', 'category': 'Title Tag', 'message': 'Missing title tag'})
        elif length < self.TITLE_MIN:
            score = 50
            self.issues.append({'severity': 'medium', 'category': 'Title Tag', 'message': f'Title too short ({length} chars). Recommended: {self.TITLE_MIN}-{self.TITLE_MAX} characters.'})
        elif length > self.TITLE_MAX:
            score = 70
            self.issues.append({'severity': 'low', 'category': 'Title Tag', 'message': f'Title too long ({length} chars). May be truncated in search results.'})

        return {'score': score, 'length': length, 'title': title}

    def analyze_meta_description(self):
        desc = self.data.get('meta_description', '')
        length = len(desc)
        score = 100

        if not desc:
            score = 0
            self.issues.append({'severity': 'high', 'category': 'Meta Description', 'message': 'Missing meta description'})
        elif length < self.META_DESC_MIN:
            score = 50
            self.issues.append({'severity': 'medium', 'category': 'Meta Description', 'message': f'Meta description too short ({length} chars). Recommended: {self.META_DESC_MIN}-{self.META_DESC_MAX} characters.'})
        elif length > self.META_DESC_MAX:
            score = 70
            self.issues.append({'severity': 'low', 'category': 'Meta Description', 'message': f'Meta description too long ({length} chars). May be truncated.'})

        return {'score': score, 'length': length}

    def analyze_headings(self):
        headings = self.data.get('headings', [])
        h1_tags = [h for h in headings if h['tag'] == 'h1']
        h2_tags = [h for h in headings if h['tag'] == 'h2']
        score = 100

        if len(h1_tags) == 0:
            score -= 40
            self.issues.append({'severity': 'high', 'category': 'Headings', 'message': 'Missing H1 tag'})
        elif len(h1_tags) > 1:
            score -= 20
            self.issues.append({'severity': 'medium', 'category': 'Headings', 'message': f'Multiple H1 tags found ({len(h1_tags)}). Use only one H1 per page.'})

        if len(h2_tags) == 0:
            score -= 15
            self.issues.append({'severity': 'low', 'category': 'Headings', 'message': 'No H2 tags found. Use H2 tags to structure your content.'})

        # Check heading hierarchy
        prev_level = 0
        for h in headings:
            level = int(h['tag'][1])
            if level > prev_level + 1 and prev_level > 0:
                score -= 10
                self.issues.append({'severity': 'low', 'category': 'Headings', 'message': f'Skipped heading level: H{prev_level} to H{level}'})
                break
            prev_level = level

        structure = [{'tag': h['tag'], 'text': h['text'][:80]} for h in headings]
        return {
            'score': max(0, score),
            'h1_count': len(h1_tags),
            'h2_count': len(h2_tags),
            'structure': structure,
        }

    def analyze_images(self):
        images = self.data.get('images', [])
        total = len(images)
        without_alt = sum(1 for img in images if not img.get('has_alt', False))
        score = 100

        if total == 0:
            return {'score': 100, 'total': 0, 'without_alt': 0}

        missing_pct = (without_alt / total) * 100 if total > 0 else 0

        if without_alt > 0:
            score = max(0, 100 - int(missing_pct))
            severity = 'high' if missing_pct > 50 else 'medium'
            self.issues.append({'severity': severity, 'category': 'Images', 'message': f'{without_alt} of {total} images missing alt text ({missing_pct:.0f}%)'})

        return {'score': score, 'total': total, 'without_alt': without_alt}

    def analyze_links(self):
        links = self.data.get('links', [])
        internal = sum(1 for l in links if l.get('is_internal'))
        external = sum(1 for l in links if not l.get('is_internal'))
        score = 100

        if len(links) == 0:
            score = 40
            self.issues.append({'severity': 'medium', 'category': 'Links', 'message': 'No links found on the page'})
        elif internal < 3:
            score -= 20
            self.issues.append({'severity': 'medium', 'category': 'Links', 'message': f'Only {internal} internal links. Add more internal links for better SEO.'})

        if external == 0 and len(links) > 0:
            score -= 10
            self.issues.append({'severity': 'low', 'category': 'Links', 'message': 'No external links. Consider adding relevant outbound links.'})

        return {'score': max(0, score), 'internal': internal, 'external': external}

    def analyze_url_structure(self):
        parsed = urlparse(self.url)
        path = parsed.path
        score = 100

        if len(self.url) > 100:
            score -= 15
            self.issues.append({'severity': 'low', 'category': 'URL', 'message': 'URL is very long. Shorter URLs are preferred for SEO.'})

        if '_' in path:
            score -= 10
            self.issues.append({'severity': 'low', 'category': 'URL', 'message': 'URL contains underscores. Use hyphens instead for better SEO.'})

        if any(c.isupper() for c in path):
            score -= 5
            self.issues.append({'severity': 'low', 'category': 'URL', 'message': 'URL contains uppercase characters. Use lowercase for consistency.'})

        if parsed.query:
            score -= 10
            self.issues.append({'severity': 'low', 'category': 'URL', 'message': 'URL contains query parameters. Clean URLs are preferred.'})

        return {'score': max(0, score)}

    def analyze_keyword_density(self):
        text = self.data.get('text_content', '')
        words = re.findall(r'\b[a-zA-ZÀ-ÿ]{3,}\b', text.lower())
        total = len(words)

        if total == 0:
            return {'score': 50, 'keywords': []}

        filtered = [w for w in words if w not in STOP_WORDS]
        counter = Counter(filtered)
        top_keywords = []
        score = 100

        for word, count in counter.most_common(10):
            density = (count / total) * 100
            top_keywords.append({
                'word': word,
                'count': count,
                'density': round(density, 2),
            })
            if density > self.KEYWORD_DENSITY_MAX:
                score -= 10
                if len([k for k in top_keywords if k['density'] > self.KEYWORD_DENSITY_MAX]) == 1:
                    self.issues.append({'severity': 'medium', 'category': 'Keywords', 'message': f'Keyword "{word}" density is {density:.1f}% (max recommended: {self.KEYWORD_DENSITY_MAX}%)'})

        return {'score': max(0, score), 'keywords': top_keywords}

    def analyze_social_tags(self):
        og_tags = self.data.get('og_tags', {})
        score = 100

        if not og_tags:
            score = 0
            self.issues.append({'severity': 'medium', 'category': 'Social Tags', 'message': 'No Open Graph tags found. Add og:title, og:description, og:image for better social sharing.'})
        else:
            required = ['og:title', 'og:description', 'og:image']
            missing = [t for t in required if t not in og_tags]
            if missing:
                score -= len(missing) * 25
                self.issues.append({'severity': 'low', 'category': 'Social Tags', 'message': f'Missing Open Graph tags: {", ".join(missing)}'})

        return {'score': max(0, score), 'og_tags': og_tags}

    def analyze_canonical(self):
        canonical = self.data.get('canonical_url', '')
        score = 100 if canonical else 0
        if not canonical:
            self.issues.append({'severity': 'medium', 'category': 'Canonical', 'message': 'No canonical URL defined. Add a canonical tag to prevent duplicate content issues.'})
        return {'score': score, 'has_canonical': bool(canonical)}

    def analyze_robots(self):
        robots = self.data.get('robots_meta', '')
        score = 100
        has_robots = bool(robots)

        if robots and ('noindex' in robots.lower()):
            score = 20
            self.issues.append({'severity': 'high', 'category': 'Robots', 'message': 'Page has noindex directive. It will NOT appear in search results.'})

        return {'score': score, 'has_robots': has_robots, 'content': robots}

    def run_full_analysis(self):
        """Run all SEO checks and compute weighted score."""
        title_result = self.analyze_title()
        meta_result = self.analyze_meta_description()
        headings_result = self.analyze_headings()
        images_result = self.analyze_images()
        links_result = self.analyze_links()
        url_result = self.analyze_url_structure()
        keywords_result = self.analyze_keyword_density()
        social_result = self.analyze_social_tags()
        canonical_result = self.analyze_canonical()
        robots_result = self.analyze_robots()

        # Weighted scoring
        weights = {
            'title': 15, 'meta': 10, 'headings': 15, 'images': 10,
            'links': 10, 'url': 10, 'keywords': 10, 'social': 10,
            'canonical': 5, 'robots': 5,
        }
        scores = {
            'title': title_result['score'],
            'meta': meta_result['score'],
            'headings': headings_result['score'],
            'images': images_result['score'],
            'links': links_result['score'],
            'url': url_result['score'],
            'keywords': keywords_result['score'],
            'social': social_result['score'],
            'canonical': canonical_result['score'],
            'robots': robots_result['score'],
        }

        total_weight = sum(weights.values())
        overall = sum(scores[k] * weights[k] for k in weights) / total_weight

        return {
            'overall_score': round(overall, 1),
            'title': title_result,
            'meta_description': meta_result,
            'headings': headings_result,
            'images': images_result,
            'links': links_result,
            'url': url_result,
            'keywords': keywords_result,
            'social': social_result,
            'canonical': canonical_result,
            'robots': robots_result,
            'issues': self.issues,
            'heading_structure': json.dumps(headings_result.get('structure', [])),
            'keyword_density': json.dumps(keywords_result.get('keywords', [])),
        }
