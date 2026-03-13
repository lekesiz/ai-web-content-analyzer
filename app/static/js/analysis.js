/* Analysis form handling */

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('analyze-form');
    if (!form) return;

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const urlInput = document.getElementById('url-input');
        const btn = document.getElementById('analyze-btn');
        const btnText = document.getElementById('btn-text');
        const btnLoading = document.getElementById('btn-loading');
        const url = urlInput.value.trim();

        if (!url) {
            showNotification('Please enter a URL', 'warning');
            return;
        }

        // Show loading state
        btn.disabled = true;
        btnText.classList.add('hidden');
        btnLoading.classList.remove('hidden');

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url }),
            });

            const data = await response.json();

            if (data.success && data.analysis_id) {
                window.location.href = `/results/${data.analysis_id}`;
            } else {
                showNotification(data.error || 'Analysis failed', 'error');
            }
        } catch (err) {
            showNotification('Network error. Please try again.', 'error');
        } finally {
            btn.disabled = false;
            btnText.classList.remove('hidden');
            btnLoading.classList.add('hidden');
        }
    });

    // Load recent analyses
    loadRecentAnalyses();
});

async function loadRecentAnalyses() {
    try {
        const response = await fetch('/api/history?limit=5');
        const data = await response.json();

        if (data.analyses && data.analyses.length > 0) {
            const container = document.getElementById('recent-analyses');
            const list = document.getElementById('recent-list');
            container.classList.remove('hidden');

            list.innerHTML = data.analyses.map(a => `
                <a href="/results/${a.id}" class="block bg-white rounded-lg shadow-sm p-4 hover:shadow-md transition">
                    <div class="flex justify-between items-center">
                        <div>
                            <p class="text-sm font-medium text-gray-900">${truncateUrl(a.url)}</p>
                            <p class="text-xs text-gray-400">${formatDate(a.timestamp)}</p>
                        </div>
                        <div class="text-right">
                            <span class="text-lg font-bold ${getScoreTextClass(a.overall_score)}">${Math.round(a.overall_score)}</span>
                            <span class="text-xs text-gray-400">/100</span>
                        </div>
                    </div>
                </a>
            `).join('');
        }
    } catch (err) {
        // Silently fail for recent analyses
    }
}
