"""
Dependencies for FastAPI endpoints
"""
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import User
import logging

logger = logging.getLogger(__name__)

# Simple in-memory token storage (matches auth_service)
# In production, use Redis or database
active_tokens = {}

def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from token
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Extract token from "Bearer <token>" format
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )
    except ValueError:
        # If no space, assume the whole string is the token
        token = authorization
    
    # Verify token (this should match the auth_service token storage)
    from app.services.auth_service import AuthService
    auth_service = AuthService()
    user_id = auth_service.verify_token(token)
    
    if not user_id:
        logger.warning(f"Invalid token attempted: {token[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    logger.debug(f"Token verified for user_id: {user_id}")
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user

def get_current_student_id(
    current_user: User = Depends(get_current_user)
) -> int:
    """
    Get the student_id for the current authenticated user
    """
    if not current_user.student_id:
        logger.error(f"User {current_user.id} ({current_user.username}) has no student_id")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have an associated student profile. Please contact support."
        )
    
    logger.debug(f"User {current_user.username} has student_id: {current_user.student_id}")
    return current_user.student_id
