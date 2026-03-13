"""AI-powered analysis using OpenAI GPT."""

import json
import logging

logger = logging.getLogger(__name__)


class AIAnalyzer:
    """Uses OpenAI GPT to generate intelligent content analysis."""

    MAX_CONTENT_CHARS = 4000

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.client = None
        self.model = 'gpt-4'
        self.available = False

        if api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=api_key)
                self.available = True
            except Exception as e:
                logger.warning(f'OpenAI initialization failed: {e}')

    def _call_gpt(self, system_prompt, user_prompt):
        """Make a GPT API call and return parsed JSON response."""
        if not self.available:
            return None

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt},
                ],
                response_format={'type': 'json_object'},
                temperature=0.3,
                max_tokens=2000,
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            logger.error(f'OpenAI API error: {e}')
            return None

    def analyze_content_quality(self, text, url):
        """Ask GPT to evaluate content quality."""
        truncated = text[:self.MAX_CONTENT_CHARS]

        system_prompt = (
            'You are a senior web content analyst and SEO expert. '
            'Analyze the provided web page content and return a JSON response with: '
            '{"score": <0-100>, "assessment": "<brief assessment>", '
            '"strengths": ["<strength1>", ...], "weaknesses": ["<weakness1>", ...]}'
        )

        user_prompt = f'URL: {url}\n\nContent:\n{truncated}'

        result = self._call_gpt(system_prompt, user_prompt)
        if result:
            return result
        return {'score': 50, 'assessment': 'AI analysis not available', 'strengths': [], 'weaknesses': []}

    def generate_seo_recommendations(self, seo_data, content):
        """Ask GPT to generate prioritized SEO recommendations."""
        truncated_content = content[:2000]

        issues_text = ''
        if seo_data.get('issues'):
            issues_text = '\n'.join(
                f'- [{i["severity"]}] {i["category"]}: {i["message"]}'
                for i in seo_data['issues'][:10]
            )

        system_prompt = (
            'You are a senior SEO consultant. Based on the analysis results, '
            'generate specific, actionable recommendations. '
            'Return JSON: {"recommendations": [{"category": "<seo|content|technical|ux>", '
            '"priority": "<high|medium|low>", "title": "<short title>", '
            '"description": "<detailed actionable advice>"}]}'
        )

        user_prompt = (
            f'SEO Score: {seo_data.get("overall_score", 0)}/100\n\n'
            f'Issues Found:\n{issues_text}\n\n'
            f'Page Content (excerpt):\n{truncated_content}'
        )

        result = self._call_gpt(system_prompt, user_prompt)
        if result and 'recommendations' in result:
            return result['recommendations']
        return []

    def generate_meta_suggestions(self, current_title, current_desc, content):
        """Ask GPT to suggest improved title and meta description."""
        truncated = content[:2000]

        system_prompt = (
            'You are an SEO copywriting expert. Suggest an improved title tag (30-60 chars) '
            'and meta description (120-160 chars) based on the page content. '
            'Return JSON: {"suggested_title": "<title>", "suggested_description": "<desc>", '
            '"reasoning": "<why these are better>"}'
        )

        user_prompt = (
            f'Current title: {current_title}\n'
            f'Current description: {current_desc}\n\n'
            f'Content:\n{truncated}'
        )

        result = self._call_gpt(system_prompt, user_prompt)
        return result

    def run_full_ai_analysis(self, scraped_data, seo_results, content_results):
        """Orchestrate all AI analysis calls."""
        if not self.available:
            return {
                'available': False,
                'message': 'OpenAI API key not configured. Set OPENAI_API_KEY to enable AI analysis.',
                'recommendations': [],
                'content_quality': None,
                'meta_suggestions': None,
            }

        text = scraped_data.get('text_content', '')
        url = scraped_data.get('url', '')

        content_quality = self.analyze_content_quality(text, url)
        recommendations = self.generate_seo_recommendations(seo_results, text)
        meta_suggestions = self.generate_meta_suggestions(
            scraped_data.get('title', ''),
            scraped_data.get('meta_description', ''),
            text,
        )

        return {
            'available': True,
            'recommendations': recommendations,
            'content_quality': content_quality,
            'meta_suggestions': meta_suggestions,
        }
