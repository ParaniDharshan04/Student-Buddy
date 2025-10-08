from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_student_id
from app.schemas.voice_chat import VoiceChatRequest, VoiceChatResponse
from app.services.voice_chat_service import VoiceChatService
from app.models import Student, StudySession
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["voice-chat"])

voice_chat_service = VoiceChatService()

@router.post("/voice-chat", response_model=VoiceChatResponse)
async def voice_chat(
    request: VoiceChatRequest,
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student_id)
):
    """
    Voice chat with AI for communication practice
    
    - **message**: User's spoken message
    - **conversation_mode**: Type of practice (practice, interview, presentation)
    - **conversation_history**: Previous messages for context
    """
    try:
        # Validate input
        if not request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message cannot be empty"
            )
        
        # Get AI response
        logger.info(f"Voice chat request from student {student_id}: {request.message[:50]}...")
        
        ai_response = await voice_chat_service.get_response(
            message=request.message,
            conversation_mode=request.conversation_mode,
            conversation_history=request.conversation_history
        )
        
        # Save conversation session
        try:
            student = db.query(Student).filter(Student.id == student_id).first()
            if student:
                study_session = StudySession(
                    student_id=student_id,
                    session_type="voice_chat",
                    topic=f"Voice Chat - {request.conversation_mode}",
                    content=request.message,
                    ai_response=ai_response["response"],
                    session_metadata=json.dumps({
                        "conversation_mode": request.conversation_mode,
                        "message_count": len(request.conversation_history) + 1,
                        "feedback": ai_response.get("feedback", {})
                    })
                )
                
                db.add(study_session)
                db.commit()
                db.refresh(study_session)
                
                logger.info(f"Saved voice chat session {study_session.id}")
        except Exception as e:
            logger.error(f"Error saving voice chat session: {str(e)}")
            db.rollback()
        
        return VoiceChatResponse(
            response=ai_response["response"],
            feedback=ai_response.get("feedback"),
            suggestions=ai_response.get("suggestions", [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in voice chat: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process voice chat: {str(e)}"
        )

@router.get("/voice-chat/history")
async def get_voice_chat_history(
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student_id),
    limit: int = 20
):
    """Get voice chat history for the student"""
    try:
        sessions = db.query(StudySession)\
            .filter(StudySession.student_id == student_id)\
            .filter(StudySession.session_type == "voice_chat")\
            .order_by(StudySession.created_at.desc())\
            .limit(limit)\
            .all()
        
        history = []
        for session in sessions:
            metadata = session.metadata_dict if hasattr(session, 'metadata_dict') else {}
            
            history.append({
                "session_id": session.id,
                "topic": session.topic,
                "user_message": session.content,
                "ai_response": session.ai_response,
                "conversation_mode": metadata.get("conversation_mode", "practice"),
                "created_at": session.created_at.isoformat() if session.created_at else None
            })
        
        return {
            "student_id": student_id,
            "total_sessions": len(history),
            "sessions": history
        }
        
    except Exception as e:
        logger.error(f"Error getting voice chat history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get voice chat history"
        )
