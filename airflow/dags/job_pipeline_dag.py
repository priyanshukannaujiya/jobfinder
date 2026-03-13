from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'jobmaker',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Run every 6 hours
dag = DAG(
    'job_scraping_and_alerting',
    default_args=default_args,
    description='A DAG to scrape jobs and send email alerts every 6 hours',
    schedule_interval='0 */6 * * *',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['etl'],
)

# Replace with the actual absolute path to your virtual environment's python and scripts
# We assume they are run from within the appropriate environment 

# 1. Run the Scraping Engine
scrape_task = BashOperator(
    task_id='run_job_scraper',
    bash_command='cd /path/to/jobmaker && python scraper/main_scraper.py',
    dag=dag,
)

# 2. Run the Alert Matching & Emailing Logic
alert_task = BashOperator(
    task_id='run_alert_manager',
    # Ensure backend is in PYTHONPATH to allow app.db imports
    bash_command='cd /path/to/jobmaker && PYTHONPATH=backend python backend/app/services/alert_manager.py',
    dag=dag,
)

scrape_task >> alert_task
