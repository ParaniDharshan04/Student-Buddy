import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from app.main import app
from app.schemas.quiz import QuizRequest, QuestionType, Difficulty

client = TestClient(app)

class TestQuizAPI:
    
    @pytest.fixture
    def mock_quiz_response(self):
        """Mock quiz service response"""
        return {
            "quiz_id": "test-quiz-123",
            "questions": [
                {
                    "id": "q_1",
                    "question": "What is 2+2?",
                    "type": "multiple_choice",
                    "options": ["3", "4", "5", "6"],
                    "correct_answer": "4",
                    "explanation": "Basic addition: 2+2=4",
                    "points": 1
                },
                {
                    "id": "q_2", 
                    "question": "Is Python a programming language?",
                    "type": "true_false",
                    "options": None,
                    "correct_answer": "True",
                    "explanation": "Python is indeed a programming language",
                    "points": 1
                }
            ],
            "topic": "Mathematics",
            "difficulty": "easy",
            "question_count": 2,
            "estimated_time": 3,
            "total_points": 2
        }
    
    @patch('app.api.quiz.quiz_service.generate_quiz')
    @patch('app.api.quiz.get_db')
    def test_generate_quiz_success(self, mock_get_db, mock_generate_quiz, mock_quiz_response):
        """Test successful quiz generation"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock quiz service
        mock_generate_quiz.return_value = mock_quiz_response
        
        # Test request
        response = client.post("/api/quiz", json={
            "topic": "Mathematics",
            "question_count": 2,
            "difficulty": "easy",
            "question_types": ["multiple_choice", "true_false"]
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["quiz_id"] == "test-quiz-123"
        assert data["topic"] == "Mathematics"
        assert data["question_count"] == 2
        assert len(data["questions"]) == 2
        assert data["estimated_time"] == 3
    
    @patch('app.api.quiz.quiz_service.generate_quiz')
    @patch('app.api.quiz.get_db')
    def test_generate_quiz_with_student_id(self, mock_get_db, mock_generate_quiz, mock_quiz_response):
        """Test quiz generation with student ID"""
        # Mock database session and student
        mock_db = Mock()
        mock_student = Mock()
        mock_student.id = 1
        mock_db.query.return_value.filter.return_value.first.return_value = mock_student
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock quiz service
        mock_generate_quiz.return_value = mock_quiz_response
        
        # Test request with student ID
        response = client.post("/api/quiz", json={
            "topic": "Physics",
            "question_count": 5,
            "difficulty": "medium",
            "question_types": ["multiple_choice"],
            "student_id": 1
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["topic"] == "Mathematics"  # From mock response
        
        # Verify database operations were called
        mock_db.commit.assert_called_once()
    
    def test_generate_quiz_empty_topic(self):
        """Test error handling for empty topic"""
        response = client.post("/api/quiz", json={
            "topic": "",
            "question_count": 5,
            "difficulty": "medium"
        })
        
        assert response.status_code == 400
        assert "cannot be empty" in response.json()["detail"]
    
    def test_generate_quiz_invalid_question_count(self):
        """Test error handling for invalid question count"""
        response = client.post("/api/quiz", json={
            "topic": "Science",
            "question_count": 15,  # Over limit
            "difficulty": "medium"
        })
        
        assert response.status_code == 422  # Validation error
    
    @patch('app.api.quiz.get_db')
    def test_submit_quiz_success(self, mock_get_db):
        """Test successful quiz submission"""
        # Mock database session and student
        mock_db = Mock()
        mock_student = Mock()
        mock_student.id = 1
        mock_student.name = "John Doe"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_student
        
        # Mock quiz attempt
        mock_attempt = Mock()
        mock_attempt.id = 1
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Test submission
        response = client.post("/api/quiz/submit", json={
            "quiz_id": "test-quiz-123",
            "student_id": 1,
            "answers": {
                "q_1": "4",
                "q_2": "True"
            },
            "time_taken": 120
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["quiz_id"] == "test-quiz-123"
        assert data["student_id"] == 1
        assert data["total_questions"] == 2
        assert "score" in data
        assert "feedback" in data
    
    @patch('app.api.quiz.get_db')
    def test_submit_quiz_student_not_found(self, mock_get_db):
        """Test quiz submission with non-existent student"""
        # Mock database session with no student found
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = None
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        response = client.post("/api/quiz/submit", json={
            "quiz_id": "test-quiz-123",
            "student_id": 999,
            "answers": {"q_1": "4"}
        })
        
        assert response.status_code == 404
        assert "Student not found" in response.json()["detail"]
    
    @patch('app.api.quiz.get_db')
    def test_get_quiz_history_success(self, mock_get_db):
        """Test getting quiz history for a student"""
        # Mock database session, student, and attempts
        mock_db = Mock()
        mock_student = Mock()
        mock_student.id = 1
        mock_student.name = "John Doe"
        
        mock_attempt = Mock()
        mock_attempt.id = 1
        mock_attempt.score = 85.0
        mock_attempt.completed_at = Mock()
        mock_attempt.completed_at.isoformat.return_value = "2024-01-01T12:00:00"
        mock_attempt.time_taken = 300
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_student
        mock_db.query.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = [mock_attempt]
        
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        response = client.get("/api/quiz/history/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["student_id"] == 1
        assert data["student_name"] == "John Doe"
        assert data["total_attempts"] == 1
        assert len(data["attempts"]) == 1
    
    @patch('app.api.quiz.get_db')
    def test_get_quiz_history_student_not_found(self, mock_get_db):
        """Test getting quiz history for non-existent student"""
        # Mock database session with no student found
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = None
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        response = client.get("/api/quiz/history/999")
        
        assert response.status_code == 404
        assert "Student not found" in response.json()["detail"]
    
    def test_get_question_types(self):
        """Test getting available question types and difficulties"""
        response = client.get("/api/quiz/types")
        
        assert response.status_code == 200
        data = response.json()
        assert "question_types" in data
        assert "difficulties" in data
        
        # Check question types
        question_types = {qt["value"] for qt in data["question_types"]}
        assert question_types == {"multiple_choice", "true_false", "short_answer"}
        
        # Check difficulties
        difficulties = {d["value"] for d in data["difficulties"]}
        assert difficulties == {"easy", "medium", "hard"}
    
    def test_quiz_request_validation(self):
        """Test QuizRequest validation"""
        # Valid request
        valid_request = QuizRequest(
            topic="Mathematics",
            question_count=5,
            difficulty=Difficulty.MEDIUM,
            question_types=[QuestionType.MULTIPLE_CHOICE]
        )
        assert valid_request.topic == "Mathematics"
        assert valid_request.question_count == 5
        
        # Test topic trimming
        request_with_spaces = QuizRequest(
            topic="  Physics  ",
            question_count=3
        )
        assert request_with_spaces.topic == "Physics"
    
    def test_quiz_request_validation_errors(self):
        """Test QuizRequest validation errors"""
        # Empty topic should raise validation error
        with pytest.raises(ValueError, match="Topic cannot be empty"):
            QuizRequest(
                topic="",
                question_count=5
            )
        
        # Empty question types should raise validation error
        with pytest.raises(ValueError, match="At least one question type must be specified"):
            QuizRequest(
                topic="Science",
                question_count=5,
                question_types=[]
            )