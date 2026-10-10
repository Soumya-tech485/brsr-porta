# Frontend Handoff Document

This document serves as the guide for the frontend developer completing the UIs for the ESGraph portal.

## Backend Status
The backend API is 100% complete and running at `http://localhost:8000`.
- **OpenAPI / Swagger UI**: You can view all available endpoints, required request bodies, and expected responses by navigating to `http://localhost:8000/docs` while the backend is running.

## Frontend Foundations
The basic HTML shells and the CSS variable framework have been established for you.
- Use `frontend/css/variables.css` for all colors, spacing, and typography. (No Tailwind!).
- Write everything in vanilla JS modules.

## API Communication
Never use `fetch()` directly. We have built a robust wrapper for you in `frontend/js/api.js`.
This wrapper automatically injects the JWT authentication token into every request, and handles `401 Unauthorized` redirects for you.

### Example Usage:
```javascript
// Ensure api.js is included in your HTML script tags
try {
    const data = await window.App.api.fetch('/entries');
    console.log(data);
} catch (error) {
    // The wrapper already handles 401 redirects, but you can catch other errors here
    console.error("Failed to fetch data:", error);
}
```

## Security & Guards
To prevent unauthorized users from accessing pages they shouldn't, include this block at the very top of your `<body>` tags for every new page you create:
```html
<script src="../js/api.js"></script>
<script>
    // Enforce role access immediately
    window.App.api.requireRole(['engineer']); // change role depending on the folder
</script>
```

Good luck!
