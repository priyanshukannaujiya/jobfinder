import os
import gspread
import logging
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

# Load config
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")

def upload_to_gsheets(df: pd.DataFrame, sheet_key_or_url: str):
    """
    Appends the scraped jobs data to a Google Sheet.
    """
    if df.empty:
        logger.info("No data to upload to Google Sheets.")
        return

    if not os.path.exists(CREDENTIALS_FILE):
        logger.error(f"Credentials file not found at {CREDENTIALS_FILE}. Cannot connect to Google Sheets.")
        logger.error("Please provide your exactly named credentials.json to enable this feature.")
        return

    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        client = gspread.authorize(creds)

        # Connect to sheet
        if "https://" in sheet_key_or_url:
            sheet = client.open_by_url(sheet_key_or_url).sheet1
        else:
            sheet = client.open_by_key(sheet_key_or_url).sheet1

        # Fetch existing data to avoid duplicates by link
        try:
            existing_data = sheet.get_all_records()
            existing_links = {row.get('Application Link', '') for row in existing_data}
        except Exception as e:
            logger.warning("Could not fetch existing data or sheet is empty. Assuming no duplicates.")
            existing_links = set()

        # Format dataframe to match the requested spreadsheet columns
        upload_data = []
        for _, row in df.iterrows():
            link = row.get('link', '')
            if link in existing_links:
                continue # Skip duplicates
                
            now = datetime.now()
            upload_data.append([
                now.strftime('%Y-%m-%d'),         # Scraped Date
                now.strftime('%H:%M:%S'),         # Scraped Time
                row.get('job_title', ''),         # Job Title
                row.get('company', ''),             # Company
                row.get('location', ''),          # Location
                row.get('job_type', ''),          # Job Type
                row.get('tech_stack', ''),        # Tech Stack
                row.get('skills', ''),            # Required Skills
                row.get('description', ''),       # Job Description
                row.get('source', ''),            # Source
                link,                             # Application Link
                '',                               # Match Score (calculated dynamically on UI, so leaving blank or generic here)
                row.get('recommended_project', '')# Recommended Project
            ])

        if not upload_data:
            logger.info("All scraped jobs already exist in the Google Sheet. Skipping upload.")
            return

        # Check if headers exist, if not we could add them, but append_rows expects plain rows.
        # It's better if the user manually sets up headers. 
        sheet.append_rows(upload_data)
        logger.info(f"Successfully appended {len(upload_data)} new jobs to Google Sheets!")

    except Exception as e:
        logger.error(f"Failed to upload to Google Sheets: {e}")
