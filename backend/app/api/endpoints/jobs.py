from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.db.models import JobJob
from app.schemas.schemas import JobResponse

router = APIRouter()

@router.get("/", response_model=List[JobResponse])
def get_jobs(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=2000),
    role: Optional[str] = None,
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    fresher_only: bool = Query(False)
):
    query = db.query(JobJob)
    
    if fresher_only:
        query = query.filter(JobJob.is_fresher == True)
    if role:
        query = query.filter(JobJob.job_title.ilike(f"%{role}%"))
    if keyword:
        # Search keyword in description or skills
        query = query.filter(
            (JobJob.description.ilike(f"%{keyword}%")) | 
            (JobJob.skills.ilike(f"%{keyword}%")) |
            (JobJob.job_title.ilike(f"%{keyword}%"))
        )
    if location:
        query = query.filter(JobJob.location.ilike(f"%{location}%"))
        
    jobs = query.order_by(JobJob.posting_date.desc()).offset(skip).limit(limit).all()
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobJob).filter(JobJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
