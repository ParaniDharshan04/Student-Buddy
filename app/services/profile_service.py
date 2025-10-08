from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models import Student, StudySession, QuizAttempt
from app.schemas.profile import ProfileStats
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

class ProfileService:
    def __init__(self):
        pass
    
    def create_student_profile(
        self, 
        db: Session, 
        name: str, 
        email: str = None, 
        date_of_birth = None,
        phone_number: str = None,
        school_name: str = None,
        grade_level: str = None,
        major_field: str = None,
        preferred_subjects: List[str] = None,
        learning_style: str = None,
        study_goals: str = None,
        bio: str = None
    ) -> Student:
        """
        Create a new student profile
        
        Args:
            db: Database session
            name: Student's name
            email: Optional email address
            date_of_birth: Date of birth
            phone_number: Phone number
            school_name: School or college name
            grade_level: Current grade level
            major_field: Major or field of study
            preferred_subjects: List of preferred subjects
            learning_style: Preferred learning style
            study_goals: Learning goals
            bio: Short bio
            
        Returns:
            Created Student object
        """
        try:
            # Check if email already exists
            if email:
                existing_student = db.query(Student).filter(Student.email == email).first()
                if existing_student:
                    raise ValueError(f"Student with email {email} already exists")
            
            # Create student
            student = Student(
                name=name,
                email=email,
                date_of_birth=date_of_birth,
                phone_number=phone_number,
                school_name=school_name,
                grade_level=grade_level,
                major_field=major_field,
                preferred_subjects=json.dumps(preferred_subjects) if preferred_subjects else None,
                learning_style=learning_style,
                study_goals=study_goals,
                bio=bio,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.add(student)
            db.commit()
            db.refresh(student)
            
            logger.info(f"Created student profile for {name} with ID {student.id}")
            return student
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating student profile: {str(e)}")
            raise
    
    def get_student_profile(self, db: Session, student_id: int) -> Optional[Student]:
        """
        Get student profile by ID
        
        Args:
            db: Database session
            student_id: Student's ID
            
        Returns:
            Student object or None if not found
        """
        return db.query(Student).filter(Student.id == student_id).first()
    
    def get_student_by_email(self, db: Session, email: str) -> Optional[Student]:
        """
        Get student profile by email
        
        Args:
            db: Database session
            email: Student's email
            
        Returns:
            Student object or None if not found
        """
        return db.query(Student).filter(Student.email == email).first()
    
    def update_student_profile(
        self, 
        db: Session, 
        student_id: int, 
        **updates
    ) -> Optional[Student]:
        """
        Update student profile
        
        Args:
            db: Database session
            student_id: Student's ID
            **updates: Fields to update
            
        Returns:
            Updated Student object or None if not found
        """
        try:
            student = db.query(Student).filter(Student.id == student_id).first()
            if not student:
                return None
            
            # Update fields
            for field, value in updates.items():
                if hasattr(student, field) and value is not None:
                    if field == 'preferred_subjects' and isinstance(value, list):
                        setattr(student, field, json.dumps(value))
                    else:
                        setattr(student, field, value)
            
            student.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(student)
            
            logger.info(f"Updated student profile {student_id}")
            return student
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating student profile: {str(e)}")
            raise
    
    def delete_student_profile(self, db: Session, student_id: int) -> bool:
        """
        Delete student profile and all associated data
        
        Args:
            db: Database session
            student_id: Student's ID
            
        Returns:
            True if deleted, False if not found
        """
        try:
            student = db.query(Student).filter(Student.id == student_id).first()
            if not student:
                return False
            
            # Delete associated data first
            db.query(StudySession).filter(StudySession.student_id == student_id).delete()
            db.query(QuizAttempt).filter(QuizAttempt.student_id == student_id).delete()
            
            # Delete student
            db.delete(student)
            db.commit()
            
            logger.info(f"Deleted student profile {student_id}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting student profile: {str(e)}")
            raise
    
    def get_student_stats(self, db: Session, student_id: int) -> ProfileStats:
        """
        Get comprehensive statistics for a student
        
        Args:
            db: Database session
            student_id: Student's ID
            
        Returns:
            ProfileStats object with learning statistics
        """
        try:
            # Count questions asked
            total_questions = db.query(StudySession)\
                .filter(StudySession.student_id == student_id)\
                .filter(StudySession.session_type == "question")\
                .count()
            
            # Count quizzes taken
            total_quizzes = db.query(QuizAttempt)\
                .filter(QuizAttempt.student_id == student_id)\
                .count()
            
            # Count notes summarized
            total_notes = db.query(StudySession)\
                .filter(StudySession.student_id == student_id)\
                .filter(StudySession.session_type == "notes")\
                .count()
            
            # Calculate average quiz score
            avg_score_result = db.query(func.avg(QuizAttempt.score))\
                .filter(QuizAttempt.student_id == student_id)\
                .scalar()
            average_quiz_score = float(avg_score_result) if avg_score_result else None
            
            # Get most studied topics
            most_studied_topics = self._get_most_studied_topics(db, student_id)
            
            # Calculate learning streak
            learning_streak = self._calculate_learning_streak(db, student_id)
            
            # Estimate total study time
            total_study_time = self._estimate_total_study_time(db, student_id)
            
            return ProfileStats(
                total_questions_asked=total_questions,
                total_quizzes_taken=total_quizzes,
                total_notes_summarized=total_notes,
                average_quiz_score=round(average_quiz_score, 2) if average_quiz_score else None,
                most_studied_topics=most_studied_topics,
                learning_streak=learning_streak,
                total_study_time=total_study_time
            )
            
        except Exception as e:
            logger.error(f"Error getting student stats: {str(e)}")
            # Return empty stats on error
            return ProfileStats(
                total_questions_asked=0,
                total_quizzes_taken=0,
                total_notes_summarized=0,
                average_quiz_score=None,
                most_studied_topics=[],
                learning_streak=0,
                total_study_time=0
            )
    
    def _get_most_studied_topics(self, db: Session, student_id: int, limit: int = 5) -> List[str]:
        """Get most frequently studied topics"""
        try:
            # Get topics from study sessions
            topic_counts = db.query(StudySession.topic, func.count(StudySession.topic))\
                .filter(StudySession.student_id == student_id)\
                .filter(StudySession.topic.isnot(None))\
                .group_by(StudySession.topic)\
                .order_by(desc(func.count(StudySession.topic)))\
                .limit(limit)\
                .all()
            
            return [topic for topic, count in topic_counts if topic]
            
        except Exception as e:
            logger.error(f"Error getting most studied topics: {str(e)}")
            return []
    
    def _calculate_learning_streak(self, db: Session, student_id: int) -> int:
        """Calculate current learning streak in days"""
        try:
            # Get all study dates (questions, quizzes, notes)
            study_dates = set()
            
            # Add question dates
            question_dates = db.query(func.date(StudySession.created_at))\
                .filter(StudySession.student_id == student_id)\
                .distinct()\
                .all()
            study_dates.update([date[0] for date in question_dates])
            
            # Add quiz dates
            quiz_dates = db.query(func.date(QuizAttempt.completed_at))\
                .filter(QuizAttempt.student_id == student_id)\
                .distinct()\
                .all()
            study_dates.update([date[0] for date in quiz_dates if date[0]])
            
            if not study_dates:
                return 0
            
            # Sort dates in descending order
            sorted_dates = sorted(study_dates, reverse=True)
            
            # Calculate streak
            streak = 0
            current_date = datetime.now().date()
            
            for study_date in sorted_dates:
                if study_date == current_date or study_date == current_date - timedelta(days=streak):
                    streak += 1
                    current_date = study_date
                else:
                    break
            
            return streak
            
        except Exception as e:
            logger.error(f"Error calculating learning streak: {str(e)}")
            return 0
    
    def _estimate_total_study_time(self, db: Session, student_id: int) -> int:
        """Estimate total study time in minutes"""
        try:
            total_time = 0
            
            # Estimate time for questions (2 minutes each)
            question_count = db.query(StudySession)\
                .filter(StudySession.student_id == student_id)\
                .filter(StudySession.session_type == "question")\
                .count()
            total_time += question_count * 2
            
            # Add actual quiz time or estimate (1.5 minutes per question)
            quiz_times = db.query(QuizAttempt.time_taken)\
                .filter(QuizAttempt.student_id == student_id)\
                .all()
            
            for time_taken in quiz_times:
                if time_taken[0]:
                    total_time += time_taken[0] // 60  # Convert seconds to minutes
                else:
                    total_time += 8  # Estimate 8 minutes per quiz
            
            # Estimate time for notes (3 minutes each)
            notes_count = db.query(StudySession)\
                .filter(StudySession.student_id == student_id)\
                .filter(StudySession.session_type == "notes")\
                .count()
            total_time += notes_count * 3
            
            return total_time
            
        except Exception as e:
            logger.error(f"Error estimating study time: {str(e)}")
            return 0
    
    def get_all_students(self, db: Session, skip: int = 0, limit: int = 100) -> List[Student]:
        """
        Get all student profiles with pagination
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Student objects
        """
        return db.query(Student)\
            .order_by(Student.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def search_students(self, db: Session, query: str, limit: int = 20) -> List[Student]:
        """
        Search students by name or email
        
        Args:
            db: Database session
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching Student objects
        """
        search_term = f"%{query}%"
        return db.query(Student)\
            .filter(
                (Student.name.ilike(search_term)) |
                (Student.email.ilike(search_term))
            )\
            .order_by(Student.name)\
            .limit(limit)\
            .all()