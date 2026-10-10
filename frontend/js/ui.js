// ui.js - Shared UI components

window.App = window.App || {};

window.App.ui = {
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.setAttribute('aria-live', 'polite');
        
        Object.assign(toast.style, {
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            padding: '12px 20px',
            borderRadius: '8px',
            background: type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : '#3b82f6',
            color: 'white',
            fontWeight: '500',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
            zIndex: '9999',
            opacity: '0',
            transform: 'translateY(20px)',
            transition: 'all 0.3s ease'
        });
        
        document.body.appendChild(toast);
        
        // Animate in
        requestAnimationFrame(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateY(0)';
        });
        
        // Remove after 3s
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(20px)';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },
    
    showError(containerId, message) {
        const container = document.getElementById(containerId);
        if (!container) return;
        container.innerHTML = `
            <div class="empty-state error-state" style="text-align: center; padding: 20px; color: #ef4444;">
                <div style="font-size: 2rem; margin-bottom: 10px;">⚠️</div>
                <p>${message}</p>
                <button class="btn btn-outline" style="margin-top: 10px;" onclick="location.reload()">Retry</button>
            </div>
        `;
    },
    
    showEmpty(containerId, message) {
        const container = document.getElementById(containerId);
        if (!container) return;
        container.innerHTML = `
            <div class="empty-state" style="text-align: center; padding: 20px; color: #64748b;">
                <div style="font-size: 2rem; margin-bottom: 10px;">📭</div>
                <p>${message}</p>
            </div>
        `;
    }
};
