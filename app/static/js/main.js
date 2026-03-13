/* Main utility functions */

function showNotification(message, type = 'info') {
    const container = document.getElementById('notification-container');
    const colors = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        info: 'bg-blue-500',
        warning: 'bg-yellow-500 text-black',
    };
    const div = document.createElement('div');
    div.className = `${colors[type] || colors.info} text-white px-6 py-3 rounded-lg shadow-lg text-sm font-medium transition-all transform translate-x-0`;
    div.textContent = message;
    container.appendChild(div);
    setTimeout(() => {
        div.classList.add('opacity-0', 'translate-x-4');
        setTimeout(() => div.remove(), 300);
    }, 4000);
}

function formatDate(isoString) {
    const date = new Date(isoString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}

function getScoreColor(score) {
    if (score >= 80) return '#22c55e';
    if (score >= 60) return '#84cc16';
    if (score >= 40) return '#eab308';
    if (score >= 20) return '#f97316';
    return '#ef4444';
}

function getScoreLabel(score) {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Needs Improvement';
    if (score >= 20) return 'Poor';
    return 'Critical';
}

function getScoreBgClass(score) {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-lime-500';
    if (score >= 40) return 'bg-yellow-500';
    if (score >= 20) return 'bg-orange-500';
    return 'bg-red-500';
}

function getScoreTextClass(score) {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-lime-600';
    if (score >= 40) return 'text-yellow-600';
    if (score >= 20) return 'text-orange-600';
    return 'text-red-600';
}

function truncateUrl(url, maxLength = 60) {
    if (url.length <= maxLength) return url;
    return url.substring(0, maxLength) + '...';
}
