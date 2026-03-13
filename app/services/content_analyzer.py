"""Content and readability analysis module."""

import re
import math
from langdetect import detect, DetectorFactory, LangDetectException

# Ensure consistent language detection
DetectorFactory.seed = 0


def _count_syllables(word):
    """Count syllables in an English word (approximation)."""
    word = word.lower().strip()
    if len(word) <= 3:
        return 1
    word = re.sub(r'(?:es|ed|e)$', '', word) or word
    vowels = re.findall(r'[aeiouy]+', word)
    return max(1, len(vowels))


def _count_complex_words(words):
    """Count words with 3+ syllables."""
    return sum(1 for w in words if _count_syllables(w) >= 3)


class ContentAnalyzer:
    """Analyzes page content for readability and quality."""

    def __init__(self, text_content, paragraphs=None, headings=None, html_length=0):
        self.text = text_content or ''
        self.paragraphs = paragraphs or []
        self.headings = headings or []
        self.html_length = html_length

    def basic_stats(self):
        """Compute basic text statistics."""
        words = self.text.split()
        word_count = len(words)

        sentences = re.split(r'[.!?]+', self.text)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)

        unique_words = set(w.lower() for w in words if w.isalpha())

        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        avg_word_length = sum(len(w) for w in words) / word_count if word_count > 0 else 0
        vocabulary_richness = len(unique_words) / word_count if word_count > 0 else 0

        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'paragraph_count': len(self.paragraphs),
            'avg_sentence_length': round(avg_sentence_length, 1),
            'avg_word_length': round(avg_word_length, 1),
            'unique_words': len(unique_words),
            'vocabulary_richness': round(vocabulary_richness, 3),
        }

    def readability_scores(self):
        """Calculate readability metrics."""
        words = [w for w in self.text.split() if w.strip()]
        word_count = len(words)

        if word_count < 10:
            return {
                'flesch_reading_ease': 0,
                'flesch_kincaid_grade': 0,
                'gunning_fog': 0,
                'coleman_liau_index': 0,
                'automated_readability_index': 0,
                'reading_time_minutes': 0,
                'interpretation': 'Not enough text to analyze',
            }

        sentences = re.split(r'[.!?]+', self.text)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = max(1, len(sentences))

        total_syllables = sum(_count_syllables(w) for w in words if w.isalpha())
        total_chars = sum(len(w) for w in words if w.isalpha())
        alpha_words = [w for w in words if w.isalpha()]
        alpha_count = max(1, len(alpha_words))

        asl = word_count / sentence_count  # avg sentence length
        asw = total_syllables / alpha_count  # avg syllables per word

        # Flesch Reading Ease: 206.835 - 1.015*ASL - 84.6*ASW
        fre = 206.835 - (1.015 * asl) - (84.6 * asw)

        # Flesch-Kincaid Grade: 0.39*ASL + 11.8*ASW - 15.59
        fkg = (0.39 * asl) + (11.8 * asw) - 15.59

        # Gunning Fog: 0.4 * (ASL + 100 * complex_words/word_count)
        complex_count = _count_complex_words(alpha_words)
        gf = 0.4 * (asl + 100 * (complex_count / alpha_count))

        # Coleman-Liau: 0.0588*L - 0.296*S - 15.8
        # L = avg letters per 100 words, S = avg sentences per 100 words
        L = (total_chars / alpha_count) * 100
        S = (sentence_count / alpha_count) * 100
        cli = (0.0588 * L) - (0.296 * S) - 15.8

        # Automated Readability Index: 4.71*(chars/words) + 0.5*(words/sentences) - 21.43
        ari = 4.71 * (total_chars / alpha_count) + 0.5 * asl - 21.43

        reading_time = round(word_count / 200, 1)

        # Interpret Flesch Reading Ease
        if fre >= 80:
            interpretation = 'Very easy to read'
        elif fre >= 60:
            interpretation = 'Easy to read'
        elif fre >= 40:
            interpretation = 'Fairly difficult'
        elif fre >= 20:
            interpretation = 'Difficult to read'
        else:
            interpretation = 'Very difficult to read'

        return {
            'flesch_reading_ease': round(fre, 1),
            'flesch_kincaid_grade': round(fkg, 1),
            'gunning_fog': round(gf, 1),
            'coleman_liau_index': round(cli, 1),
            'automated_readability_index': round(ari, 1),
            'reading_time_minutes': reading_time,
            'interpretation': interpretation,
        }

    def detect_language(self):
        """Detect the language of the text."""
        if len(self.text.split()) < 5:
            return {'language': 'unknown', 'confidence': 0}

        try:
            lang = detect(self.text)
            return {'language': lang, 'confidence': 0.9}
        except LangDetectException:
            return {'language': 'unknown', 'confidence': 0}

    def content_structure_quality(self):
        """Evaluate content structure quality."""
        score = 100
        issues = []

        # Text to HTML ratio
        text_length = len(self.text)
        if self.html_length > 0:
            ratio = (text_length / self.html_length) * 100
            if ratio < 10:
                score -= 20
                issues.append({'severity': 'medium', 'category': 'Structure', 'message': f'Low text-to-HTML ratio ({ratio:.1f}%). Consider adding more content.'})
        else:
            ratio = 0

        # Check paragraph quality
        if len(self.paragraphs) < 3:
            score -= 15
            issues.append({'severity': 'low', 'category': 'Structure', 'message': 'Very few paragraphs. Break content into more sections.'})

        long_paragraphs = [p for p in self.paragraphs if len(p.split()) > 100]
        if long_paragraphs:
            score -= 10
            issues.append({'severity': 'low', 'category': 'Structure', 'message': f'{len(long_paragraphs)} paragraph(s) are very long. Consider breaking them up.'})

        # Word count adequacy
        word_count = len(self.text.split())
        if word_count < 300:
            score -= 20
            issues.append({'severity': 'medium', 'category': 'Content Length', 'message': f'Only {word_count} words. Aim for at least 300 words for better SEO.'})

        return {
            'score': max(0, score),
            'text_html_ratio': round(ratio, 1) if self.html_length > 0 else None,
            'paragraph_count': len(self.paragraphs),
            'long_paragraphs': len(long_paragraphs),
            'issues': issues,
        }

    def run_full_analysis(self):
        """Run complete content analysis."""
        stats = self.basic_stats()
        readability = self.readability_scores()
        language = self.detect_language()
        structure = self.content_structure_quality()

        # Weighted content score
        fre = readability.get('flesch_reading_ease', 0)
        readability_score = min(100, max(0, fre))

        word_count = stats['word_count']
        if word_count >= 1000:
            length_score = 100
        elif word_count >= 300:
            length_score = 70
        elif word_count >= 100:
            length_score = 40
        else:
            length_score = 20

        vocab_score = min(100, int(stats['vocabulary_richness'] * 200))

        content_score = (
            readability_score * 0.40 +
            length_score * 0.20 +
            vocab_score * 0.20 +
            structure['score'] * 0.20
        )

        all_issues = structure.get('issues', [])

        return {
            'score': round(content_score, 1),
            'stats': stats,
            'readability': readability,
            'language': language,
            'structure': structure,
            'issues': all_issues,
        }
