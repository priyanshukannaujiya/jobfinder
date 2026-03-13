import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import insert
import datetime
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(env_path)

# Ensure absolute path for local sqlite
default_db = f"sqlite:///{os.path.join(BASE_DIR, 'jobs.db')}"
DATABASE_URL = os.getenv("DATABASE_URL", default_db)

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class JobJob(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255))
    skills = Column(String(500))
    experience_level = Column(String(100))
    description = Column(Text)
    job_type = Column(String(100))
    tech_stack = Column(Text)
    recommended_project = Column(Text)
    link = Column(String(1000), nullable=False, unique=True)
    posting_date = Column(DateTime)
    source = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Unique constraint on the link to prevent duplicate jobs
    __table_args__ = (UniqueConstraint('link', name='_link_uc'),)

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger(__name__)

def upsert_jobs(cleaned_jobs_df):
    """
    Ingest a Pandas dataframe into the database with UPSERT logic.
    Postgres uses ON CONFLICT DO UPDATE.
    For SQLite (fallback), we will use an alternative or basic merge.
    """
    if cleaned_jobs_df.empty:
        logger.warning("Dataframe is empty, skipping DB insertion.")
        return

    records = cleaned_jobs_df.to_dict(orient='records')
    session = SessionLocal()
    
    try:
        # We need to handle dialect differences
        if 'postgresql' in DATABASE_URL:
            # PostgreSQL specific UPSERT
            stmt = insert(JobJob).values(records)
            update_dict = {
                c.name: c
                for c in stmt.excluded
                if not c.primary_key and c.name != 'created_at'
            }
            stmt = stmt.on_conflict_do_update(
                index_elements=['link'],
                set_=update_dict
            )
            session.execute(stmt)
            session.commit()
            logger.info(f"Successfully upserted {len(records)} records (PostgreSQL).")
        else:
            # SQLite fallback approach (basic loop for simplicity, or we could use sqlite dialect's insert)
            from sqlalchemy.dialects.sqlite import insert as sqlite_insert
            
            # Batching to avoid "too many SQL variables"
            BATCH_SIZE = 50
            for i in range(0, len(records), BATCH_SIZE):
                batch = records[i:i + BATCH_SIZE]
                stmt = sqlite_insert(JobJob).values(batch)
                update_dict = {
                    c.name: c
                    for c in stmt.excluded
                    if not c.primary_key and c.name != 'created_at'
                }
                stmt = stmt.on_conflict_do_update(
                    index_elements=['link'],
                    set_=update_dict
                )
                session.execute(stmt)
            session.commit()
            logger.info(f"Successfully upserted {len(records)} records (SQLite).")
            
    except Exception as e:
        session.rollback()
        logger.error(f"Error upserting to DB: {e}")
    finally:
        session.close()
