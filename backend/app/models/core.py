from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Entity(Base):
    __tablename__ = 'entity'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum('group', 'subsidiary', 'bu', 'site'), nullable=False)
    parent_id = Column(Integer, ForeignKey('entity.id'))
    state = Column(String(100))
    country = Column(String(100))
    is_active = Column(Boolean, default=True)
    
    parent = relationship("Entity", remote_side=[id])

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum('engineer', 'manager', 'admin'), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserSite(Base):
    __tablename__ = 'user_site'
    
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    entity_id = Column(Integer, ForeignKey('entity.id'), primary_key=True)
