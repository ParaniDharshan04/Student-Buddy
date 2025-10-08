"""
Force recreate database by dropping all tables first
"""
from app.database import engine, Base
from app.models import User, Student, StudySession, QuizAttempt
import os

def force_recreate():
    print("=" * 60)
    print("Force Recreate Database")
    print("=" * 60)
    print()
    
    # Check which database file is being used
    from app.config import settings
    db_url = settings.DATABASE_URL
    print(f"Database URL: {db_url}")
    
    # Extract filename from URL
    if "sqlite:///" in db_url:
        db_file = db_url.replace("sqlite:///./", "").replace("sqlite:///", "")
        print(f"Database file: {db_file}")
        
        if os.path.exists(db_file):
            print(f"File exists: {os.path.getsize(db_file)} bytes")
        else:
            print("File does not exist yet")
    
    print()
    print("Step 1: Dropping all existing tables...")
    try:
        Base.metadata.drop_all(bind=engine)
        print("✓ All tables dropped")
    except Exception as e:
        print(f"Note: {e}")
    
    print()
    print("Step 2: Creating all tables with current schema...")
    Base.metadata.create_all(bind=engine)
    print("✓ All tables created")
    
    print()
    print("Step 3: Verifying Student table columns...")
    from sqlalchemy import inspect
    inspector = inspect(engine)
    columns = inspector.get_columns('students')
    
    print("Students table columns:")
    for col in columns:
        print(f"  - {col['name']} ({col['type']})")
    
    print()
    print("=" * 60)
    print("Database Recreation Complete!")
    print("=" * 60)
    print()
    
    expected_columns = ['id', 'name', 'email', 'date_of_birth', 'phone_number', 
                       'school_name', 'grade_level', 'major_field', 'preferred_subjects',
                       'last_studied_topic', 'learning_style', 'study_goals', 'bio',
                       'created_at', 'updated_at']
    
    actual_columns = [col['name'] for col in columns]
    missing = set(expected_columns) - set(actual_columns)
    
    if missing:
        print(f"⚠️  WARNING: Missing columns: {missing}")
        print("The database may still have issues!")
    else:
        print("✓ All expected columns are present!")
        print()
        print("Next steps:")
        print("1. Start backend: start_backend.bat")
        print("2. Clear browser: localStorage.clear()")
        print("3. Sign up as new user")

if __name__ == "__main__":
    force_recreate()
