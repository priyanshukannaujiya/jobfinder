# JobMaker

A highly modular, automated job-scraping and alerting platform.

## Directory Structure

```text
jobmaker/
├── backend/               # FastAPI Backend
│   ├── app/
│   │   ├── api/           # REST API endpoints
│   │   ├── core/          # App configuration & security settings
│   │   ├── db/            # Database connection & models
│   │   ├── schemas/       # Pydantic models (Users, Jobs, Preferences)
│   │   ├── services/      # Business logic
│   │   └── main.py        # FastAPI app entry point
│   └── requirements.txt
├── scraper/               # Job Scraping Engine
│   ├── spiders/           # Web scrapers (LinkedIn, Internshala)
│   ├── processors/        # Pandas data cleaning modules 
│   ├── ingestion/         # DB Upsert logic
│   ├── main_scraper.py    # Trigger for the scraping engine
│   └── requirements.txt
├── airflow/               # Automation
│   └── dags/              # Airflow DAGs for scheduling
├── frontend/              # Streamlit Dashboard
│   ├── components/        # UI components
│   ├── utils/             # Helper functions (e.g., PDF text extraction)
│   ├── app.py             # Main Streamlit app
│   └── requirements.txt
├── .env.example           # Environment variables template
└── README.md              # Project documentation
```
