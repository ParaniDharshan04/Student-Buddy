# Student Learning Buddy - System Architecture

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer (React)                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │   Auth   │ │ Questions│ │  Quizzes │ │ Voice Chat   │  │
│  │   Pages  │ │   Page   │ │   Page   │ │    Page      │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │  Notes   │ │ Profile  │ │Dashboard │ │   Context    │  │
│  │  Page    │ │   Page   │ │   Page   │ │   Providers  │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│                   API Layer (FastAPI)                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │   Auth   │ │Questions │ │  Quizzes │ │    Voice     │  │
│  │  Routes  │ │  Routes  │ │  Routes  │ │   Routes     │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                   │
│  │  Notes   │ │ Profile  │ │Analytics │                   │
│  │  Routes  │ │  Routes  │ │  Routes  │                   │
│  └──────────┘ └──────────┘ └──────────┘                   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                   Service Layer                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │   Auth   │ │   AI     │ │   Quiz   │ │    Voice     │  │
│  │ Service  │ │ Service  │ │ Service  │ │   Service    │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                   │
│  │   File   │ │ Profile  │ │Analytics │                   │
│  │ Service  │ │ Service  │ │ Service  │                   │
│  └──────────┘ └──────────┘ └──────────┘                   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│              Data Access Layer (SQLAlchemy)                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │   User   │ │ Student  │ │Question  │ │     Quiz     │  │
│  │  Model   │ │  Model   │ │  Model   │ │    Model     │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                   │
│  │   Note   │ │  Voice   │ │  Quiz    │                   │
│  │  Model   │ │ Session  │ │ Attempt  │                   │
│  └──────────┘ └──────────┘ └──────────┘                   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  Database (SQLite)                           │
│              (Migration-ready for PostgreSQL)                │
└─────────────────────────────────────────────────────────────┘

                External Services
┌─────────────────────────────────────────────────────────────┐
│                   Google Gemini API                          │
│  • Question Answering    • Quiz Generation                   │
│  • Note Summarization    • Voice Conversation                │
└─────────────────────────────────────────────────────────────┘
```

## 2. Design Principles

### Separation of Concerns
- **Routes**: Handle HTTP, validation, auth
- **Services**: Business logic, AI integration
- **Models**: Data structure, relationships
- **Schemas**: Request/response validation

### Security First
- Token-based authentication (JWT)
- Password hashing (SHA-256 + salt)
- Input validation at every layer
- User data isolation
- CORS configuration

### Scalability
- Async AI calls
- Service layer abstraction
- Database migration ready
- Stateless API design
- Centralized configuration

### User Experience
- Responsive design
- Real-time feedback
- Error handling
- Loading states
- Accessibility compliance

## 3. Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0+
- **Validation**: Pydantic v2
- **Database**: SQLite (dev), PostgreSQL (prod)
- **AI**: Google Gemini API
- **Auth**: JWT tokens
- **File Processing**: PyPDF2, python-docx

### Frontend
- **Framework**: React 18+ with TypeScript
- **Routing**: React Router v6
- **Styling**: TailwindCSS
- **State**: Context API + Custom Hooks
- **HTTP**: Axios
- **Voice**: Web Speech API

## 4. Data Flow Examples

### Question Answering Flow
```
User Input → Frontend Validation → API Request → Auth Middleware
→ Question Service → AI Service (Gemini) → Parse Response
→ Save to DB → Return to Frontend → Display Answer
```

### Quiz Generation Flow
```
Topic/File Upload → File Service (extract text) → Quiz Service
→ AI Service (generate questions) → Validate Format
→ Save Quiz → Return to Frontend → Interactive UI
```

### Voice Session Flow
```
User Speech → Web Speech API → Text → Voice Service
→ AI Service (conversation) → Response Text
→ TTS → Audio Output → Save Session History
```

## 5. Security Architecture

### Authentication Flow
1. User registers → Hash password → Store user
2. User logs in → Verify password → Generate JWT
3. Protected routes → Verify JWT → Extract user_id
4. All operations → User isolation check

### Data Protection
- All user data scoped by user_id
- No cross-user data access
- Input sanitization
- SQL injection prevention (ORM)
- XSS prevention (React)

## 6. AI Integration Strategy

### Centralized AI Service
- Single point for all Gemini calls
- Retry logic with exponential backoff
- Error handling and fallbacks
- Token usage tracking
- Rate limiting awareness

### Prompt Engineering
- Mode-specific system prompts
- Context injection
- Structured output requests
- Temperature control per feature
- Clean response formatting

## 7. Scalability Considerations

### Current Design (MVP)
- SQLite database
- Synchronous file processing
- In-memory session state

### Future Enhancements
- PostgreSQL with connection pooling
- Redis for caching and sessions
- Celery for async tasks
- S3 for file storage
- Load balancing
- Microservices architecture
