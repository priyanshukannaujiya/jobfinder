from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Job Schemas
class JobResponse(BaseModel):
    id: int
    job_title: str
    company: str
    location: Optional[str] = None
    skills: Optional[str] = None
    experience_level: Optional[str] = None
    description: Optional[str] = None
    job_type: Optional[str] = None
    is_fresher: bool = False
    tech_stack: Optional[str] = None
    recommended_project: Optional[str] = None
    recruiter_name: Optional[str] = None
    recruiter_link: Optional[str] = None
    link: str
    posting_date: Optional[datetime] = None
    source: Optional[str] = None

    class Config:
        from_attributes = True

# Preference Schemas
class PreferenceBase(BaseModel):
    keywords: str
    email_alerts: bool = True
    target_locations: Optional[str] = None

class PreferenceCreate(PreferenceBase):
    email: EmailStr # we use email to map to the user easily

class PreferenceResponse(PreferenceBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    is_active: bool
    preferences: List[PreferenceResponse] = []

    class Config:
        from_attributes = True
