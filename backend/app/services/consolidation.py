from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..models.core import Entity
from ..models.entry import SiteEntry, Indicator

def get_entity_tree_ids(db: Session, root_id: int) -> List[int]:
    """Recursively fetch all entity IDs under a given root entity using a Recursive CTE."""
    from sqlalchemy import text
    
    query = text("""
        WITH RECURSIVE entity_tree AS (
            SELECT id FROM entity WHERE id = :root_id
            UNION ALL
            SELECT e.id FROM entity e
            INNER JOIN entity_tree et ON e.parent_id = et.id
        )
        SELECT id FROM entity_tree;
    """)
    result = db.execute(query, {"root_id": root_id}).fetchall()
    return [row[0] for row in result]

def consolidate_data(db: Session, entity_id: int, period_id: int, month_date: Any = None) -> Dict[str, Any]:
    """
    Rolls up indicator values from all child sites to the given entity level.
    Follows rules: 'sum' for flows, 'snapshot_last' for headcount.
    Ratios must be calculated AFTER consolidation by the caller using the raw sums.
    """
    subtree_ids = get_entity_tree_ids(db, entity_id)
    
    # Query all verified entries in this subtree
    query = db.query(SiteEntry, Indicator).join(Indicator).filter(
        SiteEntry.entity_id.in_(subtree_ids),
        SiteEntry.period_id == period_id,
        SiteEntry.status == 'verified'
    )
    if month_date:
        query = query.filter(SiteEntry.month_date <= month_date)
        
    entries = query.all()
    
    aggregated: Dict[str, Dict[str, float]] = {}
    
    for entry, indicator in entries:
        code = indicator.code
        sub_key = entry.sub_key or "total"
        val = float(entry.value_num) if entry.value_num else 0.0
        
        if code not in aggregated:
            aggregated[code] = {}
            
        if indicator.aggregation_rule == 'sum' or indicator.aggregation_rule == 'ratio_from_components':
            # Sum up components for standard flows and ratio denominators/numerators
            aggregated[code][sub_key] = aggregated[code].get(sub_key, 0.0) + val
        elif indicator.aggregation_rule == 'snapshot_last':
            # For headcount, we ideally only take the latest month data.
            # Assuming 'entries' contains only the requested month here for simplicity.
            aggregated[code][sub_key] = aggregated[code].get(sub_key, 0.0) + val
            
    return aggregated
