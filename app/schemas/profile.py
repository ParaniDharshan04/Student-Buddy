from pydantic import BaseModel, Field, validator, EmailStr
from typing import List, Optional
from datetime import datetime, date
from enum import Enum

class LearningStyle(str, Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING_WRITING = "reading_writing"
    MIXED = "mixed"

class GradeLevel(str, Enum):
    ELEMENTARY = "Elementary School"
    MIDDLE_6 = "6th Grade"
    MIDDLE_7 = "7th Grade"
    MIDDLE_8 = "8th Grade"
    HIGH_9 = "9th Grade"
    HIGH_10 = "10th Grade"
    HIGH_11 = "11th Grade"
    HIGH_12 = "12th Grade"
    COLLEGE_FRESHMAN = "College Freshman"
    COLLEGE_SOPHOMORE = "College Sophomore"
    COLLEGE_JUNIOR = "College Junior"
    COLLEGE_SENIOR = "College Senior"
    GRADUATE = "Graduate Student"
    OTHER = "Other"

class ProfileCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Student's full name")
    email: Optional[EmailStr] = Field(default=None, description="Student's email address")
    
    # Personal Information
    date_of_birth: Optional[date] = Field(default=None, description="Date of birth")
    phone_number: Optional[str] = Field(default=None, max_length=20, description="Phone number")
    
    # Education Information
    school_name: Optional[str] = Field(default=None, max_length=200, description="School or college name")
    grade_level: Optional[str] = Field(default=None, description="Current grade level")
    major_field: Optional[str] = Field(default=None, max_length=100, description="Major or field of study")
    
    # Learning Preferences
    preferred_subjects: List[str] = Field(default=[], description="List of preferred subjects")
    learning_style: Optional[LearningStyle] = Field(default=None, description="Preferred learning style")
    study_goals: Optional[str] = Field(default=None, description="Learning goals")
    
    # Additional Info
    bio: Optional[str] = Field(default=None, max_length=500, description="Short bio")
    
    @validator('name')
    def validate_name(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    @validator('preferred_subjects')
    def validate_subjects(cls, v):
        if v:
            # Clean and validate subjects
            cleaned_subjects = []
            for subject in v:
                if isinstance(subject, str) and subject.strip():
                    cleaned_subjects.append(subject.strip().title())
            return cleaned_subjects[:10]  # Limit to 10 subjects
        return []

class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100, description="Student's full name")
    email: Optional[EmailStr] = Field(default=None, description="Student's email address")
    
    # Personal Information
    date_of_birth: Optional[date] = Field(default=None, description="Date of birth")
    phone_number: Optional[str] = Field(default=None, max_length=20, description="Phone number")
    
    # Education Information
    school_name: Optional[str] = Field(default=None, max_length=200, description="School or college name")
    grade_level: Optional[str] = Field(default=None, description="Current grade level")
    major_field: Optional[str] = Field(default=None, max_length=100, description="Major or field of study")
    
    # Learning Preferences
    preferred_subjects: Optional[List[str]] = Field(default=None, description="List of preferred subjects")
    learning_style: Optional[LearningStyle] = Field(default=None, description="Preferred learning style")
    study_goals: Optional[str] = Field(default=None, description="Learning goals")
    last_studied_topic: Optional[str] = Field(default=None, max_length=255, description="Last studied topic")
    
    # Additional Info
    bio: Optional[str] = Field(default=None, max_length=500, description="Short bio")
    
    @validator('name')
    def validate_name(cls, v):
        if v is not None:
            if not v or v.strip() == "":
                raise ValueError('Name cannot be empty')
            return v.strip()
        return v
    
    @validator('preferred_subjects')
    def validate_subjects(cls, v):
        if v is not None:
            # Clean and validate subjects
            cleaned_subjects = []
            for subject in v:
                if isinstance(subject, str) and subject.strip():
                    cleaned_subjects.append(subject.strip().title())
            return cleaned_subjects[:10]  # Limit to 10 subjects
        return v

class ProfileResponse(BaseModel):
    id: int = Field(..., description="Student's unique ID")
    name: str = Field(..., description="Student's full name")
    email: Optional[str] = Field(default=None, description="Student's email address")
    preferred_subjects: List[str] = Field(default=[], description="List of preferred subjects")
    learning_style: Optional[str] = Field(default=None, description="Preferred learning style")
    last_studied_topic: Optional[str] = Field(default=None, description="Last studied topic")
    created_at: datetime = Field(..., description="Profile creation timestamp")
    updated_at: datetime = Field(..., description="Profile last update timestamp")
    
    class Config:
        from_attributes = True

class ProfileStats(BaseModel):
    total_questions_asked: int = Field(..., description="Total questions asked by student")
    total_quizzes_taken: int = Field(..., description="Total quizzes taken by student")
    total_notes_summarized: int = Field(..., description="Total notes summarized by student")
    average_quiz_score: Optional[float] = Field(default=None, description="Average quiz score percentage")
    most_studied_topics: List[str] = Field(default=[], description="Most frequently studied topics")
    learning_streak: int = Field(default=0, description="Current learning streak in days")
    total_study_time: int = Field(default=0, description="Total estimated study time in minutes")

class ProfileWithStats(ProfileResponse):
    stats: ProfileStats = Field(..., description="Student's learning statistics")

class ProfileError(BaseModel):
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[dict] = Field(default=None, description="Additional error details")