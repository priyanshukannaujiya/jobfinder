# JobMaker — Automated Job Search, Scraping and Alerting Platform

JobMaker is a modular job discovery platform designed to collect job listings, process and store job data, and make opportunities easier to search and monitor. The repository separates the scraping engine, FastAPI backend, automation workflows, and dashboard frontend.

## Project Overview

Finding relevant job openings across multiple platforms can be time-consuming. JobMaker is structured to automate job-data collection and organize the results through a backend API and a user-facing dashboard.

## Key Components

- **Job scraping engine:** Organizes platform-specific spiders, data processors, and ingestion logic.
- **Data processing:** Uses pandas-based processing modules to clean and prepare scraped job records.
- **Backend API:** FastAPI services expose application functionality and use Pydantic schemas and SQLAlchemy models.
- **Database layer:** Stores job and user-related data through SQLAlchemy and PostgreSQL connectivity.
- **Workflow automation:** Apache Airflow DAGs provide a place to schedule recurring scraping workflows.
- **Dashboard:** A Streamlit frontend provides the user-facing interface.

## Technology Stack

| Technology | Role |
|---|---|
| Python | Core application and scraping logic |
| FastAPI | Backend REST API |
| Streamlit | Dashboard |
| PostgreSQL | Relational data storage |
| SQLAlchemy | Database ORM |
| Pydantic | Data validation and settings |
| pandas | Data cleaning and processing |
| Apache Airflow | Workflow scheduling |
| Uvicorn | ASGI application server |

## Repository Structure

```text
jobfinder/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   └── requirements.txt
├── scraper/
│   ├── spiders/
│   ├── processors/
│   ├── ingestion/
│   └── main_scraper.py
├── airflow/
│   └── dags/
├── frontend/
│   ├── components/
│   ├── utils/
│   └── app.py
└── .env.example
```

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- A virtual environment
- Apache Airflow if you intend to run scheduled workflows

### Backend setup

```bash
cd backend
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS / Linux:
```bash
source .venv/bin/activate
```

Install backend dependencies and start the API:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Configure database and application environment variables using the project's `.env.example` before running services that require external credentials.

> Scraper, Airflow, and dashboard setup may have separate dependency files. Refer to each component's requirements and configuration before starting it.

## Relevant Keywords

Job search automation, job scraper, job alerts, FastAPI, Python, web scraping, Apache Airflow, PostgreSQL, Streamlit dashboard, data engineering.

## Repository

https://github.com/priyanshukannaujiya/jobfinder

## Author

[Priyanshu Kannaujiya](https://github.com/priyanshukannaujiya)
