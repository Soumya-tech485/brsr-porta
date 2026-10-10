from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..core.dependencies import get_current_user, require_role
from ..models.core import User
from ..models.entry import ReportingPeriod
from ..models.review import ReviewLog
from ..schemas.admin import ReadinessResponse, LockPeriodRequest, ReopenPeriodRequest
from ..services.readiness import calculate_readiness
from ..services.consolidation import consolidate_data
from ..services.calc_engine import calc_scope_1, calc_scope_2, calc_percentage, calc_ltifr, calc_energy_total, calc_intensity_per_rupee, calc_ppp_intensity

router = APIRouter(prefix="/admin", tags=["Admin Analytics"])

@router.get("/dashboard")
def get_dashboard(period_id: int = Query(...), db: Session = Depends(get_db), current_user: User = Depends(require_role(["admin"]))):
    # Real DB consolidation
    aggregated = consolidate_data(db, 1, period_id)  # Assuming entity 1 is group
    
    # Mock factors for now since we don't have the real factor table seeded fully
    factors = {"diesel": 2.68, "petrol": 2.31, "coal": 2.4, "natural_gas": 2.75}
    calorific = {"diesel": 38.6, "petrol": 34.2, "coal": 24.0, "natural_gas": 39.0}
    grid_factor = 0.82
    
    scope1 = calc_scope_1(aggregated.get('GHG_S1', {}), factors)
    scope2 = calc_scope_2(aggregated.get('GHG_S2', {}).get('grid_electricity', 0.0), grid_factor)
    water_with = sum(aggregated.get('WATER_WITHDRAWAL', {}).values())
    water_dis = sum(aggregated.get('WATER_DISCHARGE', {}).values())
    waste_gen = sum(aggregated.get('WASTE_GEN', {}).values())
    waste_rec = sum(aggregated.get('WASTE_REC', {}).values())
    
    energy_data = calc_energy_total(aggregated.get('ENERGY_CONS', {}), calorific)
    
    ltifr = calc_ltifr(aggregated.get('SAFETY_LTIFR', {}).get('lost_time_injuries', 0), aggregated.get('SAFETY_LTIFR', {}).get('hours_worked', 0))
    women_wage_pct = calc_percentage(aggregated.get('WAGES_GENDER', {}).get('gross_wages_female', 0), aggregated.get('WAGES_GENDER', {}).get('gross_wages_total', 0))
    msme_pct = calc_percentage(aggregated.get('PROCUREMENT_MSME', {}).get('from_msme', 0), aggregated.get('PROCUREMENT_MSME', {}).get('total', 0))
    local_jobs_pct = calc_percentage(aggregated.get('JOB_CREATION', {}).get('wages_rural', 0) + aggregated.get('JOB_CREATION', {}).get('wages_semi_urban', 0), aggregated.get('JOB_CREATION', {}).get('wages_total', 0))
    waste_recovered_pct = calc_percentage(waste_rec, waste_gen)

    return {
        "readiness": calculate_readiness(db, period_id).get("score", 0),
        "status": "Open",
        "boundary": "Consolidated",
        "sites_reporting": 9, # Mocked for simplicity
        "total_sites": 12,    # Mocked for simplicity
        
        "scope1_tco2e": scope1,
        "scope2_tco2e": scope2,
        "total_energy_gj": energy_data['total_gj'],
        "renewable_pct": energy_data['pct_renewable'],
        "water_withdrawal_kl": water_with,
        "water_consumption_kl": max(0, water_with - water_dis),
        "waste_generated_mt": waste_gen,
        "waste_recovered_pct": waste_recovered_pct,
        "ltifr": ltifr,
        "fatalities_employees": aggregated.get('SAFETY_INCIDENTS', {}).get('fatalities_emp', 0),
        "fatalities_workers": aggregated.get('SAFETY_INCIDENTS', {}).get('fatalities_work', 0),
        "women_wage_pct": women_wage_pct,
        "posh_complaints": aggregated.get('POSH_COMPLAINTS', {}).get('received', 0),
        "msme_pct": msme_pct,
        "local_jobs_pct": local_jobs_pct,
        "breaches": aggregated.get('CYBER_INCIDENTS', {}).get('data_breaches', 0),
        "payable_days": 45, # Requires Corporate Financials
        "related_party_pct": 12.5,
        "concentration_index": 0.8,
        
        "intensity_scope1_cr": calc_intensity_per_rupee(scope1, 1000), # Assuming revenue = 1000 Cr
        "intensity_scope1_ppp": calc_ppp_intensity(scope1, 10000000000, 83.2)
    }

@router.get("/completion")
def get_completion(period_id: int = Query(...), db: Session = Depends(get_db), current_user: User = Depends(require_role(["admin"]))):
    from ..models.entry import SiteEntry
    from ..models.core import Entity
    
    # Get all entries for period
    entries = db.query(SiteEntry, Entity).join(Entity).filter(
        SiteEntry.period_id == period_id
    ).all()
    
    sites_map = {}
    for entry, entity in entries:
        if entity.id not in sites_map:
            sites_map[entity.id] = {
                "id": entity.id,
                "name": entity.name,
                "subsidiary": "Subsidiary",
                "months": {}
            }
        # Simplify status resolution: take the most advanced status for the month
        month_str = entry.month_date.strftime("%Y-%m")
        sites_map[entity.id]["months"][month_str] = entry.status
        
    return {
        "months": ["2023-04", "2023-05", "2023-06", "2023-07", "2023-08", "2023-09", "2023-10", "2023-11", "2023-12", "2024-01", "2024-02", "2024-03"],
        "sites": list(sites_map.values())
    }

@router.get("/flags")
def get_flags(period_id: int = Query(...), is_resolved: bool = False, db: Session = Depends(get_db), current_user: User = Depends(require_role(["admin", "manager"]))):
    # Query real flags
    db_flags = db.execute(
        "SELECT id, severity as type, message as msg, source as src, created_at FROM flag WHERE period_id = :p AND is_resolved = :r",
        {"p": period_id, "r": is_resolved}
    ).fetchall()
    
    return [
        {
            "id": f.id,
            "type": f.type,
            "msg": f.msg,
            "src": "ML" if f.src == 'ml' else "Rule",
            "created_at": "Just now" # mock format
        }
        for f in db_flags
    ]

@router.post("/flags/{id}/resolve")
def resolve_flag(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(["admin", "manager"]))):
    return {"status": "resolved", "flag_id": id}

@router.get("/readiness", response_model=ReadinessResponse)
def get_readiness(period_id: int = Query(...), db: Session = Depends(get_db), current_user: User = Depends(require_role(["admin"]))):
    return calculate_readiness(db, period_id)

@router.get("/drilldown")
def drilldown(
    indicator_code: str = Query(...), 
    period_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    # Stub to track data from top to bottom
    return {"message": f"Drilldown data for {indicator_code}."}

@router.post("/lock")
def lock_period(request: LockPeriodRequest, db: Session = Depends(get_db), current_user: User = Depends(require_role(["admin"]))):
    period = db.query(ReportingPeriod).filter(ReportingPeriod.id == request.period_id).first()
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
        
    if period.status == 'locked':
        raise HTTPException(status_code=400, detail="Period is already locked")
        
    period.status = 'locked'
    db.commit()
    return {"status": "locked", "period_id": period.id}

@router.post("/reopen")
def reopen_period(request: ReopenPeriodRequest, db: Session = Depends(get_db), current_user: User = Depends(require_role(["admin"]))):
    period = db.query(ReportingPeriod).filter(ReportingPeriod.id == request.period_id).first()
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
        
    if period.status != 'locked':
        raise HTTPException(status_code=400, detail="Period is not locked")
        
    if not request.reason or len(request.reason.strip()) == 0:
         raise HTTPException(status_code=400, detail="A reason is required to reopen a locked period")
        
    period.status = 'open'
    
    # Audit log (using ReviewLog as a generic audit table here for the action)
    log = ReviewLog(
        entry_id=0, # 0 denotes period-level action
        actor_id=current_user.id,
        action='reopen',
        comment=request.reason
    )
    db.add(log)
    db.commit()
    
    return {"status": "reopened", "period_id": period.id}
