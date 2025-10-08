"""
Fix users that don't have student_id linked
"""
from app.database import SessionLocal
from app.models import User, Student
from datetime import datetime

def fix_user_links():
    print("=" * 60)
    print("Fixing User-Student Links")
    print("=" * 60)
    print()
    
    db = SessionLocal()
    try:
        # Get all users
        users = db.query(User).all()
        print(f"Found {len(users)} user(s)")
        print()
        
        fixed = 0
        for user in users:
            print(f"User: {user.username} (ID: {user.id})")
            
            if user.student_id:
                print(f"  ✓ Already has student_id: {user.student_id}")
            else:
                print(f"  ✗ Missing student_id - creating student profile...")
                
                # Check if student exists with same email
                student = db.query(Student).filter(Student.email == user.email).first()
                
                if student:
                    print(f"  ℹ Found existing student with email: {student.id}")
                    user.student_id = student.id
                else:
                    # Create new student
                    student = Student(
                        name=user.full_name,
                        email=user.email,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.add(student)
                    db.commit()
                    db.refresh(student)
                    
                    print(f"  ✓ Created new student: {student.id}")
                    user.student_id = student.id
                
                db.commit()
                db.refresh(user)
                print(f"  ✓ Linked student {user.student_id} to user {user.id}")
                fixed += 1
            
            print()
        
        print("=" * 60)
        print(f"Fixed {fixed} user(s)")
        print("=" * 60)
        print()
        
        if fixed > 0:
            print("Users can now use the app!")
            print("They may need to:")
            print("1. Logout and login again")
            print("2. Clear browser cache: localStorage.clear()")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_user_links()
