import sys
import logging
logging.basicConfig(level=logging.INFO)
sys.path.insert(0, './backend')

import os
from dotenv import load_dotenv
load_dotenv('.env')

from app.services.email_service import EmailService
from app.services.job_enhancer import analyze_job

srv = EmailService()
job = {
    'job_title': 'Junior Data Analyst/Intern',
    'company': 'FinGrow Bank',
    'location': 'New York (Hybrid)',
    'skills': 'Python, SQL, Tableau',
    'description': 'Looking for a fresher to analyze finance data using Python and SQL.',
    'link': 'https://google.com',
    'source': 'LinkedIn'
}
enh = analyze_job(job['job_title'], job['company'], job['description'], job['skills'], ['python', 'sql', 'spark'])
job['enhancement'] = enh
job['status_label'] = '🌱 Fresher/Intern Role' if enh['is_fresher'] else '🎯 Professional Role'
jobs = [job]

print('Sending beautiful email...')
try:
    success = srv.send_job_alerts('heypk4@gmail.com', 'Priyanshu', jobs)
    print("Email send status:", success)
except Exception as e:
    import traceback
    traceback.print_exc()
