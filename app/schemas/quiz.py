from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum

class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"

class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=5000, description="Topic for quiz questions or full content")
    question_count: int = Field(default=5, ge=1, le=10, description="Number of questions to generate")
    difficulty: Difficulty = Field(default=Difficulty.MEDIUM, description="Difficulty level")
    question_types: List[QuestionType] = Field(
        default=[QuestionType.MULTIPLE_CHOICE, QuestionType.TRUE_FALSE], 
        description="Types of questions to include"
    )
    student_id: Optional[int] = Field(default=None, description="ID of the student taking the quiz")
    
    @validator('topic')
    def validate_topic(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Topic cannot be empty')
        return v.strip()
    
    @validator('question_types')
    def validate_question_types(cls, v):
        if not v:
            raise ValueError('At least one question type must be specified')
        return v

class QuizQuestion(BaseModel):
    id: str = Field(..., description="Unique identifier for the question")
    question: str = Field(..., description="The question text")
    type: QuestionType = Field(..., description="Type of question")
    options: Optional[List[str]] = Field(default=None, description="Answer options for multiple choice")
    correct_answer: str = Field(..., description="The correct answer")
    explanation: str = Field(..., description="Explanation of why the answer is correct")
    points: int = Field(default=1, description="Points awarded for correct answer")

class QuizResponse(BaseModel):
    quiz_id: str = Field(..., description="Unique identifier for the quiz")
    questions: List[QuizQuestion] = Field(..., description="List of quiz questions")
    topic: str = Field(..., description="Quiz topic")
    difficulty: str = Field(..., description="Quiz difficulty level")
    question_count: int = Field(..., description="Total number of questions")
    estimated_time: int = Field(..., description="Estimated time to complete in minutes")
    total_points: int = Field(..., description="Total points possible")

class QuizSubmission(BaseModel):
    quiz_id: str = Field(..., description="ID of the quiz being submitted")
    student_id: int = Field(..., description="ID of the student submitting")
    answers: Dict[str, str] = Field(..., description="Student's answers mapped by question ID")
    time_taken: Optional[int] = Field(default=None, description="Time taken in seconds")

class QuizResult(BaseModel):
    quiz_id: str = Field(..., description="ID of the completed quiz")
    student_id: int = Field(..., description="ID of the student")
    score: float = Field(..., ge=0.0, le=100.0, description="Score as percentage")
    correct_answers: int = Field(..., description="Number of correct answers")
    total_questions: int = Field(..., description="Total number of questions")
    time_taken: Optional[int] = Field(default=None, description="Time taken in seconds")
    feedback: List[Dict[str, Any]] = Field(..., description="Detailed feedback for each question")
    attempt_id: int = Field(..., description="Database ID of the quiz attempt")

class QuizError(BaseModel):
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[dict] = Field(default=None, description="Additional error details")