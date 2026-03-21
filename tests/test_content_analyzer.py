"""Tests for the content analyzer service."""

from app.services.content_analyzer import ContentAnalyzer, _count_syllables


class TestSyllableCounter:
    """Tests for the syllable counting utility."""

    def test_one_syllable_words(self):
        assert _count_syllables('cat') == 1
        assert _count_syllables('dog') == 1
        assert _count_syllables('run') == 1

    def test_two_syllable_words(self):
        assert _count_syllables('happy') >= 1
        assert _count_syllables('water') >= 1

    def test_multi_syllable_words(self):
        assert _count_syllables('beautiful') >= 2
        assert _count_syllables('development') >= 3

    def test_short_words(self):
        assert _count_syllables('a') == 1
        assert _count_syllables('it') == 1
        assert _count_syllables('the') == 1


class TestContentAnalyzerBasicStats:
    """Tests for basic text statistics."""

    def test_basic_stats_normal_text(self):
        text = "This is a test sentence. Here is another one. And a third sentence too."
        analyzer = ContentAnalyzer(text)
        stats = analyzer.basic_stats()

        assert stats['word_count'] > 0
        assert stats['sentence_count'] == 3
        assert stats['avg_sentence_length'] > 0
        assert 0 <= stats['vocabulary_richness'] <= 1

    def test_basic_stats_empty_text(self):
        analyzer = ContentAnalyzer('')
        stats = analyzer.basic_stats()
        assert stats['word_count'] == 0
        assert stats['sentence_count'] == 0
        assert stats['vocabulary_richness'] == 0

    def test_paragraph_count(self):
        paragraphs = ['First paragraph.', 'Second paragraph.', 'Third paragraph.']
        analyzer = ContentAnalyzer('Full text here.', paragraphs=paragraphs)
        stats = analyzer.basic_stats()
        assert stats['paragraph_count'] == 3


class TestContentAnalyzerReadability:
    """Tests for readability score calculations."""

    def test_readability_with_sufficient_text(self):
        text = (
            "The quick brown fox jumps over the lazy dog. "
            "This sentence is used to test the readability analysis module. "
            "It contains multiple sentences with varying complexity levels. "
            "Some sentences are short. Others are deliberately constructed to be "
            "longer and more complex to test the various readability metrics."
        )
        analyzer = ContentAnalyzer(text)
        scores = analyzer.readability_scores()

        assert 'flesch_reading_ease' in scores
        assert 'flesch_kincaid_grade' in scores
        assert 'gunning_fog' in scores
        assert 'coleman_liau_index' in scores
        assert 'automated_readability_index' in scores
        assert scores['reading_time_minutes'] > 0
        assert scores['interpretation'] != 'Not enough text to analyze'

    def test_readability_with_too_little_text(self):
        analyzer = ContentAnalyzer('Just a few words.')
        scores = analyzer.readability_scores()
        assert scores['flesch_reading_ease'] == 0
        assert scores['interpretation'] == 'Not enough text to analyze'

    def test_easy_text_readability(self):
        easy_text = "The cat sat on the mat. " * 10
        analyzer = ContentAnalyzer(easy_text)
        scores = analyzer.readability_scores()
        assert scores['flesch_reading_ease'] > 50

    def test_reading_time_calculation(self):
        # ~200 words should be about 1 minute
        words = "word " * 200
        analyzer = ContentAnalyzer(words)
        scores = analyzer.readability_scores()
        assert 0.5 <= scores['reading_time_minutes'] <= 1.5


class TestContentAnalyzerLanguage:
    """Tests for language detection."""

    def test_detect_english(self):
        text = "This is a sample text written in English for testing purposes."
        analyzer = ContentAnalyzer(text)
        result = analyzer.detect_language()
        assert result['language'] == 'en'
        assert result['confidence'] > 0

    def test_detect_french(self):
        text = "Ceci est un exemple de texte en francais pour tester la detection de langue."
        analyzer = ContentAnalyzer(text)
        result = analyzer.detect_language()
        assert result['language'] == 'fr'

    def test_detect_insufficient_text(self):
        analyzer = ContentAnalyzer('Hi')
        result = analyzer.detect_language()
        assert result['language'] == 'unknown'


class TestContentAnalyzerStructure:
    """Tests for content structure quality analysis."""

    def test_good_structure(self):
        paragraphs = [f'Paragraph {i} with some content.' for i in range(5)]
        text = ' '.join(['word'] * 500)
        analyzer = ContentAnalyzer(text, paragraphs=paragraphs, html_length=5000)
        result = analyzer.content_structure_quality()
        assert result['score'] > 50

    def test_few_paragraphs(self):
        analyzer = ContentAnalyzer('Short text.', paragraphs=['One.'], html_length=100)
        result = analyzer.content_structure_quality()
        assert result['score'] < 100

    def test_low_word_count(self):
        text = ' '.join(['word'] * 50)
        analyzer = ContentAnalyzer(text, paragraphs=['p1', 'p2', 'p3'], html_length=500)
        result = analyzer.content_structure_quality()
        assert any('words' in str(i.get('message', '')) for i in result['issues'])

    def test_long_paragraphs_flagged(self):
        long_para = ' '.join(['word'] * 150)
        analyzer = ContentAnalyzer(long_para, paragraphs=[long_para], html_length=1000)
        result = analyzer.content_structure_quality()
        assert result['long_paragraphs'] == 1


class TestContentAnalyzerFullAnalysis:
    """Tests for the full content analysis pipeline."""

    def test_full_analysis_returns_all_sections(self):
        text = (
            "Web development is the process of building websites and web applications. "
            "It involves frontend development with HTML, CSS, and JavaScript. "
            "Backend development uses server-side languages like Python, Java, or Node.js. "
            "Modern web development also includes responsive design and accessibility. "
            "Testing and deployment are crucial parts of the development lifecycle."
        )
        paragraphs = [text]
        analyzer = ContentAnalyzer(text, paragraphs=paragraphs, html_length=len(text) * 3)
        result = analyzer.run_full_analysis()

        assert 'score' in result
        assert 'stats' in result
        assert 'readability' in result
        assert 'language' in result
        assert 'structure' in result
        assert 0 <= result['score'] <= 100

    def test_full_analysis_score_reasonable_for_good_content(self):
        good_text = ' '.join([
            "The importance of search engine optimization cannot be overstated.",
            "Good SEO practices help websites rank higher in search results.",
            "This includes proper use of meta tags, heading hierarchy, and quality content.",
            "Internal linking and mobile responsiveness are also key factors.",
            "Regular content updates signal to search engines that a site is active.",
        ] * 10)
        paragraphs = good_text.split('. ')
        analyzer = ContentAnalyzer(good_text, paragraphs=paragraphs, html_length=len(good_text) * 2)
        result = analyzer.run_full_analysis()
        assert result['score'] > 30
