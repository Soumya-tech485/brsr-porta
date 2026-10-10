# ESGraph - BRSR Reporting Portal

## Setup locally

1. **Database:**
   Start MySQL via Docker:
   ```bash
   docker-compose up -d
   ```

2. **Backend:**
   Create a virtual environment and install dependencies:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
   
   Copy `.env.example` to `.env` in the root:
   ```bash
   cp .env.example .env
   ```
   
   Run the FastAPI server:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

3. **Frontend:**
   Open `frontend/login.html` in your browser. (Alternatively, run a static server from the project root `python -m http.server 3000`).
