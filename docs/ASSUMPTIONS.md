# Assumptions

This document records the assumptions relied upon by the development team while building the ESGraph BRSR portal, as derived from the problem statement, SEBI documents, and other reference materials.

## Business & Process Assumptions
1.  **Current Process**: MEIL's current ESG data collection process is largely manual, relying on spreadsheets and email.
2.  **Data Entry Frequency**: Site-level ESG data is entered into the system on a monthly basis.
3.  **Reporting Boundary & Listing Status**: MEIL's exact reporting boundary (standalone vs. consolidated) and listing status are not fixed for the purposes of this portal; therefore, they are built as Admin-configurable settings within each reporting period.
4.  **Subsidiary List**: The exact, real-world subsidiary list of MEIL is unknown. We will use generic, synthetic entities (e.g., "Subsidiary A", "Subsidiary B") for the demo.
5.  **Site-Level Data Availability**: We assume that specific data points like procurement from MSMEs/local sources are available at the site level, even though this might sometimes be managed centrally in some organizations.
6.  **Real MEIL Data**: All data used in this project will be synthetic. No real MEIL ESG data or proprietary information will be used or fabricated.

## Technical & System Assumptions
1.  **Deployment**: The system is designed to run locally via `docker-compose` for the database and standard Python/Node environments for backend/frontend during the hackathon/demo phase.
2.  **AI/ML Role**: The AI/ML models (anomaly detection, forecasting, extraction) act in an advisory capacity only. They will not automatically approve, overwrite, or reject data without a human-in-the-loop (rule-based fallback must always exist).
3.  **Authentication**: Simple JWT-based authentication with bcrypt hashing is sufficient for the scope of this project; no complex SSO/OAuth integrations are required.
4.  **Browser Support**: The frontend is assumed to be accessed via modern web browsers and must be responsive (mobile to desktop).

*(This list will be updated as new assumptions are identified during development.)*
