from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.dependencies import get_current_student_id, get_current_user
from app.schemas.profile import (
    ProfileCreateRequest, ProfileUpdateRequest, ProfileResponse, 
    ProfileWithStats, ProfileError, LearningStyle
)
from app.services.profile_service import ProfileService
from app.models import Student, User
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["profile"])

# Initialize profile service
profile_service = ProfileService()

@router.post("/profile", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    request: ProfileCreateRequest,
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student_id)
):
    """
    Update the student profile for the authenticated user
    
    - **name**: Student's full name (required)
    - **email**: Student's email address (optional, must be unique)
    - **preferred_subjects**: List of preferred subjects (optional)
    - **learning_style**: Preferred learning style (optional)
    """
    try:
        # Get existing student profile
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        # Update student profile
        import json
        
        # Basic info
        student.name = request.name
        
        # Update email only if provided and different
        if request.email and request.email != student.email:
            # Check if email is already used by another student
            existing = db.query(Student).filter(
                Student.email == request.email,
                Student.id != student_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )
            student.email = request.email
        
        # Personal information
        if request.date_of_birth is not None:
            student.date_of_birth = request.date_of_birth
        if request.phone_number is not None:
            student.phone_number = request.phone_number
        
        # Education information
        if request.school_name is not None:
            student.school_name = request.school_name
        if request.grade_level is not None:
            student.grade_level = request.grade_level
        if request.major_field is not None:
            student.major_field = request.major_field
        
        # Learning preferences
        if request.preferred_subjects is not None:
            student.preferred_subjects = json.dumps(request.preferred_subjects) if request.preferred_subjects else None
        if request.learning_style is not None:
            student.learning_style = request.learning_style.value if hasattr(request.learning_style, 'value') else request.learning_style
        if request.study_goals is not None:
            student.study_goals = request.study_goals
        
        # Additional info
        if request.bio is not None:
            student.bio = request.bio
        
        student.updated_at = datetime.utcnow()
        
        try:
            db.commit()
            db.refresh(student)
        except Exception as commit_error:
            db.rollback()
            logger.error(f"Database commit error: {str(commit_error)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update profile: {str(commit_error)}"
            )
        
        # Convert to response format
        return ProfileResponse(
            id=student.id,
            name=student.name,
            email=student.email,
            preferred_subjects=student.subjects_list,
            learning_style=student.learning_style,
            last_studied_topic=student.last_studied_topic,
            created_at=student.created_at,
            updated_at=student.updated_at
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating profile: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create profile: {str(e)}"
        )

@router.get("/profile", response_model=ProfileResponse)
async def get_profile(
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student_id)
):
    """
    Get student profile by ID
    
    - **student_id**: Unique student identifier
    """
    try:
        student = profile_service.get_student_profile(db, student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        return ProfileResponse(
            id=student.id,
            name=student.name,
            email=student.email,
            preferred_subjects=student.subjects_list,
            learning_style=student.learning_style,
            last_studied_topic=student.last_studied_topic,
            created_at=student.created_at,
            updated_at=student.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get profile: {str(e)}"
        )

@router.put("/profile", response_model=ProfileResponse)
async def update_profile(
    request: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student_id)
):
    """
    Update student profile
    
    - **student_id**: Unique student identifier
    - **name**: Student's full name (optional)
    - **email**: Student's email address (optional)
    - **preferred_subjects**: List of preferred subjects (optional)
    - **learning_style**: Preferred learning style (optional)
    - **last_studied_topic**: Last studied topic (optional)
    """
    try:
        # Prepare updates
        updates = {}
        if request.name is not None:
            updates['name'] = request.name
        if request.email is not None:
            updates['email'] = request.email
        if request.preferred_subjects is not None:
            updates['preferred_subjects'] = request.preferred_subjects
        if request.learning_style is not None:
            # Handle both enum and string values
            updates['learning_style'] = request.learning_style.value if hasattr(request.learning_style, 'value') else request.learning_style
        if request.last_studied_topic is not None:
            updates['last_studied_topic'] = request.last_studied_topic
        
        # Update profile
        student = profile_service.update_student_profile(db, student_id, **updates)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        return ProfileResponse(
            id=student.id,
            name=student.name,
            email=student.email,
            preferred_subjects=student.subjects_list,
            learning_style=student.learning_style,
            last_studied_topic=student.last_studied_topic,
            created_at=student.created_at,
            updated_at=student.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile: {str(e)}"
        )

@router.delete("/profile", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student_id)
):
    """
    Delete student profile and all associated data
    
    - **student_id**: Unique student identifier
    """
    try:
        deleted = profile_service.delete_student_profile(db, student_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete profile: {str(e)}"
        )

@router.get("/profile/stats", response_model=ProfileWithStats)
async def get_profile_with_stats(
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student_id)
):
    """
    Get student profile with comprehensive learning statistics
    
    - **student_id**: Unique student identifier
    """
    try:
        # Get student profile
        student = profile_service.get_student_profile(db, student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        # Get statistics
        stats = profile_service.get_student_stats(db, student_id)
        
        return ProfileWithStats(
            id=student.id,
            name=student.name,
            email=student.email,
            preferred_subjects=student.subjects_list,
            learning_style=student.learning_style,
            last_studied_topic=student.last_studied_topic,
            created_at=student.created_at,
            updated_at=student.updated_at,
            stats=stats
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting profile with stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get profile with stats: {str(e)}"
        )

@router.get("/profiles", response_model=List[ProfileResponse])
async def list_profiles(
    skip: int = Query(0, ge=0, description="Number of profiles to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of profiles to return"),
    db: Session = Depends(get_db)
):
    """
    List all student profiles with pagination
    
    - **skip**: Number of profiles to skip (for pagination)
    - **limit**: Maximum number of profiles to return (1-100)
    """
    try:
        students = profile_service.get_all_students(db, skip=skip, limit=limit)
        
        return [
            ProfileResponse(
                id=student.id,
                name=student.name,
                email=student.email,
                preferred_subjects=student.subjects_list,
                learning_style=student.learning_style,
                last_studied_topic=student.last_studied_topic,
                created_at=student.created_at,
                updated_at=student.updated_at
            )
            for student in students
        ]
        
    except Exception as e:
        logger.error(f"Error listing profiles: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list profiles: {str(e)}"
        )

@router.get("/profiles/search", response_model=List[ProfileResponse])
async def search_profiles(
    q: str = Query(..., min_length=1, description="Search query (name or email)"),
    limit: int = Query(20, ge=1, le=50, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Search student profiles by name or email
    
    - **q**: Search query (searches in name and email fields)
    - **limit**: Maximum number of results to return (1-50)
    """
    try:
        students = profile_service.search_students(db, query=q, limit=limit)
        
        return [
            ProfileResponse(
                id=student.id,
                name=student.name,
                email=student.email,
                preferred_subjects=student.subjects_list,
                learning_style=student.learning_style,
                last_studied_topic=student.last_studied_topic,
                created_at=student.created_at,
                updated_at=student.updated_at
            )
            for student in students
        ]
        
    except Exception as e:
        logger.error(f"Error searching profiles: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search profiles: {str(e)}"
        )

@router.get("/profile/email/{email}", response_model=ProfileResponse)
async def get_profile_by_email(
    email: str,
    db: Session = Depends(get_db)
):
    """
    Get student profile by email address
    
    - **email**: Student's email address
    """
    try:
        student = profile_service.get_student_by_email(db, email)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        return ProfileResponse(
            id=student.id,
            name=student.name,
            email=student.email,
            preferred_subjects=student.subjects_list,
            learning_style=student.learning_style,
            last_studied_topic=student.last_studied_topic,
            created_at=student.created_at,
            updated_at=student.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting profile by email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get profile by email: {str(e)}"
        )

@router.get("/profile/learning-styles")
async def get_learning_styles():
    """
    Get available learning styles
    """
    return {
        "learning_styles": [
            {
                "value": "visual",
                "name": "Visual",
                "description": "Learn best through images, diagrams, and visual aids"
            },
            {
                "value": "auditory",
                "name": "Auditory",
                "description": "Learn best through listening and verbal instruction"
            },
            {
                "value": "kinesthetic",
                "name": "Kinesthetic",
                "description": "Learn best through hands-on activities and movement"
            },
            {
                "value": "reading_writing",
                "name": "Reading/Writing",
                "description": "Learn best through reading and writing activities"
            },
            {
                "value": "mixed",
                "name": "Mixed",
                "description": "Combination of multiple learning styles"
            }
        ]
    }