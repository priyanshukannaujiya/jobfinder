from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import sys
import os
import subprocess

router = APIRouter()

class ScrapeResponse(BaseModel):
    message: str
    status: str

def trigger_scraper():
    # Execute the scraper python script
    # This works if the backend is running in the same environment or can access it
    scraper_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../scraper/main_scraper.py"))
    
    try:
        # Assuming python is in path for the environment
        subprocess.run(["python", scraper_script_path], check=True)
    except Exception as e:
        print(f"Scraper failed: {e}")

@router.post("/", response_model=ScrapeResponse)
def trigger_scraping(background_tasks: BackgroundTasks):
    """
    Manually trigger the scraping engine. 
    Runs in the background so it doesn't block the API.
    """
    background_tasks.add_task(trigger_scraper)
    return {"message": "Scraping job started in the background", "status": "processing"}
