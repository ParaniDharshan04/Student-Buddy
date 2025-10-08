"""
Script to remove all user credentials from the database (no confirmation)
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User

def clear_all_users():
    """Remove all users from the database"""
    db = SessionLocal()
    try:
        # Count users before deletion
        user_count = db.query(User).count()
        
        if user_count == 0:
            print("✓ Database is clean. No users found.")
            return
        
        # Delete all users
        deleted = db.query(User).delete()
        db.commit()
        
        print(f"✓ Deleted {deleted} user(s) from database.")
        print("✓ All user credentials removed successfully.")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Clearing all users from database...")
    clear_all_users()
