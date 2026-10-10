from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..core.dependencies import get_current_user, require_role
from ..models.core import User
from ..ml.service import run_ml_insights

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

@router.get("/insights")
def get_insights(
    entity_id: int = Query(...), 
    period_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["manager", "admin"]))
):
    # Call the safe ML service
    run_ml_insights(db, entity_id, period_id)
    
    # Stub response
    return {
        "status": "success",
        "anomalies": [],
        "forecasts": []
    }
