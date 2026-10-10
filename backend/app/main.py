from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import auth, forms, entries, review, admin, ml, reports

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0", root_path=settings.API_V1_STR)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8080", "http://127.0.0.1:8080", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(forms.router)
app.include_router(entries.router)
app.include_router(review.router)
app.include_router(admin.router)
app.include_router(ml.router)
app.include_router(reports.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "ESGraph API is healthy"}
