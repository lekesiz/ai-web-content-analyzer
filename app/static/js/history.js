/* History page logic */

let currentPage = 1;
let currentSort = 'timestamp';
let currentOrder = 'desc';
let searchTimeout = null;

document.addEventListener('DOMContentLoaded', function () {
    const tbody = document.getElementById('history-tbody');
    if (!tbody) return;

    loadHistory();

    const searchInput = document.getElementById('history-search');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                currentPage = 1;
                loadHistory();
            }, 300);
        });
    }
});

async function loadHistory() {
    const search = document.getElementById('history-search')?.value || '';
    const params = new URLSearchParams({
        page: currentPage,
        sort: currentSort,
        order: currentOrder,
        search: search,
        limit: 20,
    });

    try {
        const response = await fetch(`/api/history?${params}`);
        const data = await response.json();
        renderHistory(data);
    } catch (err) {
        showNotification('Failed to load history', 'error');
    }
}

function renderHistory(data) {
    const tbody = document.getElementById('history-tbody');
    const empty = document.getElementById('history-empty');
    const analyses = data.analyses || [];

    if (analyses.length === 0) {
        tbody.innerHTML = '';
        empty.classList.remove('hidden');
        return;
    }

    empty.classList.add('hidden');
    tbody.innerHTML = analyses.map(a => `
        <tr class="hover:bg-gray-50 transition">
            <td class="px-6 py-4">
                <a href="/results/${a.id}" class="text-sm text-blue-600 hover:underline">${truncateUrl(a.url, 50)}</a>
            </td>
            <td class="px-6 py-4">
                <span class="text-sm font-bold ${getScoreTextClass(a.overall_score)}">${Math.round(a.overall_score)}</span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-500">${formatDate(a.timestamp)}</td>
            <td class="px-6 py-4">
                <span class="px-2 py-1 text-xs rounded-full ${a.status === 'completed' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}">${a.status}</span>
            </td>
            <td class="px-6 py-4 text-right">
                <button onclick="deleteAnalysis(${a.id})" class="text-red-500 hover:text-red-700 text-sm">Delete</button>
            </td>
        </tr>
    `).join('');

    renderPagination(data.total, data.page, data.per_page);
}

function renderPagination(total, page, perPage) {
    const container = document.getElementById('history-pagination');
    const totalPages = Math.ceil(total / perPage);

    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }

    let html = '';
    for (let i = 1; i <= totalPages; i++) {
        const active = i === page ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-100';
        html += `<button onclick="goToPage(${i})" class="${active} px-3 py-1 rounded-md text-sm border">${i}</button>`;
    }
    container.innerHTML = html;
}

function goToPage(page) {
    currentPage = page;
    loadHistory();
}

function sortHistory(field) {
    if (currentSort === field) {
        currentOrder = currentOrder === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort = field;
        currentOrder = 'desc';
    }
    currentPage = 1;
    loadHistory();
}

async function deleteAnalysis(id) {
    if (!confirm('Are you sure you want to delete this analysis?')) return;

    try {
        const response = await fetch(`/api/analysis/${id}`, { method: 'DELETE' });
        const data = await response.json();
        if (data.success) {
            showNotification('Analysis deleted', 'success');
            loadHistory();
        } else {
            showNotification('Failed to delete', 'error');
        }
    } catch (err) {
        showNotification('Failed to delete', 'error');
    }
}
