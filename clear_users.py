"""
Script to remove all user credentials from the database
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User
import sys

def clear_all_users():
    """Remove all users from the database"""
    db = SessionLocal()
    try:
        # Count users before deletion
        user_count = db.query(User).count()
        
        if user_count == 0:
            print("✓ No users found in database. Database is already clean.")
            return
        
        print(f"Found {user_count} user(s) in database.")
        print("\nWARNING: This will permanently delete all user accounts!")
        print("This action cannot be undone.")
        
        # Ask for confirmation
        response = input("\nAre you sure you want to delete all users? (yes/no): ")
        
        if response.lower() != 'yes':
            print("✗ Operation cancelled. No users were deleted.")
            return
        
        # Delete all users
        deleted = db.query(User).delete()
        db.commit()
        
        print(f"\n✓ Successfully deleted {deleted} user(s) from database.")
        print("✓ All user credentials have been removed.")
        print("\nUsers can now create new accounts from scratch.")
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ Error clearing users: {str(e)}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 50)
    print("Clear All Users - Student Learning Buddy")
    print("=" * 50)
    print()
    clear_all_users()
