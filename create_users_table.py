"""
Script to create users table in the database
"""
from app.database import engine, Base
from app.models import User, Student, StudySession, QuizAttempt

def create_tables():
    """Create all tables in the database"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ All tables created successfully!")
    print("  - users")
    print("  - students")
    print("  - study_sessions")
    print("  - quiz_attempts")

if __name__ == "__main__":
    create_tables()
