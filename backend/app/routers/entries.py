from fastapi import APIRouter, Depends, Query, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from typing import List
from datetime import date
import hashlib
import os
import shutil
from ..database import get_db
from ..core.dependencies import get_current_user, require_role, require_site_access
from ..models.entry import SiteEntry
from ..schemas.entry import BulkEntryRequest, EntryResponse, SubmitRequest
from ..models.core import User

router = APIRouter(prefix="/entries", tags=["Entries"])

@router.get("", response_model=List[EntryResponse])
def get_entries(
    site_id: int = Query(...),
    period_id: int = Query(...),
    month_date: date = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["engineer", "manager", "admin"]))
):
    require_site_access(site_id)(current_user=current_user, db=db)
    
    entries = db.query(SiteEntry).filter(
        SiteEntry.entity_id == site_id,
        SiteEntry.period_id == period_id,
        SiteEntry.month_date == month_date
    ).all()
    return entries

@router.put("/bulk")
def bulk_save_entries(
    request: BulkEntryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["engineer"]))
):
    require_site_access(request.site_id)(current_user=current_user, db=db)
    
    # Upsert logic (insert or update on duplicate key)
    values_to_insert = []
    for entry in request.entries:
        values_to_insert.append({
            'entity_id': request.site_id,
            'period_id': request.period_id,
            'month_date': request.month_date,
            'indicator_id': entry.indicator_id,
            'sub_key': entry.sub_key or '',
            'value_num': entry.value_num,
            'value_text': entry.value_text,
            'status': 'draft',
            'entered_by': current_user.id
        })
    
    if not values_to_insert:
        return {"status": "ok", "saved_count": 0}

    stmt = insert(SiteEntry).values(values_to_insert)
    
    # On duplicate key, update the values
    on_duplicate_key_stmt = stmt.on_duplicate_key_update(
        value_num=stmt.inserted.value_num,
        value_text=stmt.inserted.value_text,
        status='draft',  # Reset to draft on edit
        entered_by=stmt.inserted.entered_by
    )
    
    db.execute(on_duplicate_key_stmt)
    db.commit()
    
    return {"status": "ok", "saved_count": len(request.entries)}

@router.post("/submit")
def submit_entries(
    request: SubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["engineer"]))
):
    require_site_access(request.site_id)(current_user=current_user, db=db)
    
    # Find all entries for this site/period/month that are in draft or returned
    entries = db.query(SiteEntry).filter(
        SiteEntry.entity_id == request.site_id,
        SiteEntry.period_id == request.period_id,
        SiteEntry.month_date == request.month_date,
        SiteEntry.status.in_(['draft', 'returned'])
    ).all()
    
    if not entries:
        raise HTTPException(status_code=400, detail="No draft entries found to submit")
        
    # Set status to submitted
    for entry in entries:
        entry.status = 'submitted'
        
    db.commit()
    return {"status": "submitted", "count": len(entries)}

@router.post("/{id}/evidence")
def upload_evidence(
    id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["engineer"]))
):
    entry = db.query(SiteEntry).filter(SiteEntry.id == id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
        
    require_site_access(entry.entity_id)(current_user=current_user, db=db)
    
    # Validate extension
    allowed_extensions = {".pdf", ".png", ".jpg", ".jpeg", ".xlsx", ".csv"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type")
        
    # Read file to hash and check size (approx memory limit)
    contents = file.file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")
        
    sha256_hash = hashlib.sha256(contents).hexdigest()
    
    # Save file
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{sha256_hash}{ext}")
    
    with open(file_path, "wb") as f:
        f.write(contents)
        
    # TODO: Save evidence metadata to DB (evidence table)
    
    return {"id": entry.id, "file_path": file_path, "hash": sha256_hash}
