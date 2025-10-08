from sqlalchemy import Column, Integer, String, DateTime, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import json

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    
    # Personal Information
    date_of_birth = Column(Date, nullable=True)
    phone_number = Column(String(20), nullable=True)
    
    # Education Information
    school_name = Column(String(200), nullable=True)
    grade_level = Column(String(50), nullable=True)  # e.g., "9th Grade", "College Freshman", "Graduate"
    major_field = Column(String(100), nullable=True)  # Major or field of study
    
    # Learning Preferences
    preferred_subjects = Column(Text, nullable=True)  # JSON string
    last_studied_topic = Column(String(255), nullable=True)
    learning_style = Column(String(50), nullable=True)
    study_goals = Column(Text, nullable=True)  # Student's learning goals
    
    # Additional Info
    bio = Column(Text, nullable=True)  # Short bio or description
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    study_sessions = relationship("StudySession", back_populates="student")
    quiz_attempts = relationship("QuizAttempt", back_populates="student")
    
    @property
    def subjects_list(self):
        """Get preferred subjects as a list"""
        if self.preferred_subjects:
            try:
                return json.loads(self.preferred_subjects)
            except json.JSONDecodeError:
                return []
        return []
    
    @subjects_list.setter
    def subjects_list(self, subjects):
        """Set preferred subjects from a list"""
        if subjects:
            self.preferred_subjects = json.dumps(subjects)
        else:
            self.preferred_subjects = None