from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from ..database import get_db
from ..core.dependencies import get_current_user, require_role, require_site_access
from ..models.entry import Indicator
from ..schemas.entry import IndicatorResponse
from ..models.core import User

router = APIRouter(prefix="/forms", tags=["Forms"])

@router.get("/site", response_model=List[IndicatorResponse])
def get_site_forms(
    site_id: int = Query(...),
    period_id: int = Query(...),
    month_date: date = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["engineer", "manager", "admin"]))
):
    # Enforce site access
    require_site_access(site_id)(current_user=current_user, db=db)
    
    # Return all site-level indicators
    indicators = db.query(Indicator).filter(Indicator.level == 'site').order_by(Indicator.sort_order).all()
    return indicators
