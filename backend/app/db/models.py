from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base
import datetime

class JobJob(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255))
    skills = Column(String(500))
    experience_level = Column(String(100))
    description = Column(Text)
    job_type = Column(String(100))
    tech_stack = Column(Text)
    recommended_project = Column(Text)
    link = Column(String(1000), nullable=False, unique=True)
    posting_date = Column(DateTime)
    source = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (UniqueConstraint('link', name='_link_backend_uc'),)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    preferences = relationship("AlertPreference", back_populates="user")


class AlertPreference(Base):
    __tablename__ = 'alert_preferences'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    keywords = Column(String(500)) # comma separated keywords
    email_alerts = Column(Boolean, default=True)
    target_locations = Column(String(500)) # comma separated
    
    user = relationship("User", back_populates="preferences")
