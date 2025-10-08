import google.generativeai as genai
from typing import List, Dict, Optional
import asyncio
import time
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        """Initialize the AI service with Gemini API"""
        api_key = settings.GEMINI_API_KEY
        if not api_key or api_key.strip() == "":
            raise ValueError(f"GEMINI_API_KEY is required. Current value: '{api_key}'")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        self.max_retries = 3
        self.retry_delay = 1  # seconds
    
    async def _make_request_with_retry(self, prompt: str) -> str:
        """Make a request to Gemini API with retry logic"""
        for attempt in range(self.max_retries):
            try:
                # Run the synchronous Gemini API call in a thread pool
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: self.model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            max_output_tokens=settings.MAX_TOKENS,
                            temperature=settings.TEMPERATURE,
                        )
                    )
                )
                
                if response and hasattr(response, 'text') and response.text:
                    return response.text.strip()
                else:
                    raise Exception("Empty response from Gemini API")
                    
            except Exception as e:
                error_msg = str(e).lower()
                
                # Check for quota/billing errors
                if "402" in error_msg or "quota" in error_msg or "billing" in error_msg:
                    raise Exception(
                        "API quota exceeded or billing required. "
                        "Please check your Gemini API quota at https://aistudio.google.com/app/apikey. "
                        "Free tier has limits on requests per minute and tokens per day."
                    )
                
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))  # Exponential backoff
                else:
                    raise Exception(f"Failed to get response after {self.max_retries} attempts: {str(e)}")
    
    def _get_explanation_prompt(self, question: str, style: str) -> str:
        """Generate prompt based on explanation style"""
        base_prompt = f"Question: {question}\n\n"
        
        if style == "simple":
            return base_prompt + """Please provide a clear, step-by-step explanation that's easy to understand. 
Use simple language and break down complex concepts into smaller parts. 
Format your response with numbered steps and include examples where helpful."""
            
        elif style == "exam-style":
            return base_prompt + """Please provide a detailed explanation suitable for exam preparation. 
Include key formulas, important concepts to remember, and common mistakes to avoid. 
Structure your answer as if preparing a student for a test on this topic."""
            
        elif style == "real-world":
            return base_prompt + """Please explain this concept by connecting it to real-world applications and examples. 
Show how this knowledge is used in practical situations, careers, or everyday life. 
Make the explanation engaging by demonstrating the relevance and importance of the concept."""
            
        else:
            return base_prompt + "Please provide a clear, step-by-step explanation."
    
    async def answer_question(self, question: str, style: str = "simple") -> Dict[str, any]:
        """
        Answer a student's question with step-by-step explanation
        
        Args:
            question: The student's question
            style: Explanation style (simple, exam-style, real-world)
            
        Returns:
            Dictionary containing answer, steps, and metadata
        """
        try:
            prompt = self._get_explanation_prompt(question, style)
            response = await self._make_request_with_retry(prompt)
            
            # Parse the response to extract steps
            lines = response.split('\n')
            explanation_steps = []
            answer_text = response
            
            # Try to identify numbered steps
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('Step')):
                    explanation_steps.append(line)
            
            # If no clear steps found, create basic structure
            if not explanation_steps:
                explanation_steps = [response]
            
            return {
                "answer": answer_text,
                "explanation_steps": explanation_steps,
                "style": style,
                "confidence_score": 0.85,  # Default confidence
                "related_topics": self._extract_topics(response)
            }
            
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            raise Exception(f"Failed to generate answer: {str(e)}")
    
    async def generate_quiz(self, topic: str, question_count: int = 5, difficulty: str = "medium") -> Dict[str, any]:
        """
        Generate quiz questions on a given topic
        
        Args:
            topic: The topic for quiz questions
            question_count: Number of questions to generate (5-10)
            difficulty: Difficulty level (easy, medium, hard)
            
        Returns:
            Dictionary containing quiz questions and metadata
        """
        try:
            prompt = f"""Generate {question_count} {difficulty} level quiz questions about {topic}.

For each question, provide:
1. The question text
2. Question type (multiple_choice or true_false)
3. For multiple choice: 4 options (A, B, C, D)
4. The correct answer
5. A brief explanation of why the answer is correct

Format your response as follows for each question:
Question X: [question text]
Type: [multiple_choice or true_false]
Options: (if multiple choice)
A) [option A]
B) [option B] 
C) [option C]
D) [option D]
Correct Answer: [correct answer]
Explanation: [explanation]

---"""

            response = await self._make_request_with_retry(prompt)
            questions = self._parse_quiz_response(response)
            
            return {
                "questions": questions,
                "topic": topic,
                "difficulty": difficulty,
                "question_count": len(questions),
                "estimated_time": len(questions) * 2  # 2 minutes per question
            }
            
        except Exception as e:
            logger.error(f"Error generating quiz: {str(e)}")
            raise Exception(f"Failed to generate quiz: {str(e)}")
    
    async def summarize_notes(self, content: str) -> Dict[str, any]:
        """
        Summarize long content into concise notes
        
        Args:
            content: The text content to summarize
            
        Returns:
            Dictionary containing summary and key points
        """
        try:
            # Handle long content by chunking if necessary
            if len(content) > settings.MAX_CONTENT_LENGTH:
                content = content[:settings.MAX_CONTENT_LENGTH] + "..."
            
            prompt = f"""Please summarize the following content into concise, well-structured notes:

{content}

Format your response with:
1. A brief overview (2-3 sentences)
2. Key points as bullet points
3. Important terms or concepts highlighted
4. Main takeaways

Make the summary clear and easy to review for studying."""

            response = await self._make_request_with_retry(prompt)
            
            return {
                "summary": response,
                "original_length": len(content),
                "summary_length": len(response),
                "key_terms": self._extract_key_terms(response),
                "structure": "overview_and_bullets"
            }
            
        except Exception as e:
            logger.error(f"Error summarizing content: {str(e)}")
            raise Exception(f"Failed to summarize content: {str(e)}")
    
    def _parse_quiz_response(self, response: str) -> List[Dict]:
        """Parse the AI response to extract quiz questions"""
        questions = []
        current_question = {}
        
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('Question'):
                if current_question:
                    questions.append(current_question)
                current_question = {
                    "id": f"q_{len(questions) + 1}",
                    "question": line.split(':', 1)[1].strip() if ':' in line else line,
                    "type": "multiple_choice",
                    "options": [],
                    "correct_answer": "",
                    "explanation": ""
                }
            elif line.startswith('Type:'):
                current_question["type"] = line.split(':', 1)[1].strip()
            elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                current_question["options"].append(line)
            elif line.startswith('Correct Answer:'):
                current_question["correct_answer"] = line.split(':', 1)[1].strip()
            elif line.startswith('Explanation:'):
                current_question["explanation"] = line.split(':', 1)[1].strip()
        
        # Add the last question
        if current_question:
            questions.append(current_question)
        
        return questions
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract related topics from the response text"""
        # Simple topic extraction - could be enhanced with NLP
        topics = []
        common_topics = ["mathematics", "physics", "chemistry", "biology", "history", "literature", "computer science"]
        
        text_lower = text.lower()
        for topic in common_topics:
            if topic in text_lower:
                topics.append(topic.title())
        
        return topics[:3]  # Return max 3 topics
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from summarized text"""
        # Simple key term extraction
        import re
        
        # Look for capitalized words and technical terms
        key_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Remove common words
        common_words = {"The", "This", "That", "These", "Those", "When", "Where", "What", "How", "Why"}
        key_terms = [term for term in key_terms if term not in common_words]
        
        return list(set(key_terms))[:5]  # Return max 5 unique terms