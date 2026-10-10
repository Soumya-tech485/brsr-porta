// admin-dashboard.js - Admin Dashboard Page Logic

document.addEventListener('DOMContentLoaded', () => {
    // Check auth
    if (window.App.api) {
        window.App.api.requireRole(['admin']);
    }

    const state = {
        periodId: 1, // Default period
        data: null
    };

    // Load initial data
    loadDashboardData();

    async function loadDashboardData() {
        try {
            // Try fetching from real API
            const data = await window.App.api.fetch(`/admin/dashboard?period_id=${state.periodId}`);
            
            renderDashboard(data);
            
            await renderHeatmap();
            await renderFlags();

            if (window.App.ui) {
                window.App.ui.showToast('Dashboard data loaded successfully', 'success');
            }

        } catch (error) {
            console.error("Failed to load dashboard:", error);
            if (window.App.ui) {
                window.App.ui.showError('dashboard-content', 'Failed to load dashboard data. Please try again.');
            }
        }
    }

    function renderDashboard(data) {
        // 1. Readiness Strip
        document.getElementById('readiness-score').textContent = data.readiness + '%';
        document.getElementById('sites-count').textContent = `${data.sites_reporting} / ${data.total_sites} sites`;
        
        // Setup Readiness Ring SVG
        const ring = document.getElementById('readiness-ring-circle');
        if (ring) {
            const circumference = 2 * Math.PI * 36; // r=36
            const offset = circumference - (data.readiness / 100) * circumference;
            ring.style.strokeDasharray = `${circumference} ${circumference}`;
            ring.style.strokeDashoffset = offset;
            
            if (data.readiness >= 80) ring.style.stroke = 'var(--color-success)';
            else if (data.readiness >= 50) ring.style.stroke = 'var(--color-warning)';
            else ring.style.stroke = 'var(--color-danger)';
        }

        // 2. Populate KPI Cards
        document.getElementById('val-ghg').textContent = (data.scope1_tco2e + data.scope2_tco2e).toLocaleString();
        document.getElementById('val-ghg-int').textContent = data.intensity_scope1_cr + ' / ₹Cr';
        
        document.getElementById('val-energy').textContent = data.total_energy_gj.toLocaleString();
        document.getElementById('val-energy-ren').textContent = data.renewable_pct + '% Renewable';
        
        document.getElementById('val-water').textContent = data.water_withdrawal_kl.toLocaleString();
        document.getElementById('val-water-con').textContent = data.water_consumption_kl.toLocaleString() + ' consumed';
        
        document.getElementById('val-waste').textContent = data.waste_generated_mt.toLocaleString();
        document.getElementById('val-waste-rec').textContent = data.waste_recovered_pct + '% recovered';
        
        document.getElementById('val-safety').textContent = data.ltifr;
        const fatEl = document.getElementById('val-safety-fat');
        fatEl.textContent = (data.fatalities_employees + data.fatalities_workers) + ' Fatalities';
        if (data.fatalities_employees + data.fatalities_workers > 0) fatEl.style.color = 'var(--color-danger)';
        
        document.getElementById('val-gender').textContent = data.women_wage_pct + '%';
        document.getElementById('val-gender-posh').textContent = data.posh_complaints + ' POSH cases';
        
        document.getElementById('val-inclusive').textContent = data.msme_pct + '%';
        document.getElementById('val-inclusive-local').textContent = data.local_jobs_pct + '% Local jobs';
        
        document.getElementById('val-fairness').textContent = data.breaches;
        document.getElementById('val-fairness-days').textContent = data.payable_days + ' days payable';
        
        document.getElementById('val-openness').textContent = data.related_party_pct + '%';
        document.getElementById('val-openness-conc').textContent = data.concentration_index + ' index';

        // Initialize Sparklines
        initSparklines();
        
        // Initialize Main Charts
        initMainCharts();
    }
    
    function initSparklines() {
        if (!window.App.charts) return;
        
        const sparkIds = [
            { id: 'spark-ghg', color: '#10b981' },
            { id: 'spark-energy', color: '#d97706' },
            { id: 'spark-water', color: '#0d9488' },
            { id: 'spark-waste', color: '#7c3aed' },
            { id: 'spark-safety', color: '#e11d48' },
            { id: 'spark-gender', color: '#2563eb' },
            { id: 'spark-inclusive', color: '#2563eb' },
            { id: 'spark-fairness', color: '#475569' },
            { id: 'spark-openness', color: '#475569' }
        ];
        
        sparkIds.forEach(s => {
            const el = document.getElementById(s.id);
            if (el) {
                // Random walk data for demo
                const data = Array.from({length: 6}, () => Math.floor(Math.random() * 50) + 50);
                window.App.charts.createSparkline(el.getContext('2d'), data, s.color);
            }
        });
    }

    function initMainCharts() {
        if (!window.App.charts) return;
        
        // GHG Trend Chart
        const ghgCtx = document.getElementById('chart-ghg');
        if (ghgCtx) {
            const labels = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'];
            const current = [1200, 1150, 1100, 1120, 1080, 1050, 1000, 950, null, null, null, null];
            const prev = [1300, 1280, 1250, 1220, 1200, 1180, 1150, 1100, 1050, 1020, 980, 950];
            window.App.charts.createAreaChart(ghgCtx.getContext('2d'), labels, current, prev);
        }
        
        // Resource Bar Chart (Energy/Water/Waste placeholder)
        const resCtx = document.getElementById('chart-resource');
        if (resCtx) {
            const labels = ['Sub A', 'Sub B', 'Sub C'];
            const datasets = [
                { label: 'Renewable', data: [400, 300, 500], backgroundColor: '#10b981' },
                { label: 'Non-Renewable', data: [1200, 1500, 800], backgroundColor: '#d97706' }
            ];
            window.App.charts.createBarChart(resCtx.getContext('2d'), labels, datasets);
        }
    }
    
    async function renderHeatmap() {
        const tbody = document.getElementById('heatmap-body');
        if (!tbody) return;
        
        let heatmapData;
        try {
            heatmapData = await window.App.api.fetch(`/admin/completion?period_id=${state.periodId}`);
        } catch (e) {
            // Mock fallback
            heatmapData = {
                months: ["2023-04", "2023-05", "2023-06", "2023-07", "2023-08", "2023-09", "2023-10", "2023-11", "2023-12", "2024-01", "2024-02", "2024-03"],
                sites: [
                    { id: 1, name: "Site A-1 (Highway)", months: {"2023-04": "verified", "2023-05": "verified", "2023-06": "submitted", "2023-07": "draft"} },
                    { id: 2, name: "Site B-1 (Hydro)", months: {"2023-04": "verified", "2023-05": "submitted", "2023-06": "draft"} }
                ]
            };
        }
        
        const statuses = { 'none': 'hm-none', 'draft': 'hm-draft', 'submitted': 'hm-sub', 'returned': 'hm-ret', 'verified': 'hm-ver', 'locked': 'hm-lock' };
        
        let html = '';
        heatmapData.sites.forEach(site => {
            html += `<tr><td>${site.name}</td>`;
            heatmapData.months.forEach(month => {
                const s = site.months[month] || 'none';
                const sClass = statuses[s] || 'hm-none';
                html += `<td><div class="heatmap-cell ${sClass}" title="${site.name} - ${month}: ${s}"></div></td>`;
            });
            html += `</tr>`;
        });
        
        tbody.innerHTML = html;
    }
    
    async function renderFlags() {
        const flagList = document.getElementById('flag-list');
        if (!flagList) return;
        
        let flags;
        try {
            flags = await window.App.api.fetch(`/admin/flags?period_id=${state.periodId}`);
        } catch (e) {
            // Mock fallback
            flags = [
                { id: 1, type: 'critical', msg: 'Fatality reported at Site B-1', src: 'Rule', created_at: '2 mins ago' },
                { id: 2, type: 'warning', msg: 'Diesel consumption +310% vs site median', src: 'ML', created_at: '1 hour ago' },
                { id: 3, type: 'info', msg: 'Water withdrawal and discharge mismatch > 10%', src: 'Rule', created_at: '2 hours ago' }
            ];
        }
        
        let html = '';
        flags.forEach(f => {
            html += `
                <div class="flag-item ${f.type}">
                    <div style="flex:1;">
                        <div style="display:flex; justify-content:space-between;">
                            <span class="badge badge-${f.type === 'critical' ? 'danger' : f.type === 'warning' ? 'warning' : 'info'}">${f.src}</span>
                            <span style="font-size: 12px; color: #64748b;">${f.created_at}</span>
                        </div>
                        <p style="margin-top:8px; font-size:14px;">${f.msg}</p>
                    </div>
                </div>
            `;
        });
        
        if (flags.length === 0) {
            html = '<div style="padding: 20px; text-align: center; color: var(--color-text-muted);">No active flags.</div>';
        }
        
        flagList.innerHTML = html;
    }
});

// Expose global actions
window.lockPeriod = function() {
    if (confirm('Are you sure you want to lock this period? No further edits will be allowed.')) {
        if (window.App.ui) window.App.ui.showToast('Period Locked', 'success');
    }
};

window.reopenPeriod = function() {
    const reason = prompt('Please enter a reason for reopening this period:');
    if (reason) {
        if (window.App.ui) window.App.ui.showToast('Period Reopened', 'success');
    }
};

window.exportReport = function(format) {
    if (window.App.ui) window.App.ui.showToast(`Exporting ${format.toUpperCase()}...`, 'info');
    // Actual API call: window.App.api.fetch(`/reports/1/1?format=${format}`);
};
