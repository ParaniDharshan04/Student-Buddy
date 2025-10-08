import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.quiz_service import QuizService
from app.schemas.quiz import QuizQuestion, QuestionType

class TestQuizService:
    
    @pytest.fixture
    def quiz_service(self):
        """Create QuizService instance for testing"""
        with patch('app.services.quiz_service.AIService') as mock_ai:
            mock_ai.return_value = Mock()
            return QuizService()
    
    @pytest.fixture
    def mock_ai_quiz_response(self):
        """Mock AI service quiz response"""
        return {
            "questions": [
                {
                    "id": "q_1",
                    "question": "What is the capital of France?",
                    "type": "multiple_choice",
                    "options": ["A) London", "B) Paris", "C) Berlin", "D) Madrid"],
                    "correct_answer": "B) Paris",
                    "explanation": "Paris is the capital city of France"
                },
                {
                    "id": "q_2",
                    "question": "Is Python a programming language?",
                    "type": "true_false",
                    "correct_answer": "True",
                    "explanation": "Python is indeed a programming language"
                }
            ],
            "topic": "General Knowledge",
            "difficulty": "medium",
            "question_count": 2,
            "estimated_time": 3
        }
    
    @pytest.mark.asyncio
    async def test_generate_quiz_success(self, quiz_service, mock_ai_quiz_response):
        """Test successful quiz generation"""
        quiz_service.ai_service.generate_quiz = AsyncMock(return_value=mock_ai_quiz_response)
        
        result = await quiz_service.generate_quiz(
            topic="General Knowledge",
            question_count=2,
            difficulty="medium"
        )
        
        assert "quiz_id" in result
        assert result["topic"] == "General Knowledge"
        assert result["difficulty"] == "medium"
        assert result["question_count"] == 2
        assert len(result["questions"]) == 2
        assert result["total_points"] > 0
        assert result["estimated_time"] > 0
    
    @pytest.mark.asyncio
    async def test_generate_quiz_ai_service_error(self, quiz_service):
        """Test quiz generation when AI service fails"""
        quiz_service.ai_service.generate_quiz = AsyncMock(side_effect=Exception("AI Error"))
        
        with pytest.raises(Exception) as exc_info:
            await quiz_service.generate_quiz("Mathematics", 5)
        
        assert "Failed to generate quiz" in str(exc_info.value)
    
    def test_validate_and_enhance_questions(self, quiz_service):
        """Test question validation and enhancement"""
        raw_questions = [
            {
                "id": "q_1",
                "question": "What is 2+2?",
                "type": "multiple_choice",
                "options": ["A) 3", "B) 4", "C) 5", "D) 6"],
                "correct_answer": "B) 4",
                "explanation": "Basic addition"
            },
            {
                "question": "Is Earth round?",
                "type": "true_false",
                "correct_answer": "True",
                "explanation": "Earth is approximately spherical"
            },
            {
                # Invalid question - missing required fields
                "question": "",
                "type": "multiple_choice"
            }
        ]
        
        result = quiz_service._validate_and_enhance_questions(
            raw_questions, 
            ["multiple_choice", "true_false"]
        )
        
        # Should have 2 valid questions (third one is invalid)
        assert len(result) == 2
        assert all(isinstance(q, QuizQuestion) for q in result)
        assert result[0].type == QuestionType.MULTIPLE_CHOICE
        assert result[1].type == QuestionType.TRUE_FALSE
    
    def test_determine_question_type(self, quiz_service):
        """Test question type determination"""
        # Test explicit multiple choice
        mc_question = {
            "question": "What is the capital?",
            "type": "multiple_choice",
            "options": ["A) London", "B) Paris"]
        }
        result = quiz_service._determine_question_type(mc_question, ["multiple_choice", "true_false"])
        assert result == QuestionType.MULTIPLE_CHOICE
        
        # Test explicit true/false
        tf_question = {
            "question": "Is this true?",
            "type": "true_false"
        }
        result = quiz_service._determine_question_type(tf_question, ["true_false"])
        assert result == QuestionType.TRUE_FALSE
        
        # Test auto-detection from content
        auto_tf_question = {
            "question": "True or false: Python is a language?"
        }
        result = quiz_service._determine_question_type(auto_tf_question, ["true_false", "multiple_choice"])
        assert result == QuestionType.TRUE_FALSE
    
    def test_validate_multiple_choice_options(self, quiz_service):
        """Test multiple choice option validation"""
        # Valid options
        valid_question = {
            "options": ["A) Paris", "B) London", "C) Berlin", "D) Madrid"]
        }
        result = quiz_service._validate_multiple_choice_options(valid_question)
        assert result == ["Paris", "London", "Berlin", "Madrid"]
        
        # Invalid options (too few)
        invalid_question = {
            "options": ["A) Only one option"]
        }
        result = quiz_service._validate_multiple_choice_options(invalid_question)
        assert result is None
        
        # No options
        no_options_question = {}
        result = quiz_service._validate_multiple_choice_options(no_options_question)
        assert result is None
    
    def test_clean_question_text(self, quiz_service):
        """Test question text cleaning"""
        # Test basic cleaning
        result = quiz_service._clean_question_text("  What is Python  ")
        assert result == "What is Python?"
        
        # Test with existing punctuation
        result = quiz_service._clean_question_text("What is AI?")
        assert result == "What is AI?"
        
        # Test with multiple spaces
        result = quiz_service._clean_question_text("What    is    machine    learning")
        assert result == "What is machine learning?"
    
    def test_clean_answer_text(self, quiz_service):
        """Test answer text cleaning"""
        # Test removing option letters
        result = quiz_service._clean_answer_text("B) Paris")
        assert result == "Paris"
        
        # Test without option letters
        result = quiz_service._clean_answer_text("True")
        assert result == "True"
        
        # Test with spaces
        result = quiz_service._clean_answer_text("  A) London  ")
        assert result == "London"
    
    def test_calculate_question_points(self, quiz_service):
        """Test point calculation for different question types"""
        assert quiz_service._calculate_question_points(QuestionType.MULTIPLE_CHOICE) == 1
        assert quiz_service._calculate_question_points(QuestionType.TRUE_FALSE) == 1
        assert quiz_service._calculate_question_points(QuestionType.SHORT_ANSWER) == 2
    
    def test_calculate_estimated_time(self, quiz_service):
        """Test estimated time calculation"""
        questions = [
            QuizQuestion(
                id="q1", question="Test?", type=QuestionType.MULTIPLE_CHOICE,
                correct_answer="A", explanation="Test"
            ),
            QuizQuestion(
                id="q2", question="Test?", type=QuestionType.TRUE_FALSE,
                correct_answer="True", explanation="Test"
            ),
            QuizQuestion(
                id="q3", question="Test?", type=QuestionType.SHORT_ANSWER,
                correct_answer="Answer", explanation="Test"
            )
        ]
        
        time = quiz_service._calculate_estimated_time(questions)
        assert time >= 1  # At least 1 minute
        assert isinstance(time, int)
    
    def test_calculate_quiz_score(self, quiz_service):
        """Test quiz score calculation"""
        questions = [
            QuizQuestion(
                id="q1", question="What is 2+2?", type=QuestionType.MULTIPLE_CHOICE,
                options=["3", "4", "5", "6"], correct_answer="4", explanation="Basic math", points=1
            ),
            QuizQuestion(
                id="q2", question="Is Python a language?", type=QuestionType.TRUE_FALSE,
                correct_answer="True", explanation="Yes it is", points=1
            )
        ]
        
        student_answers = {
            "q1": "4",    # Correct
            "q2": "False" # Incorrect
        }
        
        result = quiz_service.calculate_quiz_score(questions, student_answers)
        
        assert result["score"] == 50.0  # 1 out of 2 correct = 50%
        assert result["correct_answers"] == 1
        assert result["total_questions"] == 2
        assert result["points_earned"] == 1
        assert result["points_possible"] == 2
        assert len(result["feedback"]) == 2
    
    def test_is_answer_correct(self, quiz_service):
        """Test answer correctness checking"""
        # Multiple choice question
        mc_question = QuizQuestion(
            id="q1", question="Capital of France?", type=QuestionType.MULTIPLE_CHOICE,
            options=["London", "Paris", "Berlin"], correct_answer="Paris", explanation="Test"
        )
        assert quiz_service._is_answer_correct(mc_question, "Paris") == True
        assert quiz_service._is_answer_correct(mc_question, "London") == False
        
        # True/False question
        tf_question = QuizQuestion(
            id="q2", question="Is Python a language?", type=QuestionType.TRUE_FALSE,
            correct_answer="True", explanation="Test"
        )
        assert quiz_service._is_answer_correct(tf_question, "True") == True
        assert quiz_service._is_answer_correct(tf_question, "t") == True
        assert quiz_service._is_answer_correct(tf_question, "False") == False
        
        # Short answer question
        sa_question = QuizQuestion(
            id="q3", question="What is AI?", type=QuestionType.SHORT_ANSWER,
            correct_answer="artificial intelligence", explanation="Test"
        )
        assert quiz_service._is_answer_correct(sa_question, "artificial intelligence") == True
        assert quiz_service._is_answer_correct(sa_question, "machine learning") == False