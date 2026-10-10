from pydantic import BaseModel
from datetime import date

class ReviewRequest(BaseModel):
    site_id: int
    period_id: int
    month_date: date

class ReturnRequest(ReviewRequest):
    comment: str
