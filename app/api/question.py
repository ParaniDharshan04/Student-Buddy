from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_student_id
from app.schemas.question import QuestionRequest, QuestionResponse, QuestionError
from app.services.ai_service import AIService
from app.models import Student, StudySession
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["questions"])


def _get_ai_service():
    """Create AIService instance lazily and provide better error messages if not configured."""
    try:
        return AIService()
    except ValueError as e:
        # Convert configuration errors into HTTP-friendly exceptions at request time
        logger.error(f"AIService configuration error: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(
    request: QuestionRequest,
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student_id)
):
    """
    Answer a student's question with step-by-step explanation
    
    - **question**: The question to be answered
    - **explanation_style**: Style of explanation (simple, exam-style, real-world)
    - **student_id**: Optional student ID to track the session
    """
    try:
        # Validate input
        if not request.question.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question cannot be empty"
            )
        
        # Get AI response
        logger.info(f"Processing question: {request.question[:50]}...")
        try:
            ai_service = _get_ai_service()
            ai_response = await ai_service.answer_question(
                question=request.question,
                style=request.explanation_style.value
            )
        except HTTPException:
            # _get_ai_service() already logged and raised a HTTPException for missing config
            raise
        except Exception as e:
            logger.error(f"AIService error while answering question: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"AI provider error: {str(e)}"
            )
        
        # Create study session for authenticated user
        session_id = None
        try:
            # Verify student exists
            student = db.query(Student).filter(Student.id == student_id).first()
            if student:
                # Update student's last studied topic (extract from question)
                topic = _extract_topic_from_question(request.question)
                if topic:
                    student.last_studied_topic = topic
                    student.updated_at = datetime.utcnow()
                
                # Create study session
                study_session = StudySession(
                    student_id=student_id,
                    session_type="question",
                    topic=topic,
                    content=request.question,
                    ai_response=ai_response["answer"],
                    session_metadata=json.dumps({
                        "explanation_style": request.explanation_style.value,
                        "confidence_score": ai_response["confidence_score"],
                        "related_topics": ai_response["related_topics"]
                    })
                )
                
                db.add(study_session)
                db.commit()
                db.refresh(study_session)
                session_id = study_session.id
                
                logger.info(f"Created study session {session_id} for student {student_id}")
            else:
                logger.warning(f"Student {student_id} not found")
        except Exception as e:
            logger.error(f"Error creating study session: {str(e)}")
            # Don't fail the request if session creation fails
            db.rollback()
        
        # Return response
        return QuestionResponse(
            answer=ai_response["answer"],
            explanation_steps=ai_response["explanation_steps"],
            style=ai_response["style"],
            confidence_score=ai_response["confidence_score"],
            related_topics=ai_response["related_topics"],
            session_id=session_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process question: {str(e)}"
        )

@router.get("/ask/styles")
async def get_explanation_styles():
    """
    Get available explanation styles
    """
    return {
        "styles": [
            {
                "value": "simple",
                "name": "Simple",
                "description": "Clear, step-by-step explanation with simple language"
            },
            {
                "value": "exam-style", 
                "name": "Exam Style",
                "description": "Detailed explanation suitable for exam preparation"
            },
            {
                "value": "real-world",
                "name": "Real World",
                "description": "Explanation with real-world applications and examples"
            }
        ]
    }

def _extract_topic_from_question(question: str) -> str:
    """
    Extract a topic from the question text
    This is a simple implementation - could be enhanced with NLP
    """
    # Convert to lowercase for analysis
    question_lower = question.lower()
    
    # Common subject keywords
    subjects = {
        "math": ["math", "mathematics", "algebra", "calculus", "geometry", "trigonometry", "statistics"],
        "physics": ["physics", "force", "energy", "motion", "gravity", "electricity", "magnetism"],
        "chemistry": ["chemistry", "chemical", "reaction", "molecule", "atom", "compound", "element"],
        "biology": ["biology", "cell", "organism", "genetics", "evolution", "ecosystem", "photosynthesis"],
        "computer science": ["programming", "code", "algorithm", "software", "computer", "python", "javascript"],
        "history": ["history", "historical", "war", "ancient", "medieval", "revolution", "empire"],
        "literature": ["literature", "poem", "novel", "author", "writing", "story", "character"]
    }
    
    # Find matching subjects
    for subject, keywords in subjects.items():
        if any(keyword in question_lower for keyword in keywords):
            return subject.title()
    
    # If no specific subject found, try to extract the main noun
    words = question.split()
    if len(words) > 2:
        # Return first few words as topic
        return " ".join(words[:3]).title()
    
    return "General"