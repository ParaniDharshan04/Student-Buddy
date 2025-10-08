from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_student_id
from app.schemas.notes import NotesRequest, NotesResponse, NotesError, SummaryFormat
from app.services.notes_service import NotesService
from app.models import Student, StudySession
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["notes"])

# Initialize notes service
notes_service = NotesService()

@router.post("/notes", response_model=NotesResponse)
async def summarize_notes(
    request: NotesRequest,
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student_id)
):
    """
    Summarize text content into structured notes
    
    - **content**: Text content to summarize (10-10000 characters)
    - **format**: Format for the summary (bullet_points, paragraph, outline, key_concepts)
    - **max_length**: Optional maximum length of summary in characters
    - **student_id**: Optional student ID for tracking
    - **topic**: Optional topic/subject for context
    """
    try:
        # Validate input
        if not request.content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Content cannot be empty"
            )
        
        if len(request.content) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Content must be at least 10 characters long"
            )
        
        # Generate summary using notes service
        logger.info(f"Summarizing content of length {len(request.content)}")
        summary_data = await notes_service.summarize_content(
            content=request.content,
            format_type=request.format.value,
            max_length=request.max_length,
            topic=request.topic
        )
        
        # Create study session for authenticated user
        session_id = None
        try:
            # Verify student exists
            student = db.query(Student).filter(Student.id == student_id).first()
            if student:
                # Update student's last studied topic if topic provided
                if request.topic:
                    student.last_studied_topic = request.topic
                    student.updated_at = datetime.utcnow()
                
                # Create study session
                study_session = StudySession(
                    student_id=student_id,
                    session_type="notes",
                    topic=request.topic or _extract_topic_from_content(request.content),
                    content=request.content[:1000],  # Store first 1000 chars
                    ai_response=summary_data["summary"],
                    session_metadata=json.dumps({
                        "format": request.format.value,
                        "original_length": summary_data["original_length"],
                        "summary_length": summary_data["summary_length"],
                        "compression_ratio": summary_data["compression_ratio"],
                        "key_terms": summary_data["key_terms"],
                        "main_topics": summary_data["main_topics"]
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
        return NotesResponse(
            summary=summary_data["summary"],
            format=summary_data["format"],
            original_length=summary_data["original_length"],
            summary_length=summary_data["summary_length"],
            compression_ratio=summary_data["compression_ratio"],
            key_terms=summary_data["key_terms"],
            main_topics=summary_data["main_topics"],
            reading_time=summary_data["reading_time"],
            session_id=session_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error summarizing notes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to summarize content: {str(e)}"
        )

@router.get("/notes/formats")
async def get_summary_formats():
    """
    Get available summary formats
    """
    return {
        "formats": [
            {
                "value": "bullet_points",
                "name": "Bullet Points",
                "description": "Organized bullet points with key information"
            },
            {
                "value": "paragraph",
                "name": "Paragraph",
                "description": "Coherent paragraphs with flowing narrative"
            },
            {
                "value": "outline",
                "name": "Outline",
                "description": "Hierarchical outline with numbered sections"
            },
            {
                "value": "key_concepts",
                "name": "Key Concepts",
                "description": "Important concepts with explanations"
            }
        ]
    }

@router.get("/notes/history")
async def get_notes_history(
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student_id),
    limit: int = 10
):
    """
    Get notes summarization history for a student
    
    - **student_id**: ID of the student
    - **limit**: Maximum number of sessions to return
    """
    try:
        # Verify student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        # Get notes sessions
        sessions = db.query(StudySession)\
            .filter(StudySession.student_id == student_id)\
            .filter(StudySession.session_type == "notes")\
            .order_by(StudySession.created_at.desc())\
            .limit(limit)\
            .all()
        
        history = []
        for session in sessions:
            metadata = session.metadata_dict if hasattr(session, 'metadata_dict') else {}
            
            history.append({
                "session_id": session.id,
                "topic": session.topic,
                "created_at": session.created_at.isoformat() if session.created_at else None,
                "format": metadata.get("format", "unknown"),
                "original_length": metadata.get("original_length", 0),
                "summary_length": metadata.get("summary_length", 0),
                "compression_ratio": metadata.get("compression_ratio", 0),
                "key_terms": metadata.get("key_terms", []),
                "main_topics": metadata.get("main_topics", [])
            })
        
        return {
            "student_id": student_id,
            "student_name": student.name,
            "total_sessions": len(history),
            "sessions": history
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting notes history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get notes history: {str(e)}"
        )

@router.get("/notes/session/{session_id}")
async def get_notes_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Get details of a specific notes session
    
    - **session_id**: ID of the notes session
    """
    try:
        # Get session
        session = db.query(StudySession)\
            .filter(StudySession.id == session_id)\
            .filter(StudySession.session_type == "notes")\
            .first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notes session not found"
            )
        
        metadata = session.metadata_dict if hasattr(session, 'metadata_dict') else {}
        
        return {
            "session_id": session.id,
            "student_id": session.student_id,
            "topic": session.topic,
            "created_at": session.created_at.isoformat() if session.created_at else None,
            "original_content": session.content,
            "summary": session.ai_response,
            "format": metadata.get("format", "unknown"),
            "original_length": metadata.get("original_length", 0),
            "summary_length": metadata.get("summary_length", 0),
            "compression_ratio": metadata.get("compression_ratio", 0),
            "key_terms": metadata.get("key_terms", []),
            "main_topics": metadata.get("main_topics", [])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting notes session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get notes session: {str(e)}"
        )

def _extract_topic_from_content(content: str) -> str:
    """
    Extract a topic from the content text
    This is a simple implementation - could be enhanced with NLP
    """
    # Take first few words as topic
    words = content.split()[:5]
    topic = " ".join(words)
    
    # Clean up and limit length
    topic = topic.replace('\n', ' ').strip()
    if len(topic) > 50:
        topic = topic[:47] + "..."
    
    return topic or "General Notes"