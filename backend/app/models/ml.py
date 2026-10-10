from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Text, JSON, Boolean
from datetime import datetime
from .base import Base

class Flag(Base):
    __tablename__ = 'flag'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(Integer, ForeignKey('entity.id'), nullable=False)
    period_id = Column(Integer, ForeignKey('reporting_period.id'), nullable=False)
    indicator_id = Column(Integer, ForeignKey('indicator.id'), nullable=False)
    rule_key = Column(String(100))
    severity = Column(String(50))
    message = Column(Text)
    source = Column(Enum('rule', 'ml'), nullable=False)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class MLPrediction(Base):
    __tablename__ = 'ml_prediction'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(Integer, ForeignKey('entity.id'), nullable=False)
    period_id = Column(Integer, ForeignKey('reporting_period.id'), nullable=False)
    indicator_id = Column(Integer, ForeignKey('indicator.id'), nullable=False)
    kind = Column(Enum('anomaly', 'forecast', 'extraction'), nullable=False)
    payload = Column(JSON)
    model_version = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
