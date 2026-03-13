from fastapi import FastAPI
from app.api.endpoints import jobs, preferences, scrape
from app.db.database import engine, Base
from app.core.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for job scraping, filtering, and alert management",
    version="1.0.0"
)

# Includes routers
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
app.include_router(preferences.router, prefix="/preferences", tags=["Preferences"])
app.include_router(scrape.router, prefix="/scrape", tags=["Scrape"])

@app.get("/")
def root():
    return {"message": "Welcome to the JobMaker API!"}
