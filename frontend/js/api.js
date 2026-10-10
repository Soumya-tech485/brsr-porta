// api.js - Centralized API Wrapper for ESGraph

const API_BASE_URL = 'http://127.0.0.1:8000';

window.App = window.App || {};

window.App.api = {
    async fetch(endpoint, options = {}) {
        const token = sessionStorage.getItem('token');
        
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                ...options,
                headers
            });
            
            if (response.status === 401) {
                // Unauthorized - token expired or missing
                sessionStorage.removeItem('token');
                sessionStorage.removeItem('role');
                alert('Session expired. Please log in again.');
                window.location.href = '/frontend/login.html';
                throw new Error('Unauthorized');
            }
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP Error: ${response.status}`);
            }
            
            // If response is a file (e.g. PDF/Excel), return the blob instead of JSON
            const contentType = response.headers.get('content-type');
            if (contentType && (contentType.includes('application/pdf') || contentType.includes('spreadsheetml'))) {
                return await response.blob();
            }
            
            return await response.json();
            
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    // Auth Helpers
    logout() {
        sessionStorage.clear();
        window.location.href = '/frontend/login.html';
    },
    
    // Role Guard Check
    requireRole(allowedRoles) {
        const currentRole = sessionStorage.getItem('role');
        if (!currentRole || !allowedRoles.includes(currentRole)) {
            alert('Access Denied: You do not have permission to view this page.');
            window.location.href = '/frontend/login.html';
        }
    }
};
