# ESGraph API Contract

This document defines the REST API contract for ESGraph. Base URL: `/api/v1`.
All requests and responses use JSON.

## Standard Error Response
```json
{
  "detail": "Error message description",
  "code": "ERROR_CODE"
}
```

## 1. Authentication
### `POST /auth/login`
- **Role:** public
- **Request:** `{"email": "user@example.com", "password": "..."}`
- **Response:** `{"access_token": "...", "token_type": "bearer", "role": "engineer", "sites": [1, 2]}`

### `GET /auth/me`
- **Role:** any (authenticated)
- **Response:** `{"id": 1, "name": "...", "email": "...", "role": "engineer"}`

## 2. Forms & Data Entry (Engineer/Manager)
### `GET /forms/site`
- **Role:** engineer, manager
- **Query Params:** `?site_id=1&period_id=1&month_date=2024-04-01`
- **Response:** List of indicator definitions with sub_keys and units.

### `GET /entries`
- **Role:** engineer, manager
- **Query Params:** `?site_id=1&period_id=1&month_date=2024-04-01`
- **Response:** Array of existing entries.

### `PUT /entries/bulk`
- **Role:** engineer
- **Request:** `[{"indicator_id": 1, "sub_key": "diesel", "value_num": 500}]`
- **Response:** `{"status": "ok", "saved_count": 1}`

### `POST /entries/{id}/evidence`
- **Role:** engineer
- **Request:** `multipart/form-data` (file)
- **Response:** `{"id": 1, "file_path": "..."}`

### `POST /submissions/submit`
- **Role:** engineer
- **Request:** `{"site_id": 1, "period_id": 1, "month_date": "2024-04-01"}`
- **Response:** `{"status": "submitted"}`

## 3. Review (Manager)
### `GET /review/queue`
- **Role:** manager
- **Response:** Array of submitted sets for assigned sites.

### `POST /review/verify`
- **Role:** manager
- **Request:** `{"site_id": 1, "period_id": 1, "month_date": "2024-04-01"}`
- **Response:** `{"status": "verified"}`

### `POST /review/return`
- **Role:** manager
- **Request:** `{"site_id": 1, "period_id": 1, "month_date": "2024-04-01", "comment": "Fix unit"}`
- **Response:** `{"status": "returned"}`

## 4. Admin & Corporate
### `GET/PUT /corporate/entries`
- **Role:** admin
- **Request/Response:** Array of corporate entries.

### `GET/PUT /financials`
- **Role:** admin
- **Request/Response:** `{"revenue_inr": 1000, "ppp_rate": 83.2, "source_note": "..."}`

### `GET /admin/dashboard`
- **Role:** admin
- **Response:** Aggregated KPIs, YoY data, readiness score.

### `GET /reports/{entity_id}/{period_id}`
- **Role:** admin
- **Query Params:** `?format=xlsx` or `?format=pdf`
- **Response:** Binary file download.

*Draft API Contract - will be expanded with full schema models in Phase 2.*
