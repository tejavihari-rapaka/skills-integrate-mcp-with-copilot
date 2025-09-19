"""Participant model for database storage."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Participant(Base):
    """Model for storing activity participant information."""
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"))

    # Relationship to activity
    activity = relationship("Activity", back_populates="participants")