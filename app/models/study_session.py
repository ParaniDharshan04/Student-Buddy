from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import json

class StudySession(Base):
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    session_type = Column(String(20), nullable=False)  # question, quiz, notes
    topic = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)  # User input content
    ai_response = Column(Text, nullable=True)  # AI generated response
    session_metadata = Column(Text, nullable=True)  # JSON for additional data
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="study_sessions")
    
    @property
    def metadata_dict(self):
        """Get metadata as a dictionary"""
        if self.session_metadata:
            try:
                return json.loads(self.session_metadata)
            except json.JSONDecodeError:
                return {}
        return {}
    
    @metadata_dict.setter
    def metadata_dict(self, data):
        """Set metadata from a dictionary"""
        if data:
            self.session_metadata = json.dumps(data)
        else:
            self.session_metadata = None