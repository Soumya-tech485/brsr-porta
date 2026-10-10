from sqlalchemy.orm import Session
from typing import Dict, Any, List
from ..models.entry import SiteEntry, Indicator
from ..models.core import Entity

def calculate_readiness(db: Session, period_id: int) -> Dict[str, Any]:
    """
    Calculates the percentage of required Essential and Core indicators 
    that have been successfully verified across all sites.
    """
    # Find all sites
    sites = db.query(Entity).filter(Entity.type == 'site', Entity.is_active == True).all()
    site_ids = [s.id for s in sites]
    
    if not site_ids:
        return {"score": 0.0, "gap_list": []}
        
    # Find all required site-level indicators (Core or Essential)
    required_indicators = db.query(Indicator).filter(
        Indicator.level == 'site',
        (Indicator.is_core == True) | (Indicator.tier == 'Essential')
    ).all()
    
    total_required = len(required_indicators) * len(site_ids)
    if total_required == 0:
         return {"score": 100.0, "gap_list": []}
         
    required_indicator_ids = [ind.id for ind in required_indicators]
    
    # Query verified entries for those indicators/sites
    # We only count it as verified if at least one entry exists for that indicator/site combination
    # and it is verified. (Simplified for demo)
    verified_entries = db.query(SiteEntry.entity_id, SiteEntry.indicator_id).filter(
        SiteEntry.period_id == period_id,
        SiteEntry.entity_id.in_(site_ids),
        SiteEntry.indicator_id.in_(required_indicator_ids),
        SiteEntry.status == 'verified'
    ).distinct().all()
    
    verified_count = len(verified_entries)
    score = (verified_count / total_required) * 100
    
    # Generate gap list
    verified_pairs = {(e.entity_id, e.indicator_id) for e in verified_entries}
    gap_list = []
    
    # Pre-fetch names for gap list clarity
    site_dict = {s.id: s.name for s in sites}
    ind_dict = {i.id: i.code for i in required_indicators}
    
    for sid in site_ids:
        for iid in required_indicator_ids:
            if (sid, iid) not in verified_pairs:
                gap_list.append({
                    "site_id": sid,
                    "site_name": site_dict.get(sid),
                    "indicator_id": iid,
                    "indicator_code": ind_dict.get(iid)
                })
                
    return {
        "score": round(score, 2),
        "total_required": total_required,
        "verified_count": verified_count,
        "gap_list": gap_list
    }
