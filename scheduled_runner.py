import time
import subprocess
import logging
import os
from datetime import datetime

# Setup basic logging for the runner
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ScheduledRunner")

# How often to run the pipeline, in hours (Default: 12 hours)
RUN_INTERVAL_HOURS = int(os.getenv("RUN_INTERVAL_HOURS", 12))
RUN_INTERVAL_SECONDS = RUN_INTERVAL_HOURS * 3600

def run_pipeline():
    logger.info("=========================================")
    logger.info(f"Starting Scheduled Pipeline Run at {datetime.now()}")
    logger.info("=========================================")
    
    # 1. Run the Scraper
    logger.info(">>> Step 1: Running the Job Scraper...")
    try:
        subprocess.run(
            ["python", "scraper/main_scraper.py"], 
            check=True,
            # We assume this script is running from the root 'jobmaker' directory
            cwd=os.path.abspath(os.path.dirname(__file__)) 
        )
        logger.info("Scraping completed successfully.")
    except Exception as e:
        logger.error(f"Scraper failed during scheduled run: {e}")

    # 2. Run the Alert Manager
    logger.info(">>> Step 2: Running the Email Alert Manager...")
    try:
        # We need to ensure PYTHONPATH includes the backend directory
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "backend")
        
        subprocess.run(
            ["python", "backend/app/services/alert_manager.py"], 
            check=True,
            cwd=os.path.abspath(os.path.dirname(__file__)),
            env=env
        )
        logger.info("Alert manager completed successfully.")
    except Exception as e:
        logger.error(f"Alert Manager failed during scheduled run: {e}")

    logger.info(f"Pipeline finished! Sleeping for {RUN_INTERVAL_HOURS} hours.\n")

if __name__ == "__main__":
    logger.info(f"Starting background cron service. Interval set to every {RUN_INTERVAL_HOURS} hours.")
    
    while True:
        try:
            run_pipeline()
            time.sleep(RUN_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            logger.info("Scheduler manually stopped by user. Exiting.")
            break
        except Exception as e:
            logger.error(f"Unexpected error in scheduler loop: {e}")
            # Sleep a bit on failure before retrying to avoid rapid crash loops
            time.sleep(60)
