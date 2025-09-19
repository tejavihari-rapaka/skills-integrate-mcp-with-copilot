"""Database configuration and connection handling."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

# Create SQLite database in the data directory
data_dir = Path(__file__).parent.parent / "data"
data_dir.mkdir(exist_ok=True)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{data_dir}/activities.db"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()