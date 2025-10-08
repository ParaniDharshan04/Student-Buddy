from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum

class ExplanationStyle(str, Enum):
    SIMPLE = "simple"
    EXAM_STYLE = "exam-style"
    REAL_WORLD = "real-world"

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000, description="The student's question")
    explanation_style: ExplanationStyle = Field(default=ExplanationStyle.SIMPLE, description="Style of explanation")
    student_id: Optional[int] = Field(default=None, description="ID of the student asking the question")
    
    @validator('question')
    def validate_question(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Question cannot be empty')
        return v.strip()

class QuestionResponse(BaseModel):
    answer: str = Field(..., description="The complete answer to the question")
    explanation_steps: List[str] = Field(..., description="Step-by-step breakdown of the explanation")
    style: str = Field(..., description="The explanation style used")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the answer")
    related_topics: List[str] = Field(default=[], description="Related topics for further study")
    session_id: Optional[int] = Field(default=None, description="ID of the created study session")

class QuestionError(BaseModel):
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[dict] = Field(default=None, description="Additional error details")