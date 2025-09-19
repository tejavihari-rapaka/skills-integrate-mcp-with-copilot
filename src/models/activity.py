"""Activity model for database storage."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Activity(Base):
    """Activity model for storing activity information."""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    schedule = Column(String)
    max_participants = Column(Integer)

    # Relationship to participants
    participants = relationship("Participant", back_populates="activity")