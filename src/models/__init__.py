from .database import Base, engine, SessionLocal
from .activity import Activity
from .participant import Participant

# Create all tables
Base.metadata.create_all(bind=engine)