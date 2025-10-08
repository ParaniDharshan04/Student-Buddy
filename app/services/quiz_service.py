from typing import List, Dict, Any
import uuid
import re
from app.services.ai_service import AIService
from app.schemas.quiz import QuizQuestion, QuestionType, Difficulty
import logging

logger = logging.getLogger(__name__)

class QuizService:
    def __init__(self):
        # Create AIService lazily so the application can start even if
        # GEMINI_API_KEY is not configured during development.
        self.ai_service = None

    def _get_ai_service(self):
        """Return an AIService instance, creating it if necessary.

        Raises ValueError if the AIService cannot be created (e.g. missing API key).
        """
        if self.ai_service is None:
            self.ai_service = AIService()
        return self.ai_service
    
    async def generate_quiz(
        self, 
        topic: str, 
        question_count: int = 5, 
        difficulty: str = "medium",
        question_types: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a quiz using AI service and validate questions
        
        Args:
            topic: Topic for the quiz
            question_count: Number of questions to generate
            difficulty: Difficulty level
            question_types: Types of questions to include
            
        Returns:
            Dictionary containing validated quiz data
        """
        try:
            # Use AI service to generate quiz (create lazily)
            ai_service = self._get_ai_service()
            ai_response = await ai_service.generate_quiz(
                topic=topic,
                question_count=question_count,
                difficulty=difficulty
            )
            
            # Validate and enhance questions
            validated_questions = self._validate_and_enhance_questions(
                ai_response["questions"],
                question_types or ["multiple_choice", "true_false"]
            )
            
            # Generate unique quiz ID
            quiz_id = str(uuid.uuid4())
            
            # Calculate total points
            total_points = sum(q.points for q in validated_questions)
            
            return {
                "quiz_id": quiz_id,
                "questions": validated_questions,
                "topic": topic,
                "difficulty": difficulty,
                "question_count": len(validated_questions),
                "estimated_time": self._calculate_estimated_time(validated_questions),
                "total_points": total_points
            }
            
        except Exception as e:
            logger.error(f"Error generating quiz: {str(e)}")
            raise Exception(f"Failed to generate quiz: {str(e)}")
    
    def _validate_and_enhance_questions(
        self, 
        raw_questions: List[Dict], 
        allowed_types: List[str]
    ) -> List[QuizQuestion]:
        """
        Validate and enhance questions from AI response
        
        Args:
            raw_questions: Raw questions from AI service
            allowed_types: Allowed question types
            
        Returns:
            List of validated QuizQuestion objects
        """
        validated_questions = []
        
        for i, raw_q in enumerate(raw_questions):
            try:
                # Ensure required fields exist
                if not raw_q.get("question") or not raw_q.get("correct_answer"):
                    logger.warning(f"Skipping invalid question {i}: missing required fields")
                    continue
                
                # Determine question type
                question_type = self._determine_question_type(raw_q, allowed_types)
                
                # Validate and format options for multiple choice
                options = None
                if question_type == QuestionType.MULTIPLE_CHOICE:
                    options = self._validate_multiple_choice_options(raw_q)
                    if not options:
                        logger.warning(f"Skipping question {i}: invalid multiple choice options")
                        continue
                
                # Create validated question
                question = QuizQuestion(
                    id=raw_q.get("id", f"q_{i+1}"),
                    question=self._clean_question_text(raw_q["question"]),
                    type=question_type,
                    options=options,
                    correct_answer=self._clean_answer_text(raw_q["correct_answer"]),
                    explanation=raw_q.get("explanation", "No explanation provided."),
                    points=self._calculate_question_points(question_type)
                )
                
                validated_questions.append(question)
                
            except Exception as e:
                logger.warning(f"Error validating question {i}: {str(e)}")
                continue
        
        return validated_questions
    
    def _determine_question_type(self, raw_question: Dict, allowed_types: List[str]) -> QuestionType:
        """Determine the appropriate question type"""
        specified_type = raw_question.get("type", "").lower()
        
        # Check if specified type is valid and allowed
        if specified_type == "multiple_choice" and "multiple_choice" in allowed_types:
            return QuestionType.MULTIPLE_CHOICE
        elif specified_type == "true_false" and "true_false" in allowed_types:
            return QuestionType.TRUE_FALSE
        elif specified_type == "short_answer" and "short_answer" in allowed_types:
            return QuestionType.SHORT_ANSWER
        
        # Auto-detect based on content
        question_text = raw_question.get("question", "").lower()
        options = raw_question.get("options", [])
        
        # Check for true/false indicators
        if any(word in question_text for word in ["true or false", "is it true", "correct or incorrect"]):
            if "true_false" in allowed_types:
                return QuestionType.TRUE_FALSE
        
        # Check for multiple choice options
        if options and len(options) >= 2:
            if "multiple_choice" in allowed_types:
                return QuestionType.MULTIPLE_CHOICE
        
        # Default to first allowed type
        type_mapping = {
            "multiple_choice": QuestionType.MULTIPLE_CHOICE,
            "true_false": QuestionType.TRUE_FALSE,
            "short_answer": QuestionType.SHORT_ANSWER
        }
        
        for allowed_type in allowed_types:
            if allowed_type in type_mapping:
                return type_mapping[allowed_type]
        
        return QuestionType.MULTIPLE_CHOICE  # Final fallback
    
    def _validate_multiple_choice_options(self, raw_question: Dict) -> List[str]:
        """Validate and format multiple choice options"""
        options = raw_question.get("options", [])
        
        if not options:
            return None
        
        # Clean and format options
        cleaned_options = []
        for option in options:
            if isinstance(option, str):
                # Remove leading letters/numbers and clean
                cleaned = re.sub(r'^[A-D]\)\s*', '', option.strip())
                if cleaned:
                    cleaned_options.append(cleaned)
        
        # Ensure we have at least 2 options for multiple choice
        if len(cleaned_options) < 2:
            return None
        
        return cleaned_options
    
    def _clean_question_text(self, question: str) -> str:
        """Clean and format question text"""
        if not question:
            return ""
        
        # Remove extra whitespace and ensure proper punctuation
        cleaned = re.sub(r'\s+', ' ', question.strip())
        
        # Ensure question ends with question mark if it's a question
        if cleaned and not cleaned.endswith(('?', '.', '!', ':')):
            cleaned += '?'
        
        return cleaned
    
    def _clean_answer_text(self, answer: str) -> str:
        """Clean and format answer text"""
        if not answer:
            return ""
        
        # Remove leading letters/numbers from answers like "A) Paris"
        cleaned = re.sub(r'^[A-D]\)\s*', '', answer.strip())
        return cleaned
    
    def _calculate_question_points(self, question_type: QuestionType) -> int:
        """Calculate points for different question types"""
        point_values = {
            QuestionType.MULTIPLE_CHOICE: 1,
            QuestionType.TRUE_FALSE: 1,
            QuestionType.SHORT_ANSWER: 2
        }
        return point_values.get(question_type, 1)
    
    def _calculate_estimated_time(self, questions: List[QuizQuestion]) -> int:
        """Calculate estimated time to complete quiz in minutes"""
        time_per_type = {
            QuestionType.MULTIPLE_CHOICE: 1.5,  # minutes
            QuestionType.TRUE_FALSE: 0.5,
            QuestionType.SHORT_ANSWER: 3.0
        }
        
        total_time = 0
        for question in questions:
            total_time += time_per_type.get(question.type, 1.5)
        
        # Round up to nearest minute, minimum 1 minute
        return max(1, int(total_time + 0.5))
    
    def calculate_quiz_score(
        self, 
        questions: List[QuizQuestion], 
        student_answers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Calculate quiz score and provide detailed feedback
        
        Args:
            questions: List of quiz questions
            student_answers: Student's answers mapped by question ID
            
        Returns:
            Dictionary containing score and feedback
        """
        correct_count = 0
        total_points = 0
        earned_points = 0
        feedback = []
        
        for question in questions:
            student_answer = student_answers.get(question.id, "").strip()
            is_correct = self._is_answer_correct(question, student_answer)
            
            total_points += question.points
            if is_correct:
                correct_count += 1
                earned_points += question.points
            
            feedback.append({
                "question_id": question.id,
                "question": question.question,
                "student_answer": student_answer,
                "correct_answer": question.correct_answer,
                "is_correct": is_correct,
                "explanation": question.explanation,
                "points_earned": question.points if is_correct else 0,
                "points_possible": question.points
            })
        
        # Calculate percentage score
        score_percentage = (earned_points / total_points * 100) if total_points > 0 else 0
        
        return {
            "score": round(score_percentage, 2),
            "correct_answers": correct_count,
            "total_questions": len(questions),
            "points_earned": earned_points,
            "points_possible": total_points,
            "feedback": feedback
        }
    
    def _is_answer_correct(self, question: QuizQuestion, student_answer: str) -> bool:
        """Check if student's answer is correct"""
        if not student_answer:
            return False
        
        correct_answer = question.correct_answer.lower().strip()
        student_answer = student_answer.lower().strip()
        
        if question.type == QuestionType.TRUE_FALSE:
            # Handle various true/false formats
            true_answers = ["true", "t", "yes", "y", "correct", "1"]
            false_answers = ["false", "f", "no", "n", "incorrect", "0"]
            
            student_is_true = student_answer in true_answers
            correct_is_true = correct_answer in true_answers
            
            return student_is_true == correct_is_true
        
        elif question.type == QuestionType.MULTIPLE_CHOICE:
            # For multiple choice, check if answer matches any option
            if question.options:
                for option in question.options:
                    if option.lower().strip() == student_answer:
                        return option.lower().strip() == correct_answer
            
            # Direct comparison as fallback
            return student_answer == correct_answer
        
        else:  # SHORT_ANSWER
            # For short answers, allow some flexibility
            return student_answer == correct_answer or student_answer in correct_answer