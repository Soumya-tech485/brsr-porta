from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ReadinessResponse(BaseModel):
    score: float
    total_required: int
    verified_count: int
    gap_list: List[Dict[str, Any]]

class LockPeriodRequest(BaseModel):
    period_id: int

class ReopenPeriodRequest(BaseModel):
    period_id: int
    reason: str
