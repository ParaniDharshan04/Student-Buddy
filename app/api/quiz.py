from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_student_id
from app.schemas.quiz import (
    QuizRequest, QuizResponse, QuizSubmission, QuizResult, 
    QuizError, QuestionType, Difficulty
)
from app.services.quiz_service import QuizService
from app.models import Student, QuizAttempt
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["quiz"])

# Initialize quiz service
quiz_service = QuizService()

@router.post("/quiz", response_model=QuizResponse)
async def generate_quiz(
    request: QuizRequest,
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student_id)
):
    """
    Generate a quiz on a specific topic
    
    - **topic**: The topic for quiz questions
    - **question_count**: Number of questions (1-10)
    - **difficulty**: Difficulty level (easy, medium, hard)
    - **question_types**: Types of questions to include
    - **student_id**: Optional student ID for tracking
    """
    try:
        # Validate input
        if not request.topic.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Topic cannot be empty"
            )
        
        # Generate quiz using quiz service
        logger.info(f"Generating quiz on topic: {request.topic}")
        quiz_data = await quiz_service.generate_quiz(
            topic=request.topic,
            question_count=request.question_count,
            difficulty=request.difficulty.value,
            question_types=[qt.value for qt in request.question_types]
        )
        
        # Update student's last studied topic
        try:
            student = db.query(Student).filter(Student.id == student_id).first()
            if student:
                student.last_studied_topic = request.topic
                student.updated_at = datetime.utcnow()
                db.commit()
                logger.info(f"Updated last studied topic for student {student_id}")
        except Exception as e:
            logger.error(f"Error updating student topic: {str(e)}")
            db.rollback()
        
        return QuizResponse(**quiz_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating quiz: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate quiz: {str(e)}"
        )

@router.post("/quiz/submit", response_model=QuizResult)
async def submit_quiz(
    submission: QuizSubmission,
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student_id)
):
    """
    Submit quiz answers and get results with feedback
    
    - **quiz_id**: ID of the quiz being submitted
    - **student_id**: ID of the student submitting
    - **answers**: Student's answers mapped by question ID
    - **time_taken**: Optional time taken in seconds
    """
    try:
        # Verify student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        # For this MVP, we'll need to retrieve the quiz questions
        # In a production system, you'd store quiz data temporarily or in cache
        # For now, we'll create a simple scoring system
        
        # Create a basic quiz attempt record
        quiz_attempt = QuizAttempt(
            student_id=student_id,
            quiz_data=json.dumps({
                "quiz_id": submission.quiz_id,
                "submitted_at": datetime.utcnow().isoformat()
            }),
            student_answers=json.dumps(submission.answers),
            time_taken=submission.time_taken,
            score=0.0  # Will be updated after scoring
        )
        
        db.add(quiz_attempt)
        db.commit()
        db.refresh(quiz_attempt)
        
        # For MVP, return a basic result
        # In production, you'd calculate actual score based on stored questions
        total_questions = len(submission.answers)
        correct_answers = max(1, int(total_questions * 0.7))  # Simulate 70% correct
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        # Update the quiz attempt with calculated score
        quiz_attempt.score = score
        db.commit()
        
        # Generate basic feedback
        feedback = []
        for i, (question_id, answer) in enumerate(submission.answers.items()):
            feedback.append({
                "question_id": question_id,
                "question": f"Question {i+1}",
                "student_answer": answer,
                "correct_answer": "Sample correct answer",
                "is_correct": i < correct_answers,  # First N answers are "correct"
                "explanation": "This is a sample explanation for the answer.",
                "points_earned": 1 if i < correct_answers else 0,
                "points_possible": 1
            })
        
        return QuizResult(
            quiz_id=submission.quiz_id,
            student_id=student_id,
            score=round(score, 2),
            correct_answers=correct_answers,
            total_questions=total_questions,
            time_taken=submission.time_taken,
            feedback=feedback,
            attempt_id=quiz_attempt.id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting quiz: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit quiz: {str(e)}"
        )

@router.get("/quiz/history")
async def get_quiz_history(
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student_id),
    limit: int = 10
):
    """
    Get quiz history for a student
    
    - **student_id**: ID of the student
    - **limit**: Maximum number of attempts to return
    """
    try:
        # Verify student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        # Get quiz attempts
        attempts = db.query(QuizAttempt)\
            .filter(QuizAttempt.student_id == student_id)\
            .order_by(QuizAttempt.completed_at.desc())\
            .limit(limit)\
            .all()
        
        history = []
        for attempt in attempts:
            quiz_data = attempt.quiz_questions if hasattr(attempt, 'quiz_questions') else {}
            answers = attempt.answers_dict if hasattr(attempt, 'answers_dict') else {}
            
            history.append({
                "attempt_id": attempt.id,
                "quiz_id": quiz_data.get("quiz_id", "unknown"),
                "score": float(attempt.score) if attempt.score else 0.0,
                "completed_at": attempt.completed_at.isoformat() if attempt.completed_at else None,
                "time_taken": attempt.time_taken,
                "question_count": len(answers)
            })
        
        return {
            "student_id": student_id,
            "student_name": student.name,
            "total_attempts": len(history),
            "attempts": history
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting quiz history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get quiz history: {str(e)}"
        )

@router.get("/quiz/types")
async def get_question_types():
    """Get available question types and difficulties"""
    return {
        "question_types": [
            {
                "value": "multiple_choice",
                "name": "Multiple Choice",
                "description": "Questions with multiple answer options"
            },
            {
                "value": "true_false",
                "name": "True/False",
                "description": "Questions with true or false answers"
            },
            {
                "value": "short_answer",
                "name": "Short Answer",
                "description": "Questions requiring brief written responses"
            }
        ],
        "difficulties": [
            {
                "value": "easy",
                "name": "Easy",
                "description": "Basic level questions"
            },
            {
                "value": "medium",
                "name": "Medium", 
                "description": "Intermediate level questions"
            },
            {
                "value": "hard",
                "name": "Hard",
                "description": "Advanced level questions"
            }
        ]
    }