# Complete Folder Structure

```
student-learning-buddy/
│
├── backend/                                 # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                         # Application entry point
│   │   ├── config.py                       # Configuration management
│   │   ├── database.py                     # Database setup
│   │   ├── models.py                       # SQLAlchemy models
│   │   ├── schemas.py                      # Pydantic schemas
│   │   ├── dependencies.py                 # FastAPI dependencies
│   │   │
│   │   ├── routers/                        # API Routes
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                     # Authentication endpoints
│   │   │   ├── profile.py                  # Profile management
│   │   │   ├── questions.py                # Question answering
│   │   │   ├── quizzes.py                  # Quiz generation & attempts
│   │   │   ├── notes.py                    # Note summarization
│   │   │   ├── voice.py                    # Voice sessions
│   │   │   └── analytics.py                # User statistics
│   │   │
│   │   └── services/                       # Business Logic
│   │       ├── __init__.py
│   │       ├── auth_service.py             # Authentication logic
│   │       ├── ai_service.py               # Gemini AI integration
│   │       └── file_service.py             # File processing
│   │
│   ├── requirements.txt                    # Python dependencies
│   ├── .env.example                        # Environment template
│   └── .gitignore
│
├── frontend/                                # React Frontend
│   ├── public/
│   │   └── vite.svg
│   │
│   ├── src/
│   │   ├── assets/                         # Static assets
│   │   │
│   │   ├── components/                     # Reusable components
│   │   │   └── Layout.tsx                  # Main layout with nav
│   │   │
│   │   ├── contexts/                       # React Context
│   │   │   └── AuthContext.tsx             # Authentication context
│   │   │
│   │   ├── hooks/                          # Custom React hooks
│   │   │   ├── useAuth.ts                  # Auth hook
│   │   │   ├── useQuestions.ts             # Questions hook
│   │   │   ├── useQuiz.ts                  # Quiz hook
│   │   │   ├── useNotes.ts                 # Notes hook
│   │   │   ├── useVoice.ts                 # Voice hook
│   │   │   └── useProfile.ts               # Profile hook
│   │   │
│   │   ├── lib/                            # Utilities
│   │   │   └── api.ts                      # Axios configuration
│   │   │
│   │   ├── pages/                          # Page components
│   │   │   ├── Login.tsx                   # Login page
│   │   │   ├── Signup.tsx                  # Signup page
│   │   │   ├── Dashboard.tsx               # Dashboard with stats
│   │   │   ├── Questions.tsx               # Ask questions
│   │   │   ├── Quizzes.tsx                 # Quiz generation & taking
│   │   │   ├── Notes.tsx                   # Note summarization
│   │   │   ├── VoiceChat.tsx               # Voice assistant
│   │   │   └── Profile.tsx                 # User profile
│   │   │
│   │   ├── types/                          # TypeScript types
│   │   │   └── index.ts
│   │   │
│   │   ├── App.tsx                         # Main app component
│   │   ├── main.tsx                        # Entry point
│   │   └── index.css                       # Global styles
│   │
│   ├── index.html                          # HTML template
│   ├── package.json                        # Node dependencies
│   ├── tsconfig.json                       # TypeScript config
│   ├── tsconfig.node.json                  # Node TypeScript config
│   ├── vite.config.ts                      # Vite configuration
│   ├── tailwind.config.js                  # Tailwind configuration
│   ├── postcss.config.js                   # PostCSS configuration
│   ├── .env.example                        # Environment template
│   └── .gitignore
│
├── docs/                                    # Documentation
│   ├── PROJECT_ARCHITECTURE.md             # System architecture
│   ├── DATABASE_SCHEMA.md                  # Database design
│   ├── API_ENDPOINTS.md                    # API documentation
│   ├── GEMINI_PROMPTS.md                   # AI prompt templates
│   └── DEPLOYMENT.md                       # Deployment guide
│
├── README.md                                # Project overview
├── FOLDER_STRUCTURE.md                      # This file
├── .gitignore                               # Git ignore rules
└── LICENSE                                  # License file

```

## File Descriptions

### Backend Files

#### Core Application
- **main.py**: FastAPI application initialization, middleware setup, router inclusion
- **config.py**: Environment variable management using Pydantic Settings
- **database.py**: SQLAlchemy engine, session management, database initialization
- **models.py**: Database models (User, Student, Question, Quiz, etc.)
- **schemas.py**: Pydantic models for request/response validation
- **dependencies.py**: Reusable FastAPI dependencies (auth, database)

#### Routers (API Endpoints)
- **auth.py**: POST /auth/signup, POST /auth/login
- **profile.py**: GET/PUT /profile/
- **questions.py**: POST /questions/ask, GET /questions/history
- **quizzes.py**: POST /quizzes/generate, GET /quizzes/, POST /quizzes/attempts
- **notes.py**: POST /notes/summarize, GET /notes/
- **voice.py**: POST /voice/sessions, POST /voice/sessions/{id}/message
- **analytics.py**: GET /analytics/stats

#### Services (Business Logic)
- **auth_service.py**: Password hashing, JWT token generation/verification, user CRUD
- **ai_service.py**: Gemini API integration, prompt management, retry logic
- **file_service.py**: File upload validation, text extraction (PDF, DOCX, TXT)

### Frontend Files

#### Core Application
- **main.tsx**: React application entry point
- **App.tsx**: Router setup, protected routes, authentication flow
- **index.css**: Global styles, Tailwind directives

#### Components
- **Layout.tsx**: Navigation bar, sidebar, main content wrapper

#### Contexts
- **AuthContext.tsx**: Authentication state, login/signup/logout functions

#### Hooks
- **useAuth.ts**: Authentication hook
- **useQuestions.ts**: Question asking and history
- **useQuiz.ts**: Quiz generation and submission
- **useNotes.ts**: Note summarization
- **useVoice.ts**: Voice session management, TTS
- **useProfile.ts**: Profile CRUD operations

#### Pages
- **Login.tsx**: User login form
- **Signup.tsx**: User registration form
- **Dashboard.tsx**: Statistics and recent activity
- **Questions.tsx**: Ask questions interface
- **Quizzes.tsx**: Quiz generation and taking
- **Notes.tsx**: Note summarization interface
- **VoiceChat.tsx**: Voice conversation interface
- **Profile.tsx**: User profile management

#### Library
- **api.ts**: Axios instance with interceptors for auth and error handling

### Configuration Files

#### Backend
- **requirements.txt**: Python package dependencies
- **.env.example**: Environment variable template

#### Frontend
- **package.json**: Node.js dependencies and scripts
- **tsconfig.json**: TypeScript compiler options
- **vite.config.ts**: Vite build tool configuration
- **tailwind.config.js**: Tailwind CSS customization
- **postcss.config.js**: PostCSS plugins

### Documentation
- **PROJECT_ARCHITECTURE.md**: High-level system design
- **DATABASE_SCHEMA.md**: Database tables and relationships
- **API_ENDPOINTS.md**: Complete API reference
- **GEMINI_PROMPTS.md**: AI prompt templates
- **DEPLOYMENT.md**: Production deployment guide
- **README.md**: Project overview and quick start

## Key Design Decisions

### Backend Architecture
1. **Service Layer Pattern**: Separates business logic from API routes
2. **Dependency Injection**: Uses FastAPI's dependency system for auth and database
3. **Pydantic Validation**: Ensures data integrity at API boundaries
4. **Centralized AI Service**: Single point for all Gemini interactions

### Frontend Architecture
1. **Custom Hooks**: Encapsulates API calls and state management
2. **Context API**: Manages global authentication state
3. **Component Composition**: Reusable components for consistency
4. **Type Safety**: TypeScript for compile-time error checking

### Database Design
1. **User Isolation**: All data scoped by user_id
2. **JSON Columns**: Flexible storage for dynamic data
3. **Cascade Deletes**: Automatic cleanup on user deletion
4. **Indexes**: Optimized for common query patterns

### Security
1. **JWT Authentication**: Stateless token-based auth
2. **Password Hashing**: SHA-256 with salt
3. **Input Validation**: Multiple layers of validation
4. **CORS Configuration**: Controlled cross-origin access

## Development Workflow

### Adding a New Feature

1. **Backend**:
   - Add model to `models.py`
   - Create schema in `schemas.py`
   - Implement service in `services/`
   - Create router in `routers/`
   - Include router in `main.py`

2. **Frontend**:
   - Create custom hook in `hooks/`
   - Build page component in `pages/`
   - Add route in `App.tsx`
   - Update navigation in `Layout.tsx`

### Testing Strategy
- Backend: pytest with test database
- Frontend: React Testing Library
- Integration: End-to-end with Playwright
- API: Postman/Thunder Client

### Code Quality
- Backend: Black formatter, flake8 linter
- Frontend: ESLint, Prettier
- Type checking: mypy (Python), tsc (TypeScript)
- Pre-commit hooks: husky, lint-staged
