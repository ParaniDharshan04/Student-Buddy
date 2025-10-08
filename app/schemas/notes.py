from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum

class SummaryFormat(str, Enum):
    BULLET_POINTS = "bullet_points"
    PARAGRAPH = "paragraph"
    OUTLINE = "outline"
    KEY_CONCEPTS = "key_concepts"

class NotesRequest(BaseModel):
    content: str = Field(..., min_length=10, max_length=10000, description="Text content to summarize")
    format: SummaryFormat = Field(default=SummaryFormat.BULLET_POINTS, description="Format for the summary")
    max_length: Optional[int] = Field(default=None, ge=50, le=2000, description="Maximum length of summary in characters")
    student_id: Optional[int] = Field(default=None, description="ID of the student requesting summary")
    topic: Optional[str] = Field(default=None, max_length=200, description="Optional topic/subject for context")
    
    @validator('content')
    def validate_content(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Content cannot be empty')
        # Remove excessive whitespace
        return ' '.join(v.split())
    
    @validator('topic')
    def validate_topic(cls, v):
        if v:
            return v.strip()
        return v

class NotesResponse(BaseModel):
    summary: str = Field(..., description="The summarized content")
    format: str = Field(..., description="Format used for the summary")
    original_length: int = Field(..., description="Length of original content in characters")
    summary_length: int = Field(..., description="Length of summary in characters")
    compression_ratio: float = Field(..., description="Ratio of summary to original length")
    key_terms: List[str] = Field(default=[], description="Important terms extracted from content")
    main_topics: List[str] = Field(default=[], description="Main topics identified in the content")
    reading_time: int = Field(..., description="Estimated reading time for summary in minutes")
    session_id: Optional[int] = Field(default=None, description="ID of the created study session")

class NotesError(BaseModel):
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[dict] = Field(default=None, description="Additional error details")