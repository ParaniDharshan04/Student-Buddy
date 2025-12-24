# API Endpoints Documentation

## Base URL
```
http://localhost:8000
```

## Authentication Endpoints

### POST /auth/signup
Register a new user account.

**Request Body:**
```json
{
  "email": "student@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### POST /auth/login
Login with existing credentials.

**Request Body:**
```json
{
  "email": "student@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Profile Endpoints

### GET /profile/
Get current user's profile.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "full_name": "John Doe",
  "education_level": "High School",
  "grade": "12th",
  "subjects": ["Mathematics", "Physics"],
  "learning_style": "Visual",
  "preferences": {},
  "created_at": "2025-12-23T10:00:00Z",
  "updated_at": "2025-12-23T10:00:00Z"
}
```

### PUT /profile/
Update user profile.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "full_name": "John Doe",
  "education_level": "High School",
  "grade": "12th",
  "subjects": ["Mathematics", "Physics", "Chemistry"],
  "learning_style": "Visual"
}
```

## Question Endpoints

### POST /questions/ask
Ask a question and get AI-powered answer.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "question": "What is photosynthesis?",
  "explanation_type": "simple"
}
```

**Response:**
```json
{
  "id": 1,
  "question_text": "What is photosynthesis?",
  "answer_text": "Photosynthesis is the process by which plants...",
  "explanation_type": "simple",
  "topics": ["Biology", "Plant Science"],
  "concepts": ["Chlorophyll", "Light Energy"],
  "confidence_score": 0.95,
  "created_at": "2025-12-23T10:00:00Z"
}
```

### GET /questions/history
Get question history.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 20)

**Response:**
```json
[
  {
    "id": 1,
    "question_text": "What is photosynthesis?",
    "answer_text": "Photosynthesis is...",
    "explanation_type": "simple",
    "topics": ["Biology"],
    "concepts": ["Chlorophyll"],
    "confidence_score": 0.95,
    "created_at": "2025-12-23T10:00:00Z"
  }
]
```

## Quiz Endpoints

### POST /quizzes/generate
Generate a new quiz.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Form Data:**
- `topic` (optional): Quiz topic text
- `difficulty` (optional): easy, medium, hard (default: medium)
- `question_count` (optional): Number of questions (default: 5)
- `file` (optional): Upload file (PDF, DOCX, TXT)

**Response:**
```json
{
  "id": 1,
  "title": "Python Programming Quiz",
  "topic": "Python Programming",
  "difficulty": "medium",
  "question_count": 5,
  "questions": [
    {
      "id": 1,
      "type": "mcq",
      "question": "What is a list in Python?",
      "options": ["Array", "Collection", "Both", "None"],
      "correct_answer": "Both",
      "explanation": "Lists are ordered collections..."
    }
  ],
  "created_at": "2025-12-23T10:00:00Z"
}
```

### GET /quizzes/
Get all user quizzes.

**Headers:**
```
Authorization: Bearer <token>
```

### POST /quizzes/attempts
Submit quiz attempt.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "quiz_id": 1,
  "answers": [
    {
      "question_id": 1,
      "answer": "Both"
    }
  ],
  "time_taken": 300
}
```

**Response:**
```json
{
  "id": 1,
  "quiz_id": 1,
  "score": 80.0,
  "total_questions": 5,
  "answers": [
    {
      "question_id": 1,
      "user_answer": "Both",
      "correct_answer": "Both",
      "is_correct": true,
      "explanation": "Lists are ordered collections..."
    }
  ],
  "time_taken": 300,
  "created_at": "2025-12-23T10:00:00Z"
}
```

## Notes Endpoints

### POST /notes/summarize
Create note summary.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Form Data:**
- `title` (required): Note title
- `format` (optional): bullet_points, paragraph, outline, key_concepts
- `text_content` (optional): Text to summarize
- `file` (optional): Upload file

**Response:**
```json
{
  "id": 1,
  "title": "Biology Chapter 1",
  "original_text": "Long text...",
  "summary_text": "Summary...",
  "format": "bullet_points",
  "key_terms": ["Cell", "DNA", "Protein"],
  "original_length": 5000,
  "summary_length": 500,
  "created_at": "2025-12-23T10:00:00Z"
}
```

### GET /notes/
Get all user notes.

**Headers:**
```
Authorization: Bearer <token>
```

## Voice Session Endpoints

### POST /voice/sessions
Create new voice session.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "mode": "casual"
}
```

**Response:**
```json
{
  "id": 1,
  "mode": "casual",
  "duration": null,
  "messages": [],
  "feedback": {},
  "created_at": "2025-12-23T10:00:00Z",
  "ended_at": null
}
```

### POST /voice/sessions/{session_id}/message
Send message in voice session.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "content": "Hello, I want to practice my English",
  "mode": "casual"
}
```

**Response:**
```json
{
  "response": "Hello! I'm here to help you practice...",
  "feedback": {
    "fluency_score": 8.5,
    "suggestions": ["Try to speak more naturally"]
  }
}
```

### PUT /voice/sessions/{session_id}/end
End voice session.

**Headers:**
```
Authorization: Bearer <token>
```

## Analytics Endpoints

### GET /analytics/stats
Get user statistics.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "total_questions": 25,
  "total_quizzes": 10,
  "total_quiz_attempts": 15,
  "average_quiz_score": 85.5,
  "total_notes": 8,
  "total_voice_sessions": 5,
  "recent_activity": [
    {
      "type": "question",
      "title": "What is photosynthesis?",
      "timestamp": "2025-12-23T10:00:00Z"
    }
  ]
}
```

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error message description"
}
```

Common HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `500`: Internal Server Error
