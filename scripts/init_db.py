#!/usr/bin/env python3
"""Initialize database with tables."""

from sqlalchemy import create_engine
from app.core.config import settings
from app.db.base_class import Base
from app.models import item  # Import all models

def init_db():
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()