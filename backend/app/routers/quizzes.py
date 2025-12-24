from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..schemas import QuizGenerate, QuizResponse, QuizAttemptSubmit, QuizAttemptResponse
from ..models import User, Quiz, QuizAttempt
from ..dependencies import get_current_user
from ..services.ai_service import ai_service
from ..services.file_service import file_service

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


@router.post("/generate", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
async def generate_quiz(
    topic: Optional[str] = Form(None),
    difficulty: str = Form("medium"),
    question_count: int = Form(5),
    file: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a quiz from topic or uploaded file"""
    try:
        # Determine source text
        if file:
            text_content = await file_service.extract_text_from_file(file)
            quiz_topic = f"Quiz from {file.filename}"
        elif topic:
            text_content = topic
            quiz_topic = topic
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either topic or file must be provided"
            )
        
        # Generate quiz using AI
        ai_response = ai_service.generate_quiz(
            text_content,
            difficulty,
            question_count,
            ["mcq", "true_false"]
        )
        
        # Save to database
        db_quiz = Quiz(
            user_id=current_user.id,
            title=ai_response.get("title", quiz_topic),
            topic=quiz_topic,
            difficulty=difficulty,
            question_count=len(ai_response.get("questions", [])),
            questions=ai_response.get("questions", [])
        )
        
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)
        
        return db_quiz
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating quiz: {str(e)}"
        )


@router.get("/", response_model=List[QuizResponse])
def get_quizzes(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's quizzes"""
    quizzes = db.query(Quiz)\
        .filter(Quiz.user_id == current_user.id)\
        .order_by(Quiz.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return quizzes


@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(
    quiz_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific quiz by ID"""
    quiz = db.query(Quiz)\
        .filter(Quiz.id == quiz_id, Quiz.user_id == current_user.id)\
        .first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    return quiz


@router.post("/attempts", response_model=QuizAttemptResponse, status_code=status.HTTP_201_CREATED)
def submit_quiz_attempt(
    attempt_data: QuizAttemptSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit quiz attempt and get results"""
    # Verify quiz exists and belongs to user
    quiz = db.query(Quiz)\
        .filter(Quiz.id == attempt_data.quiz_id, Quiz.user_id == current_user.id)\
        .first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Grade the quiz
    correct_count = 0
    graded_answers = []
    
    for user_answer in attempt_data.answers:
        question_id = user_answer.get("question_id")
        user_ans = user_answer.get("answer")
        
        # Find correct answer
        correct_answer = None
        explanation = ""
        for q in quiz.questions:
            if q.get("id") == question_id:
                correct_answer = q.get("correct_answer")
                explanation = q.get("explanation", "")
                break
        
        is_correct = user_ans == correct_answer
        if is_correct:
            correct_count += 1
        
        graded_answers.append({
            "question_id": question_id,
            "user_answer": user_ans,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "explanation": explanation
        })
    
    # Calculate score
    total_questions = len(attempt_data.answers)
    score = (correct_count / total_questions * 100) if total_questions > 0 else 0
    
    # Save attempt
    db_attempt = QuizAttempt(
        quiz_id=attempt_data.quiz_id,
        user_id=current_user.id,
        score=score,
        total_questions=total_questions,
        answers=graded_answers,
        time_taken=attempt_data.time_taken
    )
    
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)
    
    return db_attempt


@router.get("/attempts/history", response_model=List[QuizAttemptResponse])
def get_quiz_attempts(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's quiz attempt history"""
    attempts = db.query(QuizAttempt)\
        .filter(QuizAttempt.user_id == current_user.id)\
        .order_by(QuizAttempt.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return attempts
