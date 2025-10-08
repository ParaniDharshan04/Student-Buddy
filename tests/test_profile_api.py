import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app
from app.schemas.profile import ProfileCreateRequest, LearningStyle
from app.models import Student
from datetime import datetime

client = TestClient(app)

class TestProfileAPI:
    
    @pytest.fixture
    def mock_student(self):
        """Mock Student object"""
        student = Mock(spec=Student)
        student.id = 1
        student.name = "John Doe"
        student.email = "john@example.com"
        student.subjects_list = ["Mathematics", "Physics"]
        student.learning_style = "visual"
        student.last_studied_topic = "Calculus"
        student.created_at = datetime(2024, 1, 1, 12, 0, 0)
        student.updated_at = datetime(2024, 1, 1, 12, 0, 0)
        return student
    
    @patch('app.api.profile.profile_service.create_student_profile')
    @patch('app.api.profile.get_db')
    def test_create_profile_success(self, mock_get_db, mock_create_profile, mock_student):
        """Test successful profile creation"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock profile service
        mock_create_profile.return_value = mock_student
        
        # Test request
        response = client.post("/api/profile", json={
            "name": "John Doe",
            "email": "john@example.com",
            "preferred_subjects": ["Mathematics", "Physics"],
            "learning_style": "visual"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert data["preferred_subjects"] == ["Mathematics", "Physics"]
        assert data["learning_style"] == "visual"
    
    @patch('app.api.profile.profile_service.create_student_profile')
    @patch('app.api.profile.get_db')
    def test_create_profile_duplicate_email(self, mock_get_db, mock_create_profile):
        """Test profile creation with duplicate email"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock profile service to raise ValueError
        mock_create_profile.side_effect = ValueError("Student with email john@example.com already exists")
        
        response = client.post("/api/profile", json={
            "name": "John Doe",
            "email": "john@example.com"
        })
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
    
    def test_create_profile_invalid_data(self):
        """Test profile creation with invalid data"""
        # Empty name
        response = client.post("/api/profile", json={
            "name": "",
            "email": "john@example.com"
        })
        assert response.status_code == 422
        
        # Invalid email
        response = client.post("/api/profile", json={
            "name": "John Doe",
            "email": "invalid-email"
        })
        assert response.status_code == 422
    
    @patch('app.api.profile.profile_service.get_student_profile')
    @patch('app.api.profile.get_db')
    def test_get_profile_success(self, mock_get_db, mock_get_profile, mock_student):
        """Test successful profile retrieval"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock profile service
        mock_get_profile.return_value = mock_student
        
        response = client.get("/api/profile/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
    
    @patch('app.api.profile.profile_service.get_student_profile')
    @patch('app.api.profile.get_db')
    def test_get_profile_not_found(self, mock_get_db, mock_get_profile):
        """Test profile retrieval for non-existent student"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock profile service to return None
        mock_get_profile.return_value = None
        
        response = client.get("/api/profile/999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    @patch('app.api.profile.profile_service.update_student_profile')
    @patch('app.api.profile.get_db')
    def test_update_profile_success(self, mock_get_db, mock_update_profile, mock_student):
        """Test successful profile update"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Update mock student
        updated_student = mock_student
        updated_student.name = "Jane Doe"
        updated_student.learning_style = "auditory"
        
        # Mock profile service
        mock_update_profile.return_value = updated_student
        
        response = client.put("/api/profile/1", json={
            "name": "Jane Doe",
            "learning_style": "auditory"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Jane Doe"
        assert data["learning_style"] == "auditory"
    
    @patch('app.api.profile.profile_service.update_student_profile')
    @patch('app.api.profile.get_db')
    def test_update_profile_not_found(self, mock_get_db, mock_update_profile):
        """Test profile update for non-existent student"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock profile service to return None
        mock_update_profile.return_value = None
        
        response = client.put("/api/profile/999", json={
            "name": "Jane Doe"
        })
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    @patch('app.api.profile.profile_service.delete_student_profile')
    @patch('app.api.profile.get_db')
    def test_delete_profile_success(self, mock_get_db, mock_delete_profile):
        """Test successful profile deletion"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock profile service
        mock_delete_profile.return_value = True
        
        response = client.delete("/api/profile/1")
        
        assert response.status_code == 204
    
    @patch('app.api.profile.profile_service.delete_student_profile')
    @patch('app.api.profile.get_db')
    def test_delete_profile_not_found(self, mock_get_db, mock_delete_profile):
        """Test profile deletion for non-existent student"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock profile service
        mock_delete_profile.return_value = False
        
        response = client.delete("/api/profile/999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    @patch('app.api.profile.profile_service.get_student_stats')
    @patch('app.api.profile.profile_service.get_student_profile')
    @patch('app.api.profile.get_db')
    def test_get_profile_with_stats(self, mock_get_db, mock_get_profile, mock_get_stats, mock_student):
        """Test getting profile with statistics"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock profile service
        mock_get_profile.return_value = mock_student
        
        # Mock stats
        mock_stats = Mock()
        mock_stats.total_questions_asked = 10
        mock_stats.total_quizzes_taken = 5
        mock_stats.total_notes_summarized = 3
        mock_stats.average_quiz_score = 85.5
        mock_stats.most_studied_topics = ["Mathematics", "Physics"]
        mock_stats.learning_streak = 7
        mock_stats.total_study_time = 120
        mock_get_stats.return_value = mock_stats
        
        response = client.get("/api/profile/1/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["stats"]["total_questions_asked"] == 10
        assert data["stats"]["average_quiz_score"] == 85.5
        assert data["stats"]["learning_streak"] == 7
    
    @patch('app.api.profile.profile_service.get_all_students')
    @patch('app.api.profile.get_db')
    def test_list_profiles(self, mock_get_db, mock_get_all_students, mock_student):
        """Test listing all profiles"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock profile service
        mock_get_all_students.return_value = [mock_student]
        
        response = client.get("/api/profiles")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == 1
        assert data[0]["name"] == "John Doe"
    
    @patch('app.api.profile.profile_service.search_students')
    @patch('app.api.profile.get_db')
    def test_search_profiles(self, mock_get_db, mock_search_students, mock_student):
        """Test searching profiles"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock profile service
        mock_search_students.return_value = [mock_student]
        
        response = client.get("/api/profiles/search?q=John")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "John Doe"
    
    @patch('app.api.profile.profile_service.get_student_by_email')
    @patch('app.api.profile.get_db')
    def test_get_profile_by_email(self, mock_get_db, mock_get_by_email, mock_student):
        """Test getting profile by email"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock profile service
        mock_get_by_email.return_value = mock_student
        
        response = client.get("/api/profile/email/john@example.com")
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "john@example.com"
        assert data["name"] == "John Doe"
    
    def test_get_learning_styles(self):
        """Test getting available learning styles"""
        response = client.get("/api/profile/learning-styles")
        
        assert response.status_code == 200
        data = response.json()
        assert "learning_styles" in data
        assert len(data["learning_styles"]) == 5
        
        styles = {style["value"] for style in data["learning_styles"]}
        assert styles == {"visual", "auditory", "kinesthetic", "reading_writing", "mixed"}
    
    def test_profile_create_request_validation(self):
        """Test ProfileCreateRequest validation"""
        # Valid request
        valid_request = ProfileCreateRequest(
            name="John Doe",
            email="john@example.com",
            preferred_subjects=["Math", "Science"],
            learning_style=LearningStyle.VISUAL
        )
        assert valid_request.name == "John Doe"
        assert valid_request.preferred_subjects == ["Math", "Science"]
        
        # Test name trimming
        request_with_spaces = ProfileCreateRequest(
            name="  Jane Doe  "
        )
        assert request_with_spaces.name == "Jane Doe"
    
    def test_profile_create_request_validation_errors(self):
        """Test ProfileCreateRequest validation errors"""
        # Empty name should raise validation error
        with pytest.raises(ValueError, match="Name cannot be empty"):
            ProfileCreateRequest(name="")
        
        # Whitespace-only name should raise validation error
        with pytest.raises(ValueError, match="Name cannot be empty"):
            ProfileCreateRequest(name="   ")