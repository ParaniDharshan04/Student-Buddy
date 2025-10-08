from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime

class SignupRequest(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    password: str = Field(..., min_length=6, max_length=100, description="Password")
    full_name: str = Field(..., min_length=1, max_length=100, description="Full name")
    
    @validator('username')
    def validate_username(cls, v):
        if not v.isalnum() and '_' not in v:
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return v.lower()
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v

class LoginRequest(BaseModel):
    email: str = Field(..., description="Email or username")
    password: str = Field(..., description="Password")

class AuthResponse(BaseModel):
    user_id: int
    email: str
    username: str
    full_name: str
    student_id: Optional[int]
    token: str
    message: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    student_id: Optional[int]
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
