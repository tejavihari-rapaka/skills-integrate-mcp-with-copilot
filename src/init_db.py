"""Script to initialize the database with initial activities."""

from models.database import SessionLocal, engine, Base
from models import Activity, Participant

# Initial activities data
INITIAL_ACTIVITIES = [
    {
        "name": "Chess Club",
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "initial_participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    {
        "name": "Programming Class",
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "initial_participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    {
        "name": "Gym Class",
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "initial_participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    {
        "name": "Soccer Team",
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "initial_participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    {
        "name": "Basketball Team",
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "initial_participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    {
        "name": "Art Club",
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "initial_participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    {
        "name": "Drama Club",
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "initial_participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    {
        "name": "Math Club",
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "initial_participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    {
        "name": "Debate Team",
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "initial_participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
]

def init_db():
    """Initialize the database with initial activities."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if we already have activities
        if db.query(Activity).first():
            print("Database already initialized")
            return

        # Add activities
        for activity_data in INITIAL_ACTIVITIES:
            participants = activity_data.pop("initial_participants")
            activity = Activity(**activity_data)
            db.add(activity)
            db.commit()

            # Add participants
            for email in participants:
                participant = Participant(email=email, activity_id=activity.id)
                db.add(participant)
            db.commit()

        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()