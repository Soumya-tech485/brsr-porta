from sqlalchemy import Column, Integer, String, Float, Enum, Boolean, ForeignKey, DateTime, Date, JSON, Text, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Indicator(Base):
    __tablename__ = 'indicator'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(100), nullable=False)
    format_version = Column(String(50), nullable=False)
    section = Column(String(100))
    principle = Column(String(100))
    tier = Column(String(50))
    is_core = Column(Boolean, default=False)
    level = Column(String(50))
    data_type = Column(String(50))
    unit = Column(String(50))
    aggregation_rule = Column(String(50))
    formula_key = Column(String(100))
    evidence_required = Column(Boolean, default=False)
    evidence_hint = Column(Text)
    sub_keys = Column(JSON)
    sort_order = Column(Integer, default=0)

class ReportingPeriod(Base):
    __tablename__ = 'reporting_period'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fy_label = Column(String(50), unique=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    boundary = Column(Enum('standalone', 'consolidated'), nullable=False)
    status = Column(Enum('open', 'closed', 'locked'), default='open', nullable=False)
    format_version = Column(String(50), nullable=False)

class SiteEntry(Base):
    __tablename__ = 'site_entry'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(Integer, ForeignKey('entity.id'), nullable=False)
    period_id = Column(Integer, ForeignKey('reporting_period.id'), nullable=False)
    month_date = Column(Date, nullable=False)
    indicator_id = Column(Integer, ForeignKey('indicator.id'), nullable=False)
    sub_key = Column(String(100), default='')
    value_num = Column(DECIMAL(20,4))
    value_text = Column(Text)
    status = Column(Enum('draft', 'submitted', 'returned', 'verified', 'locked'), default='draft')
    entered_by = Column(Integer, ForeignKey('user.id'))
    verified_by = Column(Integer, ForeignKey('user.id'))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    indicator = relationship("Indicator")
