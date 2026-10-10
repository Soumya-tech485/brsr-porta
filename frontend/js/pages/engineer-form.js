// engineer-form.js - Site Engineer Data Entry Logic

document.addEventListener('DOMContentLoaded', () => {
    // Check auth
    if (window.App.api) {
        window.App.api.requireRole(['engineer']);
    }

    const state = {
        siteId: 1,
        periodId: 1,
        month: '2024-04',
        currentTab: 'energy',
        draftData: {},
        isDirty: false
    };

    // Load initial data
    loadFormSchema();

    let allIndicators = [];
    
    async function loadFormSchema() {
        try {
            // Fetch real form schema from API
            allIndicators = await window.App.api.fetch(`/forms/site?site_id=${state.siteId}&period_id=${state.periodId}&month_date=${state.month}-01`);
            
            // Map the indicators to their tabs
            const schema = {
                energy: allIndicators.filter(i => i.code.startsWith('GHG') || i.code.startsWith('ENERGY')),
                water: allIndicators.filter(i => i.code.startsWith('WATER')),
                waste: allIndicators.filter(i => i.code.startsWith('WASTE')),
                safety: allIndicators.filter(i => i.principle === '3'),
                social: allIndicators.filter(i => i.principle === '5' || i.principle === '8')
            };

            // Format them for the UI
            Object.keys(schema).forEach(tab => {
                schema[tab] = schema[tab].map(ind => ({
                    id: ind.id,
                    code: ind.code,
                    label: ind.code,
                    unit: ind.unit,
                    hint: ind.evidence_hint,
                    prev: 0, // Mock prev for now
                    type: 'number',
                    tooltip: getTooltip(ind.code)
                }));
            });
            
            // Fetch existing draft data
            const existingEntries = await window.App.api.fetch(`/entries?site_id=${state.siteId}&period_id=${state.periodId}&month_date=${state.month}-01`);
            existingEntries.forEach(e => {
                state.draftData[e.indicator_id] = e.value_num;
            });

            window.formSchemaCache = schema;

            renderTabs();
            renderFormFields(schema[state.currentTab] || []);
            
            // Setup autosave
            setInterval(autoSave, 30000); // every 30s
            
            if (window.App.ui) window.App.ui.showToast('Form loaded successfully', 'success');
        } catch (error) {
            console.error('Failed to load forms:', error);
            if (window.App.ui) window.App.ui.showError('form-content', 'Failed to load form definitions.');
        }
    }
    
    function getTooltip(code) {
        if(code === 'WORKFORCE') return 'Worker: manual/skilled work (excludes supervisors). Other than Permanent: fixed term/contractors.';
        if(code === 'PROCUREMENT_MSME') return 'Small Producers: owner is worker (e.g. self-help groups, home-based).';
        return '';
    }

    function renderTabs() {
        const tabs = [
            { id: 'energy', icon: '⚡', label: 'Energy Footprint' },
            { id: 'water', icon: '💧', label: 'Water Footprint' },
            { id: 'waste', icon: '♻️', label: 'Waste & Circularity' },
            { id: 'safety', icon: '👷', label: 'Safety & Well-being' },
            { id: 'social', icon: '👥', label: 'Social & Diversity' }
        ];

        const navList = document.getElementById('form-nav');
        if (!navList) return;

        let html = '';
        tabs.forEach(t => {
            html += `<li class="form-nav-item ${t.id === state.currentTab ? 'active' : ''}" data-tab="${t.id}">
                        <span>${t.icon} ${t.label}</span>
                        <span class="badge badge-neutral">0/2</span>
                     </li>`;
        });
        navList.innerHTML = html;

        // Add event listeners
        navList.querySelectorAll('.form-nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const tab = e.currentTarget.dataset.tab;
                switchTab(tab);
            });
        });
    }

    function switchTab(tabId) {
        state.currentTab = tabId;
        document.querySelectorAll('.form-nav-item').forEach(el => {
            el.classList.toggle('active', el.dataset.tab === tabId);
        });
        document.getElementById('current-tab-title').textContent = tabId.charAt(0).toUpperCase() + tabId.slice(1) + ' Footprint';
        
        renderFormFields(window.formSchemaCache[tabId] || []);
    }

    function renderFormFields(fields) {
        const container = document.getElementById('form-fields-container');
        if (!container) return;

        if (fields.length === 0) {
            container.innerHTML = `<div style="text-align:center; padding:40px; color:#64748b;">No indicators defined for this section.</div>`;
            return;
        }

        let html = '';
        fields.forEach(f => {
            const val = state.draftData[f.id] || '';
            const tooltipHtml = f.tooltip ? `<div class="input-tooltip" style="font-size:0.8rem; color:#3b82f6; margin-bottom:4px;">ℹ️ ${f.tooltip}</div>` : '';
            html += `
                <div class="input-group" id="group-${f.id}">
                    <label class="input-label">${f.label}</label>
                    ${tooltipHtml}
                    <div class="input-description">Evidence required: ${f.hint}</div>
                    
                    <div class="input-wrapper">
                        <input type="number" class="form-control" id="input-${f.id}" value="${val}" placeholder="0.00" oninput="window.handleInput('${f.id}')">
                        <span class="input-unit">${f.unit}</span>
                    </div>
                    <div class="input-error-msg" id="err-${f.id}"></div>
                    
                    <div class="ref-value">
                        <span style="color:#94a3b8;">🕒 Previous month:</span> ${f.prev.toLocaleString()} ${f.unit}
                    </div>

                    <div class="file-dropzone" onclick="window.triggerUpload('${f.id}')">
                        <span style="font-size:1.2rem; display:block; margin-bottom:4px;">📄</span>
                        Drag & drop evidence file here or click to browse
                    </div>
                    <div id="file-info-${f.id}" style="display:none;" class="file-info">
                        <span>📄 <span id="file-name-${f.id}"></span></span>
                        <button class="btn-icon" onclick="window.removeFile('${f.id}')" title="Remove" style="width:24px; height:24px;">×</button>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    }

    window.handleInput = function(id) {
        state.isDirty = true;
        const val = document.getElementById(`input-${id}`).value;
        state.draftData[id] = val;
        
        const group = document.getElementById(`group-${id}`);
        const errMsg = document.getElementById(`err-${id}`);
        
        // Simple inline validation mock
        if (val < 0) {
            group.classList.add('has-error');
            errMsg.textContent = 'Value cannot be negative';
        } else {
            group.classList.remove('has-error');
        }
        
        updateDraftStatus('Unsaved changes');
    };

    window.triggerUpload = function(id) {
        // Mock file selection
        setTimeout(() => {
            document.getElementById(`file-info-${id}`).style.display = 'flex';
            document.getElementById(`file-name-${id}`).textContent = `${id}_evidence_apr24.pdf`;
            if (window.App.ui) window.App.ui.showToast('Evidence attached', 'success');
        }, 500);
    };

    window.removeFile = function(id) {
        document.getElementById(`file-info-${id}`).style.display = 'none';
    };

    window.saveDraft = function() {
        if (!state.isDirty) return;
        autoSave();
    };

    window.submitForm = async function() {
        const keys = Object.keys(state.draftData);
        if (keys.length === 0) {
             if (window.App.ui) window.App.ui.showToast('Please enter some data before submitting.', 'error');
             return;
        }
        
        if (confirm('Are you sure you want to submit this month\'s data for review? You will not be able to edit it unless it is returned.')) {
            try {
                await autoSave(); // Ensure latest is saved
                await window.App.api.fetch('/submissions/submit', {
                    method: 'POST',
                    body: JSON.stringify({
                        site_id: state.siteId,
                        period_id: state.periodId,
                        month_date: `${state.month}-01`
                    })
                });
                if (window.App.ui) window.App.ui.showToast('Data submitted successfully.', 'success');
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } catch (err) {
                if (window.App.ui) window.App.ui.showToast('Failed to submit: ' + err.message, 'error');
            }
        }
    };

    async function autoSave() {
        if (!state.isDirty) return;
        
        updateDraftStatus('Saving...');
        
        try {
            const entries = Object.keys(state.draftData).map(k => ({
                indicator_id: parseInt(k),
                sub_key: null,
                value_num: parseFloat(state.draftData[k]) || 0
            }));
            
            await window.App.api.fetch('/entries/bulk', {
                method: 'PUT',
                body: JSON.stringify({
                    site_id: state.siteId,
                    period_id: state.periodId,
                    month_date: `${state.month}-01`,
                    entries: entries
                })
            });
            state.isDirty = false;
            updateDraftStatus('All changes saved to Draft');
        } catch (err) {
            updateDraftStatus('Save failed');
        }
    }
    
    function updateDraftStatus(text) {
        const el = document.getElementById('draft-status');
        if (el) el.textContent = text;
    }
});
