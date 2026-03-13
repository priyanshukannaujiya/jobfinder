import sys
import logging
sys.path.insert(0, './backend')
logging.basicConfig(level=logging.INFO)

from app.db.database import SessionLocal
from app.db.models import JobJob, User, AlertPreference
from app.services.alert_manager import process_alerts

db = SessionLocal()
print("Total jobs in DB:", len(db.query(JobJob).all()))
users = db.query(User).all()
print("Users in DB:", [u.email for u in users])

print("\n--- Running Process Alerts Manually ---\n")
process_alerts()
print("\n--- Finished ---\n")
