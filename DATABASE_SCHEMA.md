# Database Schema Design

## Entity Relationship Diagram

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ email (UNIQUE)  │
│ password_hash   │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │ 1
         │
         │ 1
┌────────┴────────┐
│    Student      │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │
│ full_name       │
│ education_level │
│ grade           │
│ subjects        │ (JSON)
│ learning_style  │
│ preferences     │ (JSON)
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │ 1
         │
         ├──────────────────┬──────────────────┬──────────────────┐
         │ *                │ *                │ *                │ *
┌────────┴────────┐ ┌───────┴────────┐ ┌──────┴───────┐ ┌───────┴────────┐
│    Question     │ │      Quiz      │ │     Note     │ │  VoiceSession  │
├─────────────────┤ ├────────────────┤ ├──────────────┤ ├────────────────┤
│ id (PK)         │ │ id (PK)        │ │ id (PK)      │ │ id (PK)        │
│ user_id (FK)    │ │ user_id (FK)   │ │ user_id (FK) │ │ user_id (FK)   │
│ question_text   │ │ title          │ │ title        │ │ mode           │
│ answer_text     │ │ topic          │ │ original_text│ │ duration       │
│ explanation_type│ │ difficulty     │ │ summary_text │ │ messages       │ (JSON)
│ topics          │ │ question_count │ │ format       │ │ feedback       │ (JSON)
│ concepts        │ │ questions      │ │ key_terms    │ │ created_at     │
│ confidence      │ │ created_at     │ │ original_len │ │ ended_at       │
│ created_at      │ └────────┬───────┘ │ summary_len  │ └────────────────┘
└─────────────────┘          │ 1       │ created_at   │
                             │         └──────────────┘
                             │ *
                    ┌────────┴────────┐
                    │   QuizAttempt   │
                    ├─────────────────┤
                    │ id (PK)         │
                    │ quiz_id (FK)    │
                    │ user_id (FK)    │
                    │ score           │
                    │ total_questions │
                    │ answers         │ (JSON)
                    │ time_taken      │
                    │ created_at      │
                    └─────────────────┘
```

## Table Definitions

### 1. users
Primary authentication table.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### 2. students
Extended profile and preferences.

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    full_name VARCHAR(255),
    education_level VARCHAR(100),
    grade VARCHAR(50),
    subjects TEXT, -- JSON array
    learning_style VARCHAR(100),
    preferences TEXT, -- JSON object
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_students_user_id ON students(user_id);
```

**subjects JSON format:**
```json
["Mathematics", "Physics", "Computer Science"]
```

**preferences JSON format:**
```json
{
  "default_explanation_style": "simple",
  "default_quiz_difficulty": "medium",
  "default_summary_format": "bullet_points",
  "voice_mode_preference": "casual"
}
```

### 3. questions
Question history with AI responses.

```sql
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    answer_text TEXT NOT NULL,
    explanation_type VARCHAR(50), -- simple, exam, real_world
    topics TEXT, -- JSON array
    concepts TEXT, -- JSON array
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_questions_user_id ON questions(user_id);
CREATE INDEX idx_questions_created_at ON questions(created_at);
```

**topics/concepts JSON format:**
```json
["Algebra", "Quadratic Equations"]
```

### 4. quizzes
Generated quiz templates.

```sql
CREATE TABLE quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    topic TEXT NOT NULL,
    difficulty VARCHAR(50), -- easy, medium, hard
    question_count INTEGER,
    questions TEXT NOT NULL, -- JSON array of question objects
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_quizzes_user_id ON quizzes(user_id);
CREATE INDEX idx_quizzes_created_at ON quizzes(created_at);
```

**questions JSON format:**
```json
[
  {
    "id": 1,
    "type": "mcq",
    "question": "What is 2+2?",
    "options": ["3", "4", "5", "6"],
    "correct_answer": "4",
    "explanation": "Basic addition"
  }
]
```

### 5. quiz_attempts
Student quiz performance tracking.

```sql
CREATE TABLE quiz_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    score FLOAT NOT NULL,
    total_questions INTEGER NOT NULL,
    answers TEXT NOT NULL, -- JSON array
    time_taken INTEGER, -- seconds
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_quiz_attempts_user_id ON quiz_attempts(user_id);
CREATE INDEX idx_quiz_attempts_quiz_id ON quiz_attempts(quiz_id);
CREATE INDEX idx_quiz_attempts_created_at ON quiz_attempts(created_at);
```

**answers JSON format:**
```json
[
  {
    "question_id": 1,
    "user_answer": "4",
    "correct_answer": "4",
    "is_correct": true
  }
]
```

### 6. notes
Note summaries and metadata.

```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    original_text TEXT NOT NULL,
    summary_text TEXT NOT NULL,
    format VARCHAR(50), -- bullet_points, paragraph, outline, key_concepts
    key_terms TEXT, -- JSON array
    original_length INTEGER,
    summary_length INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_notes_user_id ON notes(user_id);
CREATE INDEX idx_notes_created_at ON notes(created_at);
```

**key_terms JSON format:**
```json
["Photosynthesis", "Chlorophyll", "ATP"]
```

### 7. voice_sessions
Voice conversation history.

```sql
CREATE TABLE voice_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    mode VARCHAR(50), -- casual, interview, presentation
    duration INTEGER, -- seconds
    messages TEXT NOT NULL, -- JSON array of conversation
    feedback TEXT, -- JSON object
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_voice_sessions_user_id ON voice_sessions(user_id);
CREATE INDEX idx_voice_sessions_created_at ON voice_sessions(created_at);
```

**messages JSON format:**
```json
[
  {
    "role": "user",
    "content": "Hello, I want to practice my presentation skills",
    "timestamp": "2025-12-23T10:30:00Z"
  },
  {
    "role": "assistant",
    "content": "Great! Let's work on your presentation skills...",
    "timestamp": "2025-12-23T10:30:05Z"
  }
]
```

**feedback JSON format:**
```json
{
  "fluency_score": 8.5,
  "confidence_score": 7.0,
  "suggestions": [
    "Try to reduce filler words",
    "Maintain eye contact"
  ],
  "strengths": [
    "Clear articulation",
    "Good pacing"
  ]
}
```

## Data Isolation & Security

### User Data Isolation
- All queries MUST filter by `user_id`
- No cross-user data access
- Cascade deletes on user removal

### Indexes
- Optimized for user-scoped queries
- Timestamp indexes for analytics
- Foreign key indexes for joins

## Migration Strategy

### SQLite → PostgreSQL
1. Change `INTEGER PRIMARY KEY AUTOINCREMENT` → `SERIAL PRIMARY KEY`
2. Change `TEXT` → `JSONB` for JSON columns
3. Add connection pooling
4. Add read replicas for analytics

### Future Enhancements
- Add `deleted_at` for soft deletes
- Add `version` for optimistic locking
- Add audit tables for compliance
- Partition large tables by date
