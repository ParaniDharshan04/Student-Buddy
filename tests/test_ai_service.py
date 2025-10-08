import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.ai_service import AIService
from app.config import settings

class TestAIService:
    
    @pytest.fixture
    def ai_service(self):
        """Create AIService instance for testing"""
        with patch('google.generativeai.configure'):
            with patch('google.generativeai.GenerativeModel') as mock_model:
                mock_model.return_value = Mock()
                return AIService()
    
    @pytest.fixture
    def mock_response(self):
        """Mock Gemini API response"""
        mock_resp = Mock()
        mock_resp.text = "This is a test response with step-by-step explanation.\n1. First step\n2. Second step"
        return mock_resp
    
    @pytest.mark.asyncio
    async def test_answer_question_simple_style(self, ai_service, mock_response):
        """Test answering question with simple explanation style"""
        ai_service.model.generate_content = Mock(return_value=mock_response)
        
        result = await ai_service.answer_question("What is 2+2?", "simple")
        
        assert result["answer"] == mock_response.text
        assert result["style"] == "simple"
        assert len(result["explanation_steps"]) >= 1
        assert result["confidence_score"] > 0
    
    @pytest.mark.asyncio
    async def test_answer_question_exam_style(self, ai_service, mock_response):
        """Test answering question with exam-style explanation"""
        ai_service.model.generate_content = Mock(return_value=mock_response)
        
        result = await ai_service.answer_question("Explain calculus", "exam-style")
        
        assert result["style"] == "exam-style"
        assert "answer" in result
        assert "explanation_steps" in result
    
    @pytest.mark.asyncio
    async def test_answer_question_real_world_style(self, ai_service, mock_response):
        """Test answering question with real-world explanation"""
        ai_service.model.generate_content = Mock(return_value=mock_response)
        
        result = await ai_service.answer_question("How does physics work?", "real-world")
        
        assert result["style"] == "real-world"
        assert isinstance(result["related_topics"], list)
    
    @pytest.mark.asyncio
    async def test_generate_quiz(self, ai_service):
        """Test quiz generation"""
        quiz_response = """Question 1: What is 2+2?
Type: multiple_choice
Options:
A) 3
B) 4
C) 5
D) 6
Correct Answer: B) 4
Explanation: Basic addition

---

Question 2: Is the Earth round?
Type: true_false
Correct Answer: True
Explanation: The Earth is approximately spherical"""
        
        mock_resp = Mock()
        mock_resp.text = quiz_response
        ai_service.model.generate_content = Mock(return_value=mock_resp)
        
        result = await ai_service.generate_quiz("Mathematics", 2, "easy")
        
        assert result["topic"] == "Mathematics"
        assert result["question_count"] >= 1
        assert len(result["questions"]) >= 1
        assert result["estimated_time"] > 0
    
    @pytest.mark.asyncio
    async def test_summarize_notes(self, ai_service, mock_response):
        """Test content summarization"""
        ai_service.model.generate_content = Mock(return_value=mock_response)
        
        content = "This is a long piece of content that needs to be summarized for better understanding."
        result = await ai_service.summarize_notes(content)
        
        assert result["summary"] == mock_response.text
        assert result["original_length"] == len(content)
        assert result["summary_length"] == len(mock_response.text)
        assert isinstance(result["key_terms"], list)
    
    @pytest.mark.asyncio
    async def test_retry_logic_success_on_second_attempt(self, ai_service):
        """Test retry logic when first attempt fails"""
        ai_service.model.generate_content = Mock(side_effect=[
            Exception("API Error"),  # First attempt fails
            Mock(text="Success on retry")  # Second attempt succeeds
        ])
        
        result = await ai_service._make_request_with_retry("test prompt")
        assert result == "Success on retry"
    
    @pytest.mark.asyncio
    async def test_retry_logic_all_attempts_fail(self, ai_service):
        """Test retry logic when all attempts fail"""
        ai_service.model.generate_content = Mock(side_effect=Exception("Persistent API Error"))
        
        with pytest.raises(Exception) as exc_info:
            await ai_service._make_request_with_retry("test prompt")
        
        assert "Failed to get response after" in str(exc_info.value)
    
    def test_get_explanation_prompt_simple(self, ai_service):
        """Test prompt generation for simple style"""
        prompt = ai_service._get_explanation_prompt("What is gravity?", "simple")
        
        assert "What is gravity?" in prompt
        assert "step-by-step" in prompt
        assert "simple language" in prompt
    
    def test_get_explanation_prompt_exam_style(self, ai_service):
        """Test prompt generation for exam style"""
        prompt = ai_service._get_explanation_prompt("Explain photosynthesis", "exam-style")
        
        assert "Explain photosynthesis" in prompt
        assert "exam preparation" in prompt
        assert "formulas" in prompt
    
    def test_get_explanation_prompt_real_world(self, ai_service):
        """Test prompt generation for real-world style"""
        prompt = ai_service._get_explanation_prompt("What is programming?", "real-world")
        
        assert "What is programming?" in prompt
        assert "real-world applications" in prompt
        assert "practical situations" in prompt
    
    def test_parse_quiz_response(self, ai_service):
        """Test parsing of quiz response"""
        response = """Question 1: What is the capital of France?
Type: multiple_choice
A) London
B) Paris
C) Berlin
D) Madrid
Correct Answer: B) Paris
Explanation: Paris is the capital city of France

---

Question 2: Is Python a programming language?
Type: true_false
Correct Answer: True
Explanation: Python is indeed a programming language"""
        
        questions = ai_service._parse_quiz_response(response)
        
        assert len(questions) == 2
        assert questions[0]["question"].strip() == "What is the capital of France?"
        assert questions[0]["type"] == "multiple_choice"
        assert len(questions[0]["options"]) == 4
        assert questions[0]["correct_answer"] == "B) Paris"
        assert questions[1]["type"] == "true_false"
    
    def test_extract_topics(self, ai_service):
        """Test topic extraction from text"""
        text = "This explanation covers mathematics and physics concepts, including chemistry reactions."
        topics = ai_service._extract_topics(text)
        
        assert "Mathematics" in topics
        assert "Physics" in topics
        assert "Chemistry" in topics
        assert len(topics) <= 3
    
    def test_extract_key_terms(self, ai_service):
        """Test key term extraction from text"""
        text = "Photosynthesis is the process by which Green Plants convert Carbon Dioxide into Oxygen using Sunlight."
        key_terms = ai_service._extract_key_terms(text)
        
        assert len(key_terms) <= 5
        assert any(term in ["Photosynthesis", "Green Plants", "Carbon Dioxide", "Oxygen", "Sunlight"] for term in key_terms)