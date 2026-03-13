import logging
import sys
import os

# Add the root directory to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper.spiders.internshala import InternshalaSpider
from scraper.spiders.linkedin import LinkedInSpider
from scraper.processors.cleaner import clean_jobs_data
from scraper.ingestion.db import upsert_jobs
from scraper.ingestion.gsheets import upload_to_gsheets

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_scrapers():
    logger.info("Starting up the job scrapers...")
    all_jobs = []
    
    # 1. Scrape Internshala
    internshala_spider = InternshalaSpider()
    internshala_jobs = internshala_spider.scrape()
    logger.info(f"Found {len(internshala_jobs)} jobs from Internshala.")
    all_jobs.extend(internshala_jobs)
    
    # 2. Scrape LinkedIn
    linkedin_spider = LinkedInSpider()
    linkedin_jobs = linkedin_spider.scrape()
    logger.info(f"Found {len(linkedin_jobs)} jobs from LinkedIn.")
    all_jobs.extend(linkedin_jobs)
    
    if not all_jobs:
        logger.warning("No jobs were scraped. Exiting.")
        return
        
    # 3. Process & Clean Data
    logger.info("Cleaning job data...")
    cleaned_df = clean_jobs_data(all_jobs)
    logger.info(f"Data cleaned. Total valid records: {len(cleaned_df)}")
    
    # 4. Ingest to DB
    logger.info("Ingesting records into local SQLite database...")
    upsert_jobs(cleaned_df)
    
    # 5. Push to Google Sheets
    # Need user to define GSHEET_URL in their .env
    gsheet_url = os.getenv("GSHEET_URL", "")
    if gsheet_url:
        logger.info(f"Syncing new records to Google Sheets at {gsheet_url}...")
        upload_to_gsheets(cleaned_df, gsheet_url)
    else:
        logger.warning("No GSHEET_URL found in .env. Skipping Google Sheets upload.")
        
    logger.info("Scraping and Data Ingestion pipeline complete!")

if __name__ == "__main__":
    run_scrapers()
