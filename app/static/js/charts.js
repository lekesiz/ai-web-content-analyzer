/* Chart.js visualization helpers */

function renderDoughnutScore(canvasId, score) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const color = getScoreColor(score);

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: [color, '#f3f4f6'],
                borderWidth: 0,
            }],
        },
        options: {
            cutout: '75%',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false },
            },
        },
    });
}

function renderScoreBar(barId, textId, score) {
    const bar = document.getElementById(barId);
    const text = document.getElementById(textId);
    if (!bar || !text) return;

    const color = getScoreBgClass(score);
    const textColor = getScoreTextClass(score);

    text.textContent = Math.round(score);
    text.className = `text-3xl font-bold mb-2 ${textColor}`;
    bar.style.width = `${score}%`;
    bar.className = `h-2 rounded-full transition-all duration-500 ${color}`;
}

function renderRadarChart(canvasId, categories) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: Object.keys(categories),
            datasets: [{
                data: Object.values(categories),
                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(59, 130, 246, 1)',
            }],
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: { stepSize: 20 },
                },
            },
        },
    });
}
