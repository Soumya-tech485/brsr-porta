from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Text
from datetime import datetime
from .base import Base

class ReviewLog(Base):
    __tablename__ = 'review_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    entry_id = Column(Integer, ForeignKey('site_entry.id'), nullable=False)
    actor_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    action = Column(Enum('submit', 'verify', 'return', 'lock', 'reopen'), nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
