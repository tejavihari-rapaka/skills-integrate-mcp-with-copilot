"""
High School Management System API

A FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import os
from pathlib import Path

from models import Activity, Participant
from models.database import SessionLocal, engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    """Get all activities with their participants."""
    activities = db.query(Activity).all()
    
    # Convert to dictionary format for compatibility
    return {
        activity.name: {
            "description": activity.description,
            "schedule": activity.schedule,
            "max_participants": activity.max_participants,
            "participants": [p.email for p in activity.participants]
        }
        for activity in activities
    }


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Sign up a student for an activity"""
    # Get activity from database
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if student is already signed up
    existing_participant = db.query(Participant).filter(
        Participant.activity_id == activity.id,
        Participant.email == email
    ).first()
    if existing_participant:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Check if activity is full
    participant_count = db.query(Participant).filter(
        Participant.activity_id == activity.id
    ).count()
    if participant_count >= activity.max_participants:
        raise HTTPException(
            status_code=400,
            detail="Activity is full"
        )

    # Add new participant
    new_participant = Participant(email=email, activity_id=activity.id)
    db.add(new_participant)
    db.commit()
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Unregister a student from an activity"""
    # Get activity from database
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Find participant
    participant = db.query(Participant).filter(
        Participant.activity_id == activity.id,
        Participant.email == email
    ).first()
    if not participant:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove participant
    db.delete(participant)
    db.commit()
    return {"message": f"Unregistered {email} from {activity_name}"}
