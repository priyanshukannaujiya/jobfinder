import pandas as pd
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.app.services.job_enhancer import analyze_job

logger = logging.getLogger(__name__)

def clean_jobs_data(jobs_data: list) -> pd.DataFrame:
    """
    Cleans raw job data using Pandas.
    Expected input: List of dictionaries.
    """
    if not jobs_data:
        logger.warning("No data to clean.")
        return pd.DataFrame()

    df = pd.DataFrame(jobs_data)

    # Expected columns: job_title, company, location, skills, experience_level, description, link, posting_date, source

    # 1. Drop records where essential fields are null
    essential_cols = ['job_title', 'company', 'link']
    for col in essential_cols:
        if col in df.columns:
            df.dropna(subset=[col], inplace=True)

    # 2. Standardize titles (title casing, removing extra spaces)
    if 'job_title' in df.columns:
        df['job_title'] = df['job_title'].str.strip().str.title()
    
    # 3. Standardize company names
    if 'company' in df.columns:
        df['company'] = df['company'].str.strip().str.title()

    # 4. Format dates
    # Assuming posting_date might come in various formats, coerce errors to NaT if necessary
    if 'posting_date' in df.columns:
        df['posting_date'] = pd.to_datetime(df['posting_date'], errors='coerce')
        # Fill missing dates with today's date or handle appropriately
        df['posting_date'] = df['posting_date'].fillna(pd.Timestamp.utcnow())

    # 5. Fill empty strings or nulls for non-essential columns
    fill_defaults = {
        'location': 'Remote / Unspecified',
        'skills': 'Not Specified',
        'experience_level': 'Entry Level',
        'description': '',
        'source': 'Unknown'
    }
    for col, default_val in fill_defaults.items():
        if col in df.columns:
            df[col] = df[col].fillna(default_val)
        else:
            df[col] = default_val

    # 6. AI-based Enhance Jobs (Extract Tech Stack, Job Type, and Project Request)
    tech_stacks = []
    job_types = []
    recommended_projects = []
    
    for idx, row in df.iterrows():
        title = row.get('job_title', '')
        company = row.get('company', '')
        desc = row.get('description', '')
        skills = row.get('skills', '')
        
        # We pass an empty list for user_keywords because we just want general stats 
        # (not matching against a specific user during general DB ingestion)
        analysis = analyze_job(title, company, desc, skills, [])
        
        # job_type
        if analysis['is_fresher']:
            job_types.append('Internship' if 'intern' in str(title).lower() else 'Entry Level')
        else:
            job_types.append('Full-Time' if 'contract' not in str(title).lower() else 'Contract')
            
        tech_stacks.append(','.join(analysis['actual_stack']))
        recommended_projects.append(analysis['suggested_project'])
        
    df['job_type'] = job_types
    df['tech_stack'] = tech_stacks
    df['recommended_project'] = recommended_projects

    # Return cleaned records as a list of dictionaries for the DB ingestion
    return df
