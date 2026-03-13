import logging
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.database import SessionLocal
from app.db.models import JobJob, User, AlertPreference
from app.services.email_service import EmailService
from app.services.job_enhancer import analyze_job

logger = logging.getLogger(__name__)

def process_alerts(user_id: int = None, force_send: bool = False):
    """
    Finds new jobs and matches them against user preferences.
    - If user_id is provided, only processes for that user.
    - force_send: ignores the 12-hour interval (used for immediate feedback on submit).
    """
    db: Session = SessionLocal()
    email_service = EmailService()
    
    try:
        query = db.query(User).filter(User.is_active == True)
        if user_id:
            query = query.filter(User.id == user_id)
        users = query.all()
        
        for user in users:
            pref = db.query(AlertPreference).filter(
                AlertPreference.user_id == user.id, 
                AlertPreference.email_alerts == True
            ).first()
            
            if not pref or not pref.keywords:
                continue

            # Check 12 hour interval
            now = datetime.utcnow()
            if not force_send and pref.last_alert_sent:
                if now < pref.last_alert_sent + timedelta(hours=12):
                    logger.info(f"Skipping user {user.email} - within 12h interval.")
                    continue

            # Match for jobs newer than what they last saw
            last_job_id = pref.last_seen_job_id or 0
            new_jobs = db.query(JobJob).filter(JobJob.id > last_job_id).all()
            
            if not new_jobs:
                if force_send:
                    # If they just hit submit, they might expect something, 
                    # but if there are absolutely NO new jobs in the DB at all, we can't send much.
                    # Or we could send top 5 match from all jobs.
                    pass
                continue

            # Match keywords
            keywords = [k.strip().lower() for k in pref.keywords.split(',')] if pref.keywords else []
            targets = [l.strip().lower() for l in pref.target_locations.split(',')] if pref.target_locations else []
            
            matched_jobs = []
            max_seen_id = last_job_id
            
            for job in new_jobs:
                max_seen_id = max(max_seen_id, job.id)
                job_desc = (job.description or "").lower()
                job_title = (job.job_title or "").lower()
                job_skills = (job.skills or "").lower()
                job_loc = (job.location or "").lower()
                
                if targets:
                    location_ok = any(t in job_loc for t in targets)
                    if not location_ok and "remote" not in targets:
                        continue
                
                for k in keywords:
                    if k in job_title or k in job_skills or k in job_desc:
                        enhancement = analyze_job(job_title, job.company, job_desc, job_skills, keywords)
                        status_label = "🌱 Fresher/Intern Role" if enhancement['is_fresher'] else "🎯 Professional Role"

                        matched_jobs.append({
                            "job_title": job.job_title,
                            "company": job.company,
                            "location": job.location,
                            "skills": job.skills,
                            "link": job.link,
                            "source": job.source,
                            "enhancement": enhancement,
                            "status_label": status_label
                        })
                        break
            
            if matched_jobs:
                logger.info(f"User {user.email} matched {len(matched_jobs)} new jobs.")
                sent = email_service.send_job_alerts(user.email, user.name, matched_jobs)
                if sent:
                    pref.last_alert_sent = now
                    pref.last_seen_job_id = max_seen_id
                    db.commit()
            elif force_send:
                # Update last seen anyway so we don't spam them with no-matches
                pref.last_seen_job_id = max_seen_id
                db.commit()

    except Exception as e:
        logger.error(f"Error processing alerts: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    process_alerts()
