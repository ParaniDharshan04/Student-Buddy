from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# Auth Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


# Student Profile Schemas
class StudentCreate(BaseModel):
    full_name: str
    education_level: Optional[str] = None
    grade: Optional[str] = None
    subjects: Optional[List[str]] = []
    learning_style: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = {}


class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    education_level: Optional[str] = None
    grade: Optional[str] = None
    subjects: Optional[List[str]] = None
    learning_style: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class StudentResponse(BaseModel):
    id: int
    user_id: int
    full_name: Optional[str]
    education_level: Optional[str]
    grade: Optional[str]
    subjects: Optional[List[str]]
    learning_style: Optional[str]
    preferences: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Question Schemas
class QuestionAsk(BaseModel):
    question: str = Field(..., min_length=5)
    explanation_type: str = Field(default="simple", pattern="^(simple|exam|real_world)$")


class QuestionResponse(BaseModel):
    id: int
    question_text: str
    answer_text: str
    explanation_type: str
    topics: Optional[List[str]]
    concepts: Optional[List[str]]
    confidence_score: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Quiz Schemas
class QuizGenerate(BaseModel):
    topic: Optional[str] = None
    text_content: Optional[str] = None
    difficulty: str = Field(default="medium", pattern="^(easy|medium|hard)$")
    question_count: int = Field(default=5, ge=1, le=20)
    question_types: Optional[List[str]] = ["mcq", "true_false"]


class QuizQuestion(BaseModel):
    id: int
    type: str
    question: str
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    id: int
    title: str
    topic: str
    difficulty: str
    question_count: int
    questions: List[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True


class QuizAttemptSubmit(BaseModel):
    quiz_id: int
    answers: List[Dict[str, Any]]
    time_taken: Optional[int] = None


class QuizAttemptResponse(BaseModel):
    id: int
    quiz_id: int
    score: float
    total_questions: int
    answers: List[Dict[str, Any]]
    time_taken: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Note Schemas
class NoteCreate(BaseModel):
    title: str
    text_content: str = Field(..., min_length=50)
    format: str = Field(default="bullet_points", pattern="^(bullet_points|paragraph|outline|key_concepts)$")


class NoteResponse(BaseModel):
    id: int
    title: str
    original_text: str
    summary_text: str
    format: str
    key_terms: Optional[List[str]]
    original_length: int
    summary_length: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Voice Session Schemas
class VoiceMessage(BaseModel):
    content: str
    mode: str = Field(..., pattern="^(casual|interview|presentation)$")


class VoiceSessionCreate(BaseModel):
    mode: str = Field(..., pattern="^(casual|interview|presentation)$")


class VoiceSessionResponse(BaseModel):
    id: int
    mode: str
    duration: Optional[int]
    messages: List[Dict[str, Any]]
    feedback: Optional[Dict[str, Any]]
    created_at: datetime
    ended_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Analytics Schemas
class UserStats(BaseModel):
    total_questions: int
    total_quizzes: int
    total_quiz_attempts: int
    average_quiz_score: float
    total_notes: int
    total_voice_sessions: int
    recent_activity: List[Dict[str, Any]]
