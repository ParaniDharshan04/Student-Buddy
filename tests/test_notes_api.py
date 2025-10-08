import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from app.main import app
from app.schemas.notes import NotesRequest, SummaryFormat

client = TestClient(app)

class TestNotesAPI:
    
    @pytest.fixture
    def mock_notes_response(self):
        """Mock notes service response"""
        return {
            "summary": "• Key point 1: Important concept\n• Key point 2: Another concept\n• Key point 3: Final point",
            "format": "bullet_points",
            "original_length": 500,
            "summary_length": 85,
            "compression_ratio": 0.17,
            "key_terms": ["Important", "Concept", "Analysis"],
            "main_topics": ["Science", "Research"],
            "reading_time": 1
        }
    
    @patch('app.api.notes.notes_service.summarize_content')
    @patch('app.api.notes.get_db')
    def test_summarize_notes_success(self, mock_get_db, mock_summarize, mock_notes_response):
        """Test successful notes summarization"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock notes service
        mock_summarize.return_value = mock_notes_response
        
        # Test request
        response = client.post("/api/notes", json={
            "content": "This is a long piece of content that needs to be summarized for better understanding and study purposes.",
            "format": "bullet_points"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["summary"] == mock_notes_response["summary"]
        assert data["format"] == "bullet_points"
        assert data["original_length"] == 500
        assert data["compression_ratio"] == 0.17
        assert len(data["key_terms"]) == 3
    
    @patch('app.api.notes.notes_service.summarize_content')
    @patch('app.api.notes.get_db')
    def test_summarize_notes_with_student_id(self, mock_get_db, mock_summarize, mock_notes_response):
        """Test notes summarization with student ID"""
        # Mock database session and student
        mock_db = Mock()
        mock_student = Mock()
        mock_student.id = 1
        mock_db.query.return_value.filter.return_value.first.return_value = mock_student
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock notes service
        mock_summarize.return_value = mock_notes_response
        
        # Test request with student ID
        response = client.post("/api/notes", json={
            "content": "Detailed content about photosynthesis and plant biology that needs summarization.",
            "format": "paragraph",
            "topic": "Biology",
            "student_id": 1
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["summary"] == mock_notes_response["summary"]
        
        # Verify database operations were called
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
    
    def test_summarize_notes_empty_content(self):
        """Test error handling for empty content"""
        response = client.post("/api/notes", json={
            "content": "",
            "format": "bullet_points"
        })
        
        assert response.status_code == 400
        assert "cannot be empty" in response.json()["detail"]
    
    def test_summarize_notes_content_too_short(self):
        """Test error handling for content that's too short"""
        response = client.post("/api/notes", json={
            "content": "Short",
            "format": "bullet_points"
        })
        
        assert response.status_code == 400
        assert "at least 10 characters" in response.json()["detail"]
    
    def test_summarize_notes_invalid_format(self):
        """Test error handling for invalid format"""
        response = client.post("/api/notes", json={
            "content": "This is valid content that is long enough to be summarized properly.",
            "format": "invalid_format"
        })
        
        assert response.status_code == 422  # Validation error
    
    @patch('app.api.notes.notes_service.summarize_content')
    @patch('app.api.notes.get_db')
    def test_summarize_notes_service_error(self, mock_get_db, mock_summarize):
        """Test error handling when notes service fails"""
        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        # Mock notes service to raise exception
        mock_summarize.side_effect = Exception("Notes service error")
        
        response = client.post("/api/notes", json={
            "content": "This is content that will cause the service to fail during processing.",
            "format": "bullet_points"
        })
        
        assert response.status_code == 500
        assert "Failed to summarize content" in response.json()["detail"]
    
    def test_get_summary_formats(self):
        """Test getting available summary formats"""
        response = client.get("/api/notes/formats")
        
        assert response.status_code == 200
        data = response.json()
        assert "formats" in data
        assert len(data["formats"]) == 4
        
        formats = {f["value"] for f in data["formats"]}
        assert formats == {"bullet_points", "paragraph", "outline", "key_concepts"}
    
    @patch('app.api.notes.get_db')
    def test_get_notes_history_success(self, mock_get_db):
        """Test getting notes history for a student"""
        # Mock database session, student, and sessions
        mock_db = Mock()
        mock_student = Mock()
        mock_student.id = 1
        mock_student.name = "John Doe"
        
        mock_session = Mock()
        mock_session.id = 1
        mock_session.topic = "Biology"
        mock_session.created_at = Mock()
        mock_session.created_at.isoformat.return_value = "2024-01-01T12:00:00"
        mock_session.metadata_dict = {
            "format": "bullet_points",
            "original_length": 1000,
            "summary_length": 200,
            "compression_ratio": 0.2,
            "key_terms": ["Biology", "Cell"],
            "main_topics": ["Science"]
        }
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_student
        mock_db.query.return_value.filter.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = [mock_session]
        
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        response = client.get("/api/notes/history/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["student_id"] == 1
        assert data["student_name"] == "John Doe"
        assert data["total_sessions"] == 1
        assert len(data["sessions"]) == 1
    
    @patch('app.api.notes.get_db')
    def test_get_notes_history_student_not_found(self, mock_get_db):
        """Test getting notes history for non-existent student"""
        # Mock database session with no student found
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = None
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        response = client.get("/api/notes/history/999")
        
        assert response.status_code == 404
        assert "Student not found" in response.json()["detail"]
    
    @patch('app.api.notes.get_db')
    def test_get_notes_session_success(self, mock_get_db):
        """Test getting specific notes session"""
        # Mock database session and notes session
        mock_db = Mock()
        mock_session = Mock()
        mock_session.id = 1
        mock_session.student_id = 1
        mock_session.topic = "Chemistry"
        mock_session.created_at = Mock()
        mock_session.created_at.isoformat.return_value = "2024-01-01T12:00:00"
        mock_session.content = "Original content..."
        mock_session.ai_response = "Summarized content..."
        mock_session.metadata_dict = {
            "format": "paragraph",
            "original_length": 800,
            "summary_length": 150
        }
        
        mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = mock_session
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        response = client.get("/api/notes/session/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == 1
        assert data["student_id"] == 1
        assert data["topic"] == "Chemistry"
        assert data["original_content"] == "Original content..."
        assert data["summary"] == "Summarized content..."
    
    @patch('app.api.notes.get_db')
    def test_get_notes_session_not_found(self, mock_get_db):
        """Test getting non-existent notes session"""
        # Mock database session with no session found
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = None
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_get_db.return_value.__exit__.return_value = None
        
        response = client.get("/api/notes/session/999")
        
        assert response.status_code == 404
        assert "Notes session not found" in response.json()["detail"]
    
    def test_notes_request_validation(self):
        """Test NotesRequest validation"""
        # Valid request
        valid_request = NotesRequest(
            content="This is a valid piece of content that is long enough to be summarized.",
            format=SummaryFormat.BULLET_POINTS
        )
        assert valid_request.content.startswith("This is a valid")
        assert valid_request.format == SummaryFormat.BULLET_POINTS
        
        # Test content cleaning (multiple spaces)
        request_with_spaces = NotesRequest(
            content="This   has    multiple    spaces   between   words.",
            format=SummaryFormat.PARAGRAPH
        )
        assert "multiple    spaces" not in request_with_spaces.content
    
    def test_notes_request_validation_errors(self):
        """Test NotesRequest validation errors"""
        # Empty content should raise validation error
        with pytest.raises(ValueError, match="Content cannot be empty"):
            NotesRequest(
                content="",
                format=SummaryFormat.BULLET_POINTS
            )
        
        # Content too short should pass validation (handled at API level)
        short_request = NotesRequest(
            content="Short text",
            format=SummaryFormat.BULLET_POINTS
        )
        assert short_request.content == "Short text"