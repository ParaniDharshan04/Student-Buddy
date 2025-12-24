from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..schemas import NoteCreate, NoteResponse
from ..models import User, Note
from ..dependencies import get_current_user
from ..services.ai_service import ai_service
from ..services.file_service import file_service

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/summarize", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_summary(
    title: str = Form(...),
    format: str = Form("bullet_points"),
    text_content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create note summary from text or file"""
    try:
        # Get text content
        if file:
            original_text = await file_service.extract_text_from_file(file)
        elif text_content:
            original_text = text_content
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either text_content or file must be provided"
            )
        
        # Generate summary
        ai_response = ai_service.summarize_text(original_text, format)
        summary_text = ai_response.get("summary", "")
        key_terms = ai_response.get("key_terms", [])
        
        # Save to database
        db_note = Note(
            user_id=current_user.id,
            title=title,
            original_text=original_text,
            summary_text=summary_text,
            format=format,
            key_terms=key_terms,
            original_length=len(original_text),
            summary_length=len(summary_text)
        )
        
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        
        return db_note
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating summary: {str(e)}"
        )


@router.get("/", response_model=List[NoteResponse])
def get_notes(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's notes"""
    notes = db.query(Note)\
        .filter(Note.user_id == current_user.id)\
        .order_by(Note.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return notes


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific note by ID"""
    note = db.query(Note)\
        .filter(Note.id == note_id, Note.user_id == current_user.id)\
        .first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    return note
