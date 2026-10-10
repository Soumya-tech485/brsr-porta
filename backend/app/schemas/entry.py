from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import date

class EntryCreate(BaseModel):
    indicator_id: int
    sub_key: Optional[str] = ''
    value_num: Optional[float] = None
    value_text: Optional[str] = None

class BulkEntryRequest(BaseModel):
    site_id: int
    period_id: int
    month_date: date
    entries: List[EntryCreate]

class SubmitRequest(BaseModel):
    site_id: int
    period_id: int
    month_date: date

class EntryResponse(BaseModel):
    id: int
    indicator_id: int
    sub_key: str
    value_num: Optional[float]
    value_text: Optional[str]
    status: str

    class Config:
        from_attributes = True

class IndicatorResponse(BaseModel):
    id: int
    code: str
    unit: str
    principle: Optional[str]
    sub_keys: Optional[Any]
    evidence_required: bool
    evidence_hint: Optional[str]

    class Config:
        from_attributes = True
