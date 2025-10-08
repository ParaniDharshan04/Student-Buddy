from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import json

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    quiz_data = Column(Text, nullable=False)  # JSON quiz questions
    student_answers = Column(Text, nullable=True)  # JSON student responses
    score = Column(DECIMAL(5, 2), nullable=True)  # Score as percentage
    time_taken = Column(Integer, nullable=True)  # Time in seconds
    completed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="quiz_attempts")
    
    @property
    def quiz_questions(self):
        """Get quiz questions as a list"""
        if self.quiz_data:
            try:
                return json.loads(self.quiz_data)
            except json.JSONDecodeError:
                return []
        return []
    
    @quiz_questions.setter
    def quiz_questions(self, questions):
        """Set quiz questions from a list"""
        if questions:
            self.quiz_data = json.dumps(questions)
        else:
            self.quiz_data = None
    
    @property
    def answers_dict(self):
        """Get student answers as a dictionary"""
        if self.student_answers:
            try:
                return json.loads(self.student_answers)
            except json.JSONDecodeError:
                return {}
        return {}
    
    @answers_dict.setter
    def answers_dict(self, answers):
        """Set student answers from a dictionary"""
        if answers:
            self.student_answers = json.dumps(answers)
        else:
            self.student_answers = None