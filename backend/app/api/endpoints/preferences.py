from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User, AlertPreference
from app.schemas.schemas import PreferenceCreate, PreferenceResponse, UserResponse
from app.services.alert_manager import process_alerts
from typing import List

router = APIRouter()

@router.post("/", response_model=PreferenceResponse)
def manage_preferences(pref_in: PreferenceCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # First, find or create user based on email
    user = db.query(User).filter(User.email == pref_in.email).first()
    if not user:
        user = User(email=pref_in.email, name=pref_in.email.split('@')[0])
        db.add(user)
        db.commit()
        db.refresh(user)

    # Then upate/create preferences for this user
    pref = db.query(AlertPreference).filter(AlertPreference.user_id == user.id).first()
    if pref:
        pref.keywords = pref_in.keywords
        pref.email_alerts = pref_in.email_alerts
        pref.target_locations = pref_in.target_locations
    else:
        pref = AlertPreference(
            user_id=user.id,
            keywords=pref_in.keywords,
            email_alerts=pref_in.email_alerts,
            target_locations=pref_in.target_locations
        )
        db.add(pref)
        
    db.commit()
    db.refresh(pref)
    
    # Trigger an immediate background task to find matches and email ONLY this user now
    if pref.email_alerts:
        background_tasks.add_task(process_alerts, user_id=user.id, force_send=True)
        
    return pref

@router.get("/{email}", response_model=UserResponse)
def get_user_preferences(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
