import logging
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.database import SessionLocal
from app.db.models import JobJob, User, AlertPreference
from app.services.email_service import EmailService
from app.services.job_enhancer import analyze_job

logger = logging.getLogger(__name__)

def process_alerts():
    """
    Finds new jobs scraped in the last few hours
    and matches them against user preferences.
    """
    db: Session = SessionLocal()
    email_service = EmailService()
    
    # We look for jobs created in the last 6 hours
    time_threshold = datetime.utcnow() - timedelta(hours=6)
    
    try:
        new_jobs = db.query(JobJob).filter(JobJob.created_at >= time_threshold).all()
        if not new_jobs:
            logger.info("No new jobs in the given timeframe.")
            return

        users = db.query(User).filter(User.is_active == True).all()
        
        for user in users:
            pref = db.query(AlertPreference).filter(AlertPreference.user_id == user.id, AlertPreference.email_alerts == True).first()
            if not pref or not pref.keywords:
                continue
                
            # Match keywords
            keywords = [k.strip().lower() for k in pref.keywords.split(',')]
            matched_jobs = []
            
            for job in new_jobs:
                job_desc = (job.description or "").lower()
                job_title = (job.job_title or "").lower()
                job_skills = (job.skills or "").lower()
                
                # If any keyword is found in title, skills or description
                for k in keywords:
                    if k in job_title or k in job_skills or k in job_desc:
                        
                        enhancement = analyze_job(job_title, job.company, job_desc, job_skills, keywords)
                        
                        # Apply Fresher check - highlight it
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
                        break # No need to match multiple keywords for same job
            
            if matched_jobs:
                logger.info(f"User {user.email} matched {len(matched_jobs)} new jobs.")
                email_service.send_job_alerts(user.email, user.name, matched_jobs)

    except Exception as e:
        logger.error(f"Error processing alerts: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    process_alerts()
