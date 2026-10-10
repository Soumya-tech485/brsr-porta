from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import date
from ..database import get_db
from ..core.dependencies import get_current_user, require_role, require_site_access
from ..models.entry import SiteEntry
from ..models.review import ReviewLog
from ..models.core import UserSite, User
from ..schemas.review import ReviewRequest, ReturnRequest

router = APIRouter(prefix="/review", tags=["Review"])

@router.get("/queue")
def get_review_queue(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["manager", "admin"]))
):
    # Fetch all submitted entries for sites assigned to the user
    user_sites = db.query(UserSite).filter(UserSite.user_id == current_user.id).all()
    site_ids = [us.entity_id for us in user_sites]
    
    if not site_ids and current_user.role != 'admin':
        return []
        
    query = db.query(SiteEntry).filter(SiteEntry.status == 'submitted')
    if current_user.role != 'admin':
        query = query.filter(SiteEntry.entity_id.in_(site_ids))
        
    entries = query.all()
    
    # Group by site/period/month for the queue view
    queue = []
    # simple grouping logic (in real life might group by SQL)
    grouped = {}
    for entry in entries:
        key = f"{entry.entity_id}_{entry.period_id}_{entry.month_date}"
        if key not in grouped:
            grouped[key] = {
                "site_id": entry.entity_id,
                "period_id": entry.period_id,
                "month_date": entry.month_date,
                "entry_count": 0
            }
        grouped[key]["entry_count"] += 1
        
    return list(grouped.values())

@router.post("/verify")
def verify_entries(
    request: ReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["manager", "admin"]))
):
    require_site_access(request.site_id)(current_user=current_user, db=db)
    
    entries = db.query(SiteEntry).filter(
        SiteEntry.entity_id == request.site_id,
        SiteEntry.period_id == request.period_id,
        SiteEntry.month_date == request.month_date,
        SiteEntry.status == 'submitted'
    ).all()
    
    if not entries:
        raise HTTPException(status_code=400, detail="No submitted entries found to verify")
        
    # Check for self-verification
    if any(e.entered_by == current_user.id for e in entries):
        raise HTTPException(status_code=403, detail="Cannot verify entries you submitted yourself")
        
    for entry in entries:
        entry.status = 'verified'
        entry.verified_by = current_user.id
        # Log action
        log = ReviewLog(
            entry_id=entry.id,
            actor_id=current_user.id,
            action='verify',
            comment=''
        )
        db.add(log)
        
    db.commit()
    return {"status": "verified", "count": len(entries)}

@router.post("/return")
def return_entries(
    request: ReturnRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["manager", "admin"]))
):
    require_site_access(request.site_id)(current_user=current_user, db=db)
    
    entries = db.query(SiteEntry).filter(
        SiteEntry.entity_id == request.site_id,
        SiteEntry.period_id == request.period_id,
        SiteEntry.month_date == request.month_date,
        SiteEntry.status == 'submitted'
    ).all()
    
    if not entries:
        raise HTTPException(status_code=400, detail="No submitted entries found to return")
        
    if not request.comment or len(request.comment.strip()) == 0:
        raise HTTPException(status_code=400, detail="A comment is required when returning data")
        
    for entry in entries:
        entry.status = 'returned'
        # Log action
        log = ReviewLog(
            entry_id=entry.id,
            actor_id=current_user.id,
            action='return',
            comment=request.comment
        )
        db.add(log)
        
    db.commit()
    return {"status": "returned", "count": len(entries)}
