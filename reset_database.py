#!/usr/bin/env python3
"""
Reset database - Remove all data and recreate tables
"""

from app.database import engine, Base, SessionLocal
from app.models import Student, StudySession, QuizAttempt
import os

def reset_database():
    """Drop all tables and recreate them"""
    print("🗑️  Resetting database...")
    
    # Drop all tables
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped")
    
    # Recreate all tables
    print("Creating fresh tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created")
    
    print("\n✅ Database reset complete!")
    print("All profiles, study sessions, and quiz attempts have been removed.")
    print("\nYou can now create a fresh profile.")

def clear_all_data():
    """Clear all data but keep table structure"""
    print("🗑️  Clearing all data from database...")
    
    db = SessionLocal()
    try:
        # Delete all quiz attempts
        quiz_count = db.query(QuizAttempt).count()
        db.query(QuizAttempt).delete()
        print(f"✅ Deleted {quiz_count} quiz attempts")
        
        # Delete all study sessions
        session_count = db.query(StudySession).count()
        db.query(StudySession).delete()
        print(f"✅ Deleted {session_count} study sessions")
        
        # Delete all students
        student_count = db.query(Student).count()
        db.query(Student).delete()
        print(f"✅ Deleted {student_count} student profiles")
        
        db.commit()
        print("\n✅ All data cleared successfully!")
        print("Database tables are empty and ready for new data.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error clearing data: {e}")
    finally:
        db.close()

def main():
    print("=" * 60)
    print("DATABASE RESET UTILITY")
    print("=" * 60)
    print("\nChoose an option:")
    print("1. Clear all data (keep table structure)")
    print("2. Reset database (drop and recreate tables)")
    print("3. Cancel")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        confirm = input("\n⚠️  This will delete ALL data. Are you sure? (yes/no): ").strip().lower()
        if confirm == "yes":
            clear_all_data()
        else:
            print("❌ Cancelled")
    elif choice == "2":
        confirm = input("\n⚠️  This will DROP and RECREATE all tables. Are you sure? (yes/no): ").strip().lower()
        if confirm == "yes":
            reset_database()
        else:
            print("❌ Cancelled")
    elif choice == "3":
        print("❌ Cancelled")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
