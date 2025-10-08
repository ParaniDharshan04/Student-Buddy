import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from app.main import app
from app.schemas.question import QuestionRequest, ExplanationStyle

client = TestClient(app)

class TestQuestionAPI:
    
    @pytest.fixture
    def mock_ai_response(self):
        """Mock AI service response"""
        return {
            "answer": "The answer is 4. Here's the step-by-step explanation.",
            "explanation_steps": ["Step 1: Add 2", "Step 2: Add another 2", "Step 3: Result is 4"],
            "style": "simple",
            "confidence_score": 0.95,
            "related_topics": ["Mathematics", "Arithmetic"]
        }
    
    @patch('app.api.question.ai_service.answer_question')
    @patch('app.api.question.get_db')
    def test_ask_question_success(self, mock_get_db, mock_answer_question, mock_ai_response):
        """Test successful question answering"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock AI service
        mock_answer_question.return_value = mock_ai_response
        
        # Test request
        response = client.post("/api/ask", json={
            "question": "What is 2+2?",
            "explanation_style": "simple"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == mock_ai_response["answer"]
        assert data["style"] == "simple"
        assert len(data["explanation_steps"]) == 3
        assert data["confidence_score"] == 0.95
    
    @patch('app.api.question.ai_service.answer_question')
    @patch('app.api.question.get_db')
    def test_ask_question_with_student_id(self, mock_get_db, mock_answer_question, mock_ai_response):
        """Test question answering with student ID"""
        # Mock database session and student
        mock_db = Mock()
        mock_student = Mock()
        mock_student.id = 1
        mock_db.query.return_value.filter.return_value.first.return_value = mock_student
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock AI service
        mock_answer_question.return_value = mock_ai_response
        
        # Test request with student ID
        response = client.post("/api/ask", json={
            "question": "Explain photosynthesis",
            "explanation_style": "exam-style",
            "student_id": 1
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == mock_ai_response["answer"]
        assert data["style"] == "simple"  # From mock response
        
        # Verify database operations were called
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
    
    def test_ask_question_empty_question(self):
        """Test error handling for empty question"""
        response = client.post("/api/ask", json={
            "question": "",
            "explanation_style": "simple"
        })
        
        assert response.status_code == 400
        assert "cannot be empty" in response.json()["detail"]
    
    def test_ask_question_invalid_style(self):
        """Test error handling for invalid explanation style"""
        response = client.post("/api/ask", json={
            "question": "What is gravity?",
            "explanation_style": "invalid_style"
        })
        
        assert response.status_code == 422  # Validation error
    
    @patch('app.api.question.ai_service.answer_question')
    @patch('app.api.question.get_db')
    def test_ask_question_ai_service_error(self, mock_get_db, mock_answer_question):
        """Test error handling when AI service fails"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock AI service to raise exception
        mock_answer_question.side_effect = Exception("AI service error")
        
        response = client.post("/api/ask", json={
            "question": "What is quantum physics?",
            "explanation_style": "simple"
        })
        
        assert response.status_code == 500
        assert "Failed to process question" in response.json()["detail"]
    
    def test_get_explanation_styles(self):
        """Test getting available explanation styles"""
        response = client.get("/api/ask/styles")
        
        assert response.status_code == 200
        data = response.json()
        assert "styles" in data
        assert len(data["styles"]) == 3
        
        styles = {style["value"] for style in data["styles"]}
        assert styles == {"simple", "exam-style", "real-world"}
    
    def test_question_request_validation(self):
        """Test QuestionRequest validation"""
        # Valid request
        valid_request = QuestionRequest(
            question="What is the meaning of life?",
            explanation_style=ExplanationStyle.SIMPLE
        )
        assert valid_request.question == "What is the meaning of life?"
        assert valid_request.explanation_style == ExplanationStyle.SIMPLE
        
        # Test question trimming
        request_with_spaces = QuestionRequest(
            question="  What is AI?  ",
            explanation_style=ExplanationStyle.REAL_WORLD
        )
        assert request_with_spaces.question == "What is AI?"
    
    def test_question_request_validation_errors(self):
        """Test QuestionRequest validation errors"""
        # Empty question should raise validation error
        with pytest.raises(ValueError, match="Question cannot be empty"):
            QuestionRequest(
                question="",
                explanation_style=ExplanationStyle.SIMPLE
            )
        
        # Whitespace-only question should raise validation error
        with pytest.raises(ValueError, match="Question cannot be empty"):
            QuestionRequest(
                question="   ",
                explanation_style=ExplanationStyle.SIMPLE
            )
    
    @patch('app.api.question._extract_topic_from_question')
    def test_extract_topic_from_question(self, mock_extract):
        """Test topic extraction function"""
        from app.api.question import _extract_topic_from_question
        
        # Test math question
        topic = _extract_topic_from_question("What is the derivative of x^2?")
        assert topic == "Math"
        
        # Test physics question
        topic = _extract_topic_from_question("Explain Newton's laws of motion")
        assert topic == "Physics"
        
        # Test chemistry question
        topic = _extract_topic_from_question("What happens in a chemical reaction?")
        assert topic == "Chemistry"
        
        # Test general question
        topic = _extract_topic_from_question("How do I study effectively?")
        assert topic in ["General", "How Do I"]  # Could be either depending on implementation