/* Results page logic */

document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('results-container');
    if (!container) return;

    const analysisId = container.dataset.analysisId;
    if (!analysisId) return;

    loadResults(analysisId);
});

async function loadResults(analysisId) {
    try {
        const response = await fetch(`/api/analysis/${analysisId}`);
        const data = await response.json();

        if (!data.success) {
            showNotification(data.error || 'Failed to load results', 'error');
            return;
        }

        const analysis = data.analysis;
        renderResults(analysis, analysisId);
    } catch (err) {
        showNotification('Failed to load results', 'error');
    }
}

function renderResults(analysis, analysisId) {
    document.getElementById('results-loading').classList.add('hidden');
    document.getElementById('results-content').classList.remove('hidden');

    // Header info
    document.getElementById('result-url').textContent = analysis.url;
    document.getElementById('result-date').textContent = formatDate(analysis.timestamp);

    // Export links
    document.getElementById('export-json-btn').href = `/api/analysis/${analysisId}/export/json`;
    document.getElementById('export-pdf-btn').href = `/api/analysis/${analysisId}/export/pdf`;

    // Scores
    renderDoughnutScore('overall-score-chart', analysis.overall_score);
    document.getElementById('overall-score-text').textContent = Math.round(analysis.overall_score);
    document.getElementById('overall-score-text').className = `text-3xl font-bold ${getScoreTextClass(analysis.overall_score)}`;

    renderScoreBar('seo-score-bar', 'seo-score-text', analysis.seo_score);
    renderScoreBar('content-score-bar', 'content-score-text', analysis.content_score);
    renderScoreBar('technical-score-bar', 'technical-score-text', analysis.technical_score);

    // SEO Details
    if (analysis.seo_details) {
        renderSEODetails(analysis.seo_details);
    }

    // Content Details
    renderContentDetails(analysis);

    // Issues
    if (analysis.seo_details && analysis.seo_details.issues) {
        renderIssues(analysis.seo_details.issues);
    }

    // AI Recommendations
    renderAIRecommendations(analysis.ai_recommendations);
}

function renderSEODetails(seo) {
    const grid = document.getElementById('seo-details-grid');
    const items = [
        { label: 'Title Tag', value: `${seo.title_length} chars`, score: seo.title_score },
        { label: 'Meta Description', value: `${seo.meta_desc_length} chars`, score: seo.meta_desc_score },
        { label: 'Headings', value: `H1: ${seo.h1_count}, H2: ${seo.h2_count}`, score: seo.headings_score },
        { label: 'Images', value: `${seo.img_total} total, ${seo.img_without_alt} missing alt`, score: seo.images_score },
        { label: 'Links', value: `${seo.internal_links} internal, ${seo.external_links} external`, score: seo.links_score },
        { label: 'URL Structure', value: '-', score: seo.url_score },
        { label: 'Canonical URL', value: seo.has_canonical ? 'Present' : 'Missing', score: seo.has_canonical ? 100 : 0 },
        { label: 'Open Graph Tags', value: seo.has_og_tags ? 'Present' : 'Missing', score: seo.has_og_tags ? 100 : 0 },
    ];

    grid.innerHTML = items.map(item => `
        <div class="bg-gray-50 rounded-lg p-4">
            <div class="flex justify-between items-start mb-2">
                <span class="text-sm font-medium text-gray-700">${item.label}</span>
                <span class="text-sm font-bold ${getScoreTextClass(item.score)}">${Math.round(item.score)}/100</span>
            </div>
            <p class="text-xs text-gray-500">${item.value}</p>
            <div class="w-full bg-gray-200 rounded-full h-1.5 mt-2">
                <div class="h-1.5 rounded-full ${getScoreBgClass(item.score)}" style="width: ${item.score}%"></div>
            </div>
        </div>
    `).join('');
}

function renderContentDetails(analysis) {
    const container = document.getElementById('content-details');
    const items = [
        { label: 'Word Count', value: analysis.word_count || 0 },
        { label: 'Language', value: (analysis.language || 'Unknown').toUpperCase() },
        { label: 'Response Time', value: analysis.response_time ? `${analysis.response_time.toFixed(2)}s` : 'N/A' },
        { label: 'Status', value: analysis.status },
    ];

    container.innerHTML = items.map(item => `
        <div class="bg-gray-50 rounded-lg p-4 text-center">
            <p class="text-2xl font-bold text-gray-900">${item.value}</p>
            <p class="text-xs text-gray-500 mt-1">${item.label}</p>
        </div>
    `).join('');
}

function renderIssues(issues) {
    const list = document.getElementById('issues-list');
    const noIssues = document.getElementById('no-issues');

    if (!issues || issues.length === 0) {
        noIssues.classList.remove('hidden');
        return;
    }

    const severityColors = {
        high: 'border-red-400 bg-red-50',
        medium: 'border-yellow-400 bg-yellow-50',
        low: 'border-blue-400 bg-blue-50',
    };

    const severityIcons = {
        high: '<span class="text-red-500 font-bold">!</span>',
        medium: '<span class="text-yellow-500 font-bold">~</span>',
        low: '<span class="text-blue-500 font-bold">i</span>',
    };

    list.innerHTML = issues.map(issue => `
        <div class="border-l-4 ${severityColors[issue.severity] || severityColors.low} p-3 rounded-r-lg">
            <div class="flex items-start gap-2">
                ${severityIcons[issue.severity] || severityIcons.low}
                <div>
                    <p class="text-sm font-medium text-gray-800">${issue.category || ''}</p>
                    <p class="text-sm text-gray-600">${issue.message}</p>
                </div>
            </div>
        </div>
    `).join('');
}

function renderAIRecommendations(recommendations) {
    const container = document.getElementById('ai-recommendations');
    const noAI = document.getElementById('no-ai');

    if (!recommendations || recommendations.length === 0) {
        noAI.classList.remove('hidden');
        return;
    }

    const priorityColors = {
        high: 'border-red-400 bg-red-50',
        medium: 'border-yellow-400 bg-yellow-50',
        low: 'border-green-400 bg-green-50',
    };

    const priorityLabels = {
        high: '<span class="px-2 py-0.5 text-xs font-medium bg-red-100 text-red-700 rounded-full">High Priority</span>',
        medium: '<span class="px-2 py-0.5 text-xs font-medium bg-yellow-100 text-yellow-700 rounded-full">Medium Priority</span>',
        low: '<span class="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-700 rounded-full">Low Priority</span>',
    };

    container.innerHTML = recommendations.map(rec => `
        <div class="border-l-4 ${priorityColors[rec.priority] || 'border-gray-400 bg-gray-50'} p-4 rounded-r-lg">
            <div class="flex items-center gap-2 mb-1">
                ${priorityLabels[rec.priority] || ''}
                <span class="text-xs text-gray-400 uppercase">${rec.category || ''}</span>
            </div>
            <h4 class="font-medium text-gray-900">${rec.title}</h4>
            <p class="text-sm text-gray-600 mt-1">${rec.description}</p>
        </div>
    `).join('');
}
