// manager-review.js - Site Manager Review Logic

document.addEventListener('DOMContentLoaded', () => {
    // Check auth
    if (window.App.api) {
        window.App.api.requireRole(['manager', 'admin']);
    }

    const state = {
        queue: [],
        selectedItem: null,
        indicators: []
    };

    // Load initial data
    loadQueue();

    async function loadQueue() {
        try {
            // Fetch real queue from API
            const queueItems = await window.App.api.fetch('/review/queue');
            state.queue = queueItems.map((q, idx) => ({
                id: q.site_id, // we map site_id as the queue item id
                site: q.site_name,
                month: q.month_date,
                submitter: q.submitted_by_name || 'System',
                date: 'Recently',
                status: 'pending'
            }));
            
            renderQueue();
            
            // Auto-select first item if queue not empty
            if (state.queue.length > 0) {
                selectQueueItem(state.queue[0].id);
            } else {
                showEmptyWorkspace();
            }
            
        } catch (error) {
            console.error('Failed to load queue:', error);
            if (window.App.ui) window.App.ui.showError('queue-list', 'Failed to load review queue.');
        }
    }

    function renderQueue() {
        const queueList = document.getElementById('queue-list');
        if (!queueList) return;

        let html = '';
        state.queue.forEach(q => {
            html += `
                <div class="queue-item ${state.selectedItem && state.selectedItem.id === q.id ? 'active' : ''}" onclick="window.selectQueueItem(${q.id})">
                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                        <span style="font-weight:600; color:var(--color-text-dark);">${q.site}</span>
                        <span class="badge badge-warning">Pending</span>
                    </div>
                    <div class="text-sm text-muted">${q.month}</div>
                    <div class="text-xs text-muted" style="margin-top:8px;">Submitted by ${q.submitter} • ${q.date}</div>
                </div>
            `;
        });
        queueList.innerHTML = html;
    }

    window.selectQueueItem = function(id) {
        state.selectedItem = state.queue.find(q => q.id === id);
        renderQueue(); // Update active class
        loadWorkspaceData(id);
    };

    function showEmptyWorkspace() {
        const ws = document.getElementById('review-workspace');
        if (ws && window.App.ui) window.App.ui.showEmpty('review-workspace', 'Select an item from the queue to review.');
    }

    async function loadWorkspaceData(site_id) {
        try {
            const month = state.selectedItem.month;
            // Get entries for the site and month
            const entries = await window.App.api.fetch(`/entries?site_id=${site_id}&period_id=1&month_date=${month}`);
            
            state.indicators = entries.map(e => ({
                code: `IND-${e.indicator_id}`,
                name: `Indicator ${e.indicator_id}`,
                value: e.value_num || 0,
                unit: 'units', // Need to join with indicator metadata ideally
                flag: null,
                prev: 0,
                file: 'evidence.pdf'
            }));

            renderWorkspace();
        } catch (err) {
            console.error(err);
            if (window.App.ui) window.App.ui.showError('review-workspace', 'Failed to load data for this submission.');
        }
    }

    function renderWorkspace() {
        const ws = document.getElementById('review-workspace');
        if (!ws) return;

        let html = `
            <div class="card" style="margin-bottom: 0;">
                <div class="flex items-center justify-between">
                    <div>
                        <h2 class="text-lg">${state.selectedItem.site} - ${state.selectedItem.month}</h2>
                        <p class="text-sm text-muted">Submitted by ${state.selectedItem.submitter} on ${state.selectedItem.date}</p>
                    </div>
                    <div>
                        <button class="btn btn-outline" onclick="window.returnAll()">Return Submission</button>
                        <button class="btn" style="background: var(--color-primary);" onclick="window.verifyAll()">Verify & Approve</button>
                    </div>
                </div>
            </div>

            <div class="split-view">
                <!-- Left: Data Panel -->
                <div class="data-panel">
                    <div class="panel-header">Submitted Data (4 Indicators)</div>
                    <div class="panel-content">
                        <table class="verify-table">
                            <thead>
                                <tr>
                                    <th>Indicator</th>
                                    <th>Value</th>
                                    <th>Trend / Flag</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
        `;

        state.indicators.forEach((ind, idx) => {
            html += `
                <tr onclick="window.selectRow(${idx})" id="row-${idx}">
                    <td>
                        <div style="font-weight:500;">${ind.name}</div>
                        <div class="text-xs text-muted">${ind.code}</div>
                    </td>
                    <td>
                        <div style="font-weight:600;">${ind.value.toLocaleString()} <span style="font-weight:400; color:var(--color-text-muted);">${ind.unit}</span></div>
                    </td>
                    <td>
                        ${ind.flag ? `<span style="color:var(--color-warning); font-size:12px; font-weight:500;">${ind.flag.msg}</span>` : `<span style="color:var(--color-text-muted); font-size:12px;">Prev: ${ind.prev.toLocaleString()}</span>`}
                    </td>
                    <td>
                        <div class="action-buttons">
                            <button class="btn-icon approve" title="Looks Good">✓</button>
                            <button class="btn-icon reject" title="Return">✕</button>
                        </div>
                    </td>
                </tr>
            `;
        });

        html += `
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Right: Evidence Panel -->
                <div class="evidence-panel">
                    <div class="panel-header">Evidence & Context</div>
                    <div class="evidence-viewer" id="evidence-viewer">
                        <div class="text-center text-muted" style="margin-top:40px;">Select a row to view evidence.</div>
                    </div>
                </div>
            </div>
        `;

        ws.innerHTML = html;
        
        // Auto-select first row
        if (state.indicators.length > 0) selectRow(0);
    }

    window.selectRow = function(idx) {
        document.querySelectorAll('.verify-table tr').forEach((row, i) => {
            if (row.id) row.classList.toggle('selected', i - 1 === idx); // i-1 because of thead tr
        });

        const ind = state.indicators[idx];
        const viewer = document.getElementById('evidence-viewer');
        
        viewer.innerHTML = `
            <div style="margin-bottom:var(--spacing-4);">
                <h4 style="margin-bottom:4px;">${ind.name}</h4>
                <div class="flex gap-2 text-sm text-muted">
                    <span>Value: <strong>${ind.value.toLocaleString()} ${ind.unit}</strong></span> |
                    <span>Prev: ${ind.prev.toLocaleString()} ${ind.unit}</span>
                </div>
            </div>
            
            <div class="preview-box">
                <div style="text-align:center;">
                    <div style="font-size:3rem; margin-bottom:10px;">📄</div>
                    <div>${ind.file}</div>
                    <button class="btn btn-outline" style="margin-top:10px; padding:4px 8px; font-size:12px;">Download / View</button>
                </div>
            </div>
            
            <div class="return-form">
                <label class="input-label" style="font-size:12px;">Mandatory comment if returning:</label>
                <textarea class="form-control" placeholder="Explain why this value is being returned... e.g., 'Unit error, please check'"></textarea>
                <div style="display:flex; justify-content:flex-end; margin-top:8px;">
                    <button class="btn btn-outline" style="color:var(--color-danger); border-color:var(--color-danger);" onclick="window.returnField()">Return Field</button>
                </div>
            </div>
        `;
    };

    window.verifyAll = async function() {
        if (confirm('Verify and approve all data for this site month?')) {
            try {
                await window.App.api.fetch('/review/verify', {
                    method: 'POST',
                    body: JSON.stringify({
                        site_id: state.selectedItem.id,
                        period_id: 1, // mock
                        month_date: state.selectedItem.month
                    })
                });
                if (window.App.ui) window.App.ui.showToast('Data verified successfully.', 'success');
                state.queue = state.queue.filter(q => q.id !== state.selectedItem.id);
                state.selectedItem = null;
                renderQueue();
                if (state.queue.length > 0) selectQueueItem(state.queue[0].id);
                else showEmptyWorkspace();
            } catch(e) {
                if (window.App.ui) window.App.ui.showToast('Error verifying: ' + e.message, 'error');
            }
        }
    };

    window.returnAll = async function() {
        const reason = prompt('Please enter a reason for returning this entire submission:');
        if (reason) {
            try {
                await window.App.api.fetch('/review/return', {
                    method: 'POST',
                    body: JSON.stringify({
                        site_id: state.selectedItem.id,
                        period_id: 1, // mock
                        month_date: state.selectedItem.month,
                        comment: reason
                    })
                });
                if (window.App.ui) window.App.ui.showToast('Submission returned to Engineer.', 'success');
                state.queue = state.queue.filter(q => q.id !== state.selectedItem.id);
                state.selectedItem = null;
                renderQueue();
                if (state.queue.length > 0) selectQueueItem(state.queue[0].id);
                else showEmptyWorkspace();
            } catch(e) {
                if (window.App.ui) window.App.ui.showToast('Error returning: ' + e.message, 'error');
            }
        }
    };

    window.returnField = function() {
        if (window.App.ui) window.App.ui.showToast('Field marked as returned.', 'info');
    };
});
