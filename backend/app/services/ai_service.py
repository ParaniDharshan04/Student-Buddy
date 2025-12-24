from google import genai
from google.genai import types
import time
import json
from typing import Dict, Any, List, Optional
from ..config import settings


class AIService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_id = settings.GEMINI_MODEL
    
    def _call_with_retry(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Call Gemini API with retry logic"""
        for attempt in range(settings.AI_RETRY_ATTEMPTS):
            try:
                messages = []
                if system_instruction:
                    messages.append(types.Content(
                        role="user",
                        parts=[types.Part(text=system_instruction)]
                    ))
                
                messages.append(types.Content(
                    role="user",
                    parts=[types.Part(text=prompt)]
                ))
                
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=messages,
                    config=types.GenerateContentConfig(
                        temperature=settings.AI_TEMPERATURE,
                        max_output_tokens=settings.AI_MAX_TOKENS,
                    )
                )
                
                return response.text
            except Exception as e:
                if attempt < settings.AI_RETRY_ATTEMPTS - 1:
                    time.sleep(settings.AI_RETRY_DELAY * (attempt + 1))
                else:
                    raise Exception(f"AI service error after {settings.AI_RETRY_ATTEMPTS} attempts: {str(e)}")
    
    def answer_question(self, question: str, explanation_type: str = "simple") -> Dict[str, Any]:
        """Generate answer to student question"""
        system_prompts = {
            "simple": "You are a friendly tutor explaining concepts in simple, easy-to-understand language suitable for beginners.",
            "exam": "You are an exam preparation tutor. Provide structured answers with key points, formulas, and exam tips.",
            "real_world": "You are a practical tutor connecting concepts to real-world applications and examples."
        }
        
        system_instruction = system_prompts.get(explanation_type, system_prompts["simple"])
        
        prompt = f"""Answer the following student question clearly and accurately.

Question: {question}

Provide your response in the following JSON format:
{{
    "answer": "detailed answer here",
    "topics": ["topic1", "topic2"],
    "concepts": ["concept1", "concept2"],
    "confidence_score": 0.95
}}

IMPORTANT FORMATTING RULES:
- Do NOT use asterisks (*) for emphasis or bullet points
- Do NOT use markdown formatting (**, __, ##, etc.)
- Use plain text only
- Use numbers (1, 2, 3) for lists instead of asterisks
- Use clear paragraph breaks for readability
- Keep the answer professional and educational
- Write in a natural, conversational style"""
        
        response_text = self._call_with_retry(prompt, system_instruction)
        
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                response_data = json.loads(response_text[json_start:json_end])
                # Clean up any remaining asterisks
                if 'answer' in response_data:
                    response_data['answer'] = response_data['answer'].replace('**', '').replace('*', '')
            else:
                response_data = {
                    "answer": response_text.replace('**', '').replace('*', ''),
                    "topics": [],
                    "concepts": [],
                    "confidence_score": 0.8
                }
        except json.JSONDecodeError:
            response_data = {
                "answer": response_text.replace('**', '').replace('*', ''),
                "topics": [],
                "concepts": [],
                "confidence_score": 0.8
            }
        
        return response_data
    
    def generate_quiz(self, topic: str, difficulty: str, question_count: int, question_types: List[str]) -> Dict[str, Any]:
        """Generate quiz questions"""
        prompt = f"""Generate a quiz on the following topic: {topic}

Requirements:
- Difficulty: {difficulty}
- Number of questions: {question_count}
- Question types: {', '.join(question_types)}

Provide your response in the following JSON format:
{{
    "title": "Quiz title",
    "questions": [
        {{
            "id": 1,
            "type": "mcq",
            "question": "Question text",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Option A",
            "explanation": "Why this is correct"
        }}
    ]
}}

IMPORTANT FORMATTING RULES:
- Do NOT use asterisks (*) or markdown formatting
- Use plain text only
- For true_false questions, use options: ["True", "False"]
- For short_answer questions, omit the options field
- Keep questions educational and appropriate for the difficulty level
- Write in clear, simple language"""
        
        response_text = self._call_with_retry(prompt)
        
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                quiz_data = json.loads(response_text[json_start:json_end])
                # Clean up asterisks from questions and explanations
                if 'questions' in quiz_data:
                    for q in quiz_data['questions']:
                        if 'question' in q:
                            q['question'] = q['question'].replace('**', '').replace('*', '')
                        if 'explanation' in q:
                            q['explanation'] = q['explanation'].replace('**', '').replace('*', '')
            else:
                raise ValueError("No valid JSON found in response")
        except (json.JSONDecodeError, ValueError):
            quiz_data = {
                "title": f"Quiz on {topic}",
                "questions": []
            }
        
        return quiz_data
    
    def summarize_text(self, text: str, format_type: str = "bullet_points") -> Dict[str, Any]:
        """Summarize text in specified format"""
        format_instructions = {
            "bullet_points": "Provide a summary as clear bullet points highlighting key information. Use numbers (1, 2, 3) instead of asterisks.",
            "paragraph": "Provide a summary as a cohesive paragraph.",
            "outline": "Provide a summary as a hierarchical outline with main points and sub-points. Use numbers instead of asterisks.",
            "key_concepts": "Extract and explain the key concepts from the text."
        }
        
        instruction = format_instructions.get(format_type, format_instructions["bullet_points"])
        
        prompt = f"""Summarize the following text. {instruction}

Text to summarize:
{text}

Provide your response in the following JSON format:
{{
    "summary": "summary text here",
    "key_terms": ["term1", "term2", "term3"]
}}

IMPORTANT FORMATTING RULES:
- Do NOT use asterisks (*) or markdown formatting
- Use plain text only
- For lists, use numbers (1, 2, 3) instead of asterisks
- Keep the summary concise and educational
- Write in clear, simple language"""
        
        response_text = self._call_with_retry(prompt)
        
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                summary_data = json.loads(response_text[json_start:json_end])
                # Clean up asterisks
                if 'summary' in summary_data:
                    summary_data['summary'] = summary_data['summary'].replace('**', '').replace('*', '')
            else:
                summary_data = {
                    "summary": response_text.replace('**', '').replace('*', ''),
                    "key_terms": []
                }
        except json.JSONDecodeError:
            summary_data = {
                "summary": response_text.replace('**', '').replace('*', ''),
                "key_terms": []
            }
        
        return summary_data
    
    def voice_conversation(self, message: str, mode: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Handle voice conversation with context"""
        mode_prompts = {
            "casual": "You are a friendly conversation partner helping a student practice casual English communication. Be encouraging and natural.",
            "interview": "You are an interview coach conducting a mock interview. Ask relevant questions and provide constructive feedback using the STAR method.",
            "presentation": "You are a public speaking coach helping a student practice presentation skills. Provide feedback on clarity, structure, and delivery."
        }
        
        system_instruction = mode_prompts.get(mode, mode_prompts["casual"])
        
        context = ""
        if conversation_history:
            context = "Previous conversation:\n"
            for msg in conversation_history[-5:]:
                context += f"{msg['role']}: {msg['content']}\n"
            context += "\n"
        
        prompt = f"""{context}Student: {message}

Respond naturally and provide helpful feedback. Keep responses conversational and concise.

Provide your response in the following JSON format:
{{
    "response": "your response here",
    "feedback": {{
        "fluency_score": 8.5,
        "suggestions": ["suggestion1", "suggestion2"]
    }}
}}

IMPORTANT FORMATTING RULES:
- Do NOT use asterisks (*) or markdown formatting
- Use plain text only
- Write in a natural, conversational style
- Keep responses clear and easy to understand
- Provide constructive, encouraging feedback"""
        
        response_text = self._call_with_retry(prompt, system_instruction)
        
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                conversation_data = json.loads(response_text[json_start:json_end])
                # Clean up asterisks
                if 'response' in conversation_data:
                    conversation_data['response'] = conversation_data['response'].replace('**', '').replace('*', '')
                if 'feedback' in conversation_data and 'suggestions' in conversation_data['feedback']:
                    conversation_data['feedback']['suggestions'] = [
                        s.replace('**', '').replace('*', '') for s in conversation_data['feedback']['suggestions']
                    ]
            else:
                conversation_data = {
                    "response": response_text.replace('**', '').replace('*', ''),
                    "feedback": {}
                }
        except json.JSONDecodeError:
            conversation_data = {
                "response": response_text.replace('**', '').replace('*', ''),
                "feedback": {}
            }
        
        return conversation_data


ai_service = AIService()
