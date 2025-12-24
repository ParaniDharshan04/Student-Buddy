from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..schemas import UserStats
from ..models import User, Question, Quiz, QuizAttempt, Note, VoiceSession
from ..dependencies import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/stats", response_model=UserStats)
def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user statistics and analytics"""
    # Count totals
    total_questions = db.query(func.count(Question.id))\
        .filter(Question.user_id == current_user.id)\
        .scalar()
    
    total_quizzes = db.query(func.count(Quiz.id))\
        .filter(Quiz.user_id == current_user.id)\
        .scalar()
    
    total_quiz_attempts = db.query(func.count(QuizAttempt.id))\
        .filter(QuizAttempt.user_id == current_user.id)\
        .scalar()
    
    total_notes = db.query(func.count(Note.id))\
        .filter(Note.user_id == current_user.id)\
        .scalar()
    
    total_voice_sessions = db.query(func.count(VoiceSession.id))\
        .filter(VoiceSession.user_id == current_user.id)\
        .scalar()
    
    # Calculate average quiz score
    avg_score = db.query(func.avg(QuizAttempt.score))\
        .filter(QuizAttempt.user_id == current_user.id)\
        .scalar() or 0.0
    
    # Get recent activity
    recent_questions = db.query(Question)\
        .filter(Question.user_id == current_user.id)\
        .order_by(Question.created_at.desc())\
        .limit(5)\
        .all()
    
    recent_activity = []
    for q in recent_questions:
        recent_activity.append({
            "type": "question",
            "title": q.question_text[:50] + "..." if len(q.question_text) > 50 else q.question_text,
            "timestamp": q.created_at.isoformat()
        })
    
    return UserStats(
        total_questions=total_questions or 0,
        total_quizzes=total_quizzes or 0,
        total_quiz_attempts=total_quiz_attempts or 0,
        average_quiz_score=round(avg_score, 2),
        total_notes=total_notes or 0,
        total_voice_sessions=total_voice_sessions or 0,
        recent_activity=recent_activity
    )
