import os
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..core.dependencies import get_current_user, require_role
from ..models.core import User
from ..services.consolidation import consolidate_data
from ..services.report import generate_excel_report, generate_pdf_report

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/download")
def download_report(
    period_id: int = Query(...),
    format: str = Query(..., description="pdf or excel"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["manager", "admin"]))
):
    if format not in ["pdf", "excel"]:
        raise HTTPException(status_code=400, detail="Invalid format. Choose 'pdf' or 'excel'")
        
    # In a real scenario we'd find the top level Group entity ID.
    # For demo, assume root entity ID = 1
    root_entity_id = 1 
    
    # Run the math
    data = consolidate_data(db, entity_id=root_entity_id, period_id=period_id)
    
    # Generate file
    if format == "excel":
        filepath = generate_excel_report(data)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    else:
        filepath = generate_pdf_report(data)
        media_type = "application/pdf"
        
    return FileResponse(
        path=filepath,
        filename=os.path.basename(filepath),
        media_type=media_type
    )
