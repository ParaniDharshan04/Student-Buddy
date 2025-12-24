from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import StudentCreate, StudentUpdate, StudentResponse
from ..models import User, Student
from ..dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/", response_model=StudentResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile"""
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return student


@router.put("/", response_model=StudentResponse)
def update_profile(
    profile_data: StudentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Update fields
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    
    db.commit()
    db.refresh(student)
    
    return student


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    profile_data: StudentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create or update user profile"""
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    
    if student:
        # Update existing profile
        update_data = profile_data.model_dump()
        for field, value in update_data.items():
            setattr(student, field, value)
    else:
        # Create new profile
        student = Student(user_id=current_user.id, **profile_data.model_dump())
        db.add(student)
    
    db.commit()
    db.refresh(student)
    
    return student
