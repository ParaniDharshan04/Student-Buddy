from typing import List, Dict, Any
from app.services.ai_service import AIService
import logging

logger = logging.getLogger(__name__)

class VoiceChatService:
    def __init__(self):
        self.ai_service = None
    
    def _get_ai_service(self):
        """Get AI service instance"""
        if self.ai_service is None:
            self.ai_service = AIService()
        return self.ai_service
    
    async def get_response(
        self,
        message: str,
        conversation_mode: str = "practice",
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Get AI response for voice chat
        
        Args:
            message: User's message
            conversation_mode: Type of conversation (practice, interview, presentation)
            conversation_history: Previous messages for context
            
        Returns:
            Dictionary with response, feedback, and suggestions
        """
        try:
            # Build conversation context
            system_prompt = self._get_system_prompt(conversation_mode)
            
            # Build conversation history
            history = conversation_history or []
            
            # Create prompt with context
            prompt = self._build_prompt(message, conversation_mode, history)
            
            # Get AI response
            ai_service = self._get_ai_service()
            response = await ai_service._make_request_with_retry(prompt)
            
            # Clean the response (remove markdown and emojis)
            cleaned_response = self._clean_response(response)
            
            # Parse response for feedback
            feedback = self._extract_feedback(cleaned_response, conversation_mode)
            suggestions = self._generate_suggestions(message, conversation_mode)
            
            return {
                "response": cleaned_response,
                "feedback": feedback,
                "suggestions": suggestions
            }
            
        except Exception as e:
            logger.error(f"Error getting voice chat response: {str(e)}")
            raise
    
    def _get_system_prompt(self, mode: str) -> str:
        """Get system prompt based on conversation mode"""
        prompts = {
            "practice": """You are a friendly English conversation partner helping someone practice their communication skills. 
Be encouraging, natural, and conversational. Ask follow-up questions to keep the conversation flowing. 
Gently correct major grammar mistakes but focus on building confidence.""",
            
            "interview": """You are a professional interviewer conducting a mock job interview. 
Ask relevant interview questions, provide constructive feedback on answers, and help the candidate improve their responses. 
Be professional but supportive.""",
            
            "presentation": """You are a presentation coach helping someone practice public speaking. 
Provide feedback on clarity, structure, and delivery. Ask questions to help them organize their thoughts better. 
Encourage confident and clear communication."""
        }
        return prompts.get(mode, prompts["practice"])
    
    def _build_prompt(
        self,
        message: str,
        mode: str,
        history: List[Dict[str, str]]
    ) -> str:
        """Build prompt with conversation context"""
        system_prompt = self._get_system_prompt(mode)
        
        # Build conversation context
        context = f"{system_prompt}\n\n"
        
        if history:
            context += "Previous conversation:\n"
            for msg in history[-5:]:  # Last 5 messages for context
                role = msg.get("role", "user")
                content = msg.get("content", "")
                context += f"{role.capitalize()}: {content}\n"
            context += "\n"
        
        context += f"User: {message}\n\nRespond naturally and helpfully:"
        
        return context
    
    def _extract_feedback(self, response: str, mode: str) -> Dict[str, Any]:
        """Extract feedback from response"""
        # Simple feedback based on mode
        feedback = {
            "mode": mode,
            "encouragement": "Great job practicing!",
            "areas_to_improve": []
        }
        
        if mode == "interview":
            feedback["areas_to_improve"] = [
                "Consider providing specific examples",
                "Structure your answer with STAR method (Situation, Task, Action, Result)"
            ]
        elif mode == "presentation":
            feedback["areas_to_improve"] = [
                "Use clear transitions between points",
                "Maintain confident tone throughout"
            ]
        
        return feedback
    
    def _clean_response(self, text: str) -> str:
        """Clean AI response by removing markdown and emojis"""
        import re
        
        # Remove markdown bold (**text**)
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        
        # Remove markdown italic (*text* or _text_)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)
        
        # Remove markdown headers (# ## ###)
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        
        # Remove bullet points (* or -)
        text = re.sub(r'^\s*[\*\-]\s+', '', text, flags=re.MULTILINE)
        
        # Remove emojis (basic emoji removal)
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        text = emoji_pattern.sub('', text)
        
        # Clean up extra whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Multiple newlines to double
        text = text.strip()
        
        return text
    
    def _generate_suggestions(self, message: str, mode: str) -> List[str]:
        """Generate suggestions for improvement"""
        suggestions = []
        
        if mode == "practice":
            suggestions = [
                "Try to elaborate more on your thoughts",
                "Use varied vocabulary to express ideas",
                "Practice speaking in complete sentences"
            ]
        elif mode == "interview":
            suggestions = [
                "Prepare specific examples from your experience",
                "Practice the STAR method for behavioral questions",
                "Research common interview questions"
            ]
        elif mode == "presentation":
            suggestions = [
                "Organize your points with clear structure",
                "Use pauses for emphasis",
                "Practice maintaining eye contact (imagine your audience)"
            ]
        
        return suggestions[:3]  # Return top 3 suggestions
