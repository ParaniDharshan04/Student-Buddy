#!/usr/bin/env python3
"""
Database initialization script for Student Learning Buddy
"""

from app.database import init_db, SessionLocal
from app.models import Student, StudySession, QuizAttempt
import json

def create_sample_data():
    """Create sample data for testing"""
    db = SessionLocal()
    try:
        # Check if sample data already exists
        existing_student = db.query(Student).first()
        if existing_student:
            print("Sample data already exists. Skipping creation.")
            return
        
        # Create sample student
        sample_student = Student(
            name="John Doe",
            email="john.doe@example.com",
            preferred_subjects=json.dumps(["Mathematics", "Physics", "Computer Science"]),
            last_studied_topic="Calculus",
            learning_style="visual"
        )
        
        db.add(sample_student)
        db.commit()
        db.refresh(sample_student)
        
        # Create sample study session
        sample_session = StudySession(
            student_id=sample_student.id,
            session_type="question",
            topic="Calculus",
            content="What is the derivative of x^2?",
            ai_response="The derivative of x^2 is 2x. Here's the step-by-step explanation...",
            metadata=json.dumps({"explanation_style": "simple", "confidence": 0.95})
        )
        
        db.add(sample_session)
        db.commit()
        
        print("Sample data created successfully!")
        print(f"Created student: {sample_student.name}")
        print(f"Created study session: {sample_session.topic}")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Initialize database and create sample data"""
    print("Initializing database...")
    init_db()
    print("Database tables created successfully!")
    
    print("Creating sample data...")
    create_sample_data()
    
    print("Database initialization complete!")

if __name__ == "__main__":
    main()