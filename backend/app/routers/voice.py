from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from ..schemas import VoiceMessage, VoiceSessionCreate, VoiceSessionResponse
from ..models import User, VoiceSession
from ..dependencies import get_current_user
from ..services.ai_service import ai_service

router = APIRouter(prefix="/voice", tags=["Voice"])


@router.post("/sessions", response_model=VoiceSessionResponse, status_code=status.HTTP_201_CREATED)
def create_voice_session(
    session_data: VoiceSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new voice session"""
    db_session = VoiceSession(
        user_id=current_user.id,
        mode=session_data.mode,
        messages=[],
        feedback={}
    )
    
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return db_session


@router.post("/sessions/{session_id}/message", response_model=dict)
def send_voice_message(
    session_id: int,
    message_data: VoiceMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send message in voice session and get AI response"""
    # Get session
    session = db.query(VoiceSession)\
        .filter(VoiceSession.id == session_id, VoiceSession.user_id == current_user.id)\
        .first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voice session not found"
        )
    
    try:
        # Add user message to history
        user_message = {
            "role": "user",
            "content": message_data.content,
            "timestamp": datetime.utcnow().isoformat()
        }
        session.messages.append(user_message)
        
        # Get AI response
        ai_response = ai_service.voice_conversation(
            message_data.content,
            message_data.mode,
            session.messages
        )
        
        # Add AI response to history
        ai_message = {
            "role": "assistant",
            "content": ai_response.get("response", ""),
            "timestamp": datetime.utcnow().isoformat()
        }
        session.messages.append(ai_message)
        
        # Update feedback
        if ai_response.get("feedback"):
            session.feedback = ai_response.get("feedback")
        
        db.commit()
        db.refresh(session)
        
        return {
            "response": ai_response.get("response", ""),
            "feedback": ai_response.get("feedback", {})
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )


@router.put("/sessions/{session_id}/end", response_model=VoiceSessionResponse)
def end_voice_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """End voice session"""
    session = db.query(VoiceSession)\
        .filter(VoiceSession.id == session_id, VoiceSession.user_id == current_user.id)\
        .first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voice session not found"
        )
    
    session.ended_at = datetime.utcnow()
    if session.created_at:
        duration = (session.ended_at - session.created_at).total_seconds()
        session.duration = int(duration)
    
    db.commit()
    db.refresh(session)
    
    return session


@router.get("/sessions", response_model=List[VoiceSessionResponse])
def get_voice_sessions(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's voice sessions"""
    sessions = db.query(VoiceSession)\
        .filter(VoiceSession.user_id == current_user.id)\
        .order_by(VoiceSession.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return sessions


@router.get("/sessions/{session_id}", response_model=VoiceSessionResponse)
def get_voice_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific voice session"""
    session = db.query(VoiceSession)\
        .filter(VoiceSession.id == session_id, VoiceSession.user_id == current_user.id)\
        .first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voice session not found"
        )
    
    return session
