"""
Complete database fix - deletes old DB and creates new one with all columns
"""
import os
import sys
import time

def fix_database():
    print("=" * 60)
    print("Database Column Fix")
    print("=" * 60)
    print()
    
    # Check if backend is running
    print("⚠️  IMPORTANT: Make sure backend is STOPPED before continuing!")
    print("   Press Ctrl+C in the backend terminal to stop it.")
    print()
    response = input("Is the backend stopped? (yes/no): ")
    if response.lower() != 'yes':
        print("Please stop the backend first, then run this script again.")
        sys.exit(0)
    
    print()
    print("Step 1: Deleting old database files...")
    
    # Delete both database files
    db_files = ['student_buddy.db', 'student_learning_buddy.db']
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print(f"   ✓ Deleted {db_file}")
            except Exception as e:
                print(f"   ✗ Could not delete {db_file}: {e}")
                print(f"   Make sure backend is completely stopped!")
                sys.exit(1)
        else:
            print(f"   ℹ {db_file} not found (already deleted)")
    
    print()
    print("Step 2: Creating new database with all columns...")
    
    # Import after deleting old DB
    from app.database import Base, engine
    from app.models import User, Student, StudySession, QuizAttempt
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("   ✓ Database tables created successfully!")
        print("   ✓ All columns are now present:")
        print("      - users table")
        print("      - students table (with all new columns)")
        print("      - study_sessions table")
        print("      - quiz_attempts table")
    except Exception as e:
        print(f"   ✗ Error creating tables: {e}")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("Database Fix Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Start backend: start_backend.bat")
    print("2. Clear browser: localStorage.clear() in console (F12)")
    print("3. Sign up as new user")
    print("4. Create profile - should work now!")
    print()

if __name__ == "__main__":
    fix_database()
