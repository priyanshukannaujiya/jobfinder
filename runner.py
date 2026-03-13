import sys
import logging
logging.basicConfig(level=logging.INFO)
sys.path.insert(0, './backend')

from app.db.database import engine, Base, SessionLocal
from app.db.models import JobJob, User, AlertPreference
print("Creating tables...")
Base.metadata.create_all(bind=engine)

db = SessionLocal()
print("Tables created. Adding users...")
for email in ['heypk4@gmail.com', 'kannaujiyapriyanshu111@gmail.com']:
    u = db.query(User).filter_by(email=email).first()
    if not u:
        u = User(email=email, name=email.split('@')[0])
        db.add(u)
        db.commit()
        db.refresh(u)
        
    pref = db.query(AlertPreference).filter_by(user_id=u.id).first()
    if not pref:
        pref = AlertPreference(user_id=u.id, keywords='Data Engineer, Python', email_alerts=True)
        db.add(pref)
        db.commit()
print("Users added successfully.")

from app.services.alert_manager import process_alerts
print("Triggering Process Alerts...")
process_alerts()
print("Finished!")
