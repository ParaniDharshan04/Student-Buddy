from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class ConversationMessage(BaseModel):
    role: str = Field(..., description="Role: user or assistant")
    content: str = Field(..., description="Message content")

class VoiceChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="User's spoken message")
    conversation_mode: str = Field(default="practice", description="Conversation mode: practice, interview, or presentation")
    conversation_history: List[ConversationMessage] = Field(default=[], description="Previous conversation messages")

class VoiceChatFeedback(BaseModel):
    mode: str
    encouragement: str
    areas_to_improve: List[str]

class VoiceChatResponse(BaseModel):
    response: str = Field(..., description="AI's response")
    feedback: Optional[VoiceChatFeedback] = Field(default=None, description="Feedback on communication")
    suggestions: List[str] = Field(default=[], description="Suggestions for improvement")
