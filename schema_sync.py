"""
schema_sync.py
Script to auto-create or update tables in logistics_db from SQLAlchemy models.
Only use in dev/test environments! DO NOT run in production.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Import your models here (adjust path as needed)
from app.models import Base

# Load environment variables
load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = "logistics_db"

# Only allow in dev/test
if os.getenv("ENV") not in ("dev", "test"):
    raise RuntimeError("schema_sync.py should only be run in dev/test environments!")

engine = create_engine(f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{DB_NAME}")

if __name__ == "__main__":
    print("Creating/updating tables in logistics_db...")
    Base.metadata.create_all(engine)
    print("Schema sync complete.")
