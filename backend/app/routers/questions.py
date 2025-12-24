from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import QuestionAsk, QuestionResponse
from ..models import User, Question
from ..dependencies import get_current_user
from ..services.ai_service import ai_service

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/ask", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def ask_question(
    question_data: QuestionAsk,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Ask a question and get AI-powered answer"""
    try:
        # Get AI response
        ai_response = ai_service.answer_question(
            question_data.question,
            question_data.explanation_type
        )
        
        # Save to database
        db_question = Question(
            user_id=current_user.id,
            question_text=question_data.question,
            answer_text=ai_response.get("answer", ""),
            explanation_type=question_data.explanation_type,
            topics=ai_response.get("topics", []),
            concepts=ai_response.get("concepts", []),
            confidence_score=ai_response.get("confidence_score", 0.8)
        )
        
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        
        return db_question
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )


@router.get("/history", response_model=List[QuestionResponse])
def get_question_history(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's question history"""
    questions = db.query(Question)\
        .filter(Question.user_id == current_user.id)\
        .order_by(Question.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return questions


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific question by ID"""
    question = db.query(Question)\
        .filter(Question.id == question_id, Question.user_id == current_user.id)\
        .first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    return question
