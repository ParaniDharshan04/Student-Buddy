# Student Learning Buddy 🎓

An AI-powered educational platform that acts as a 24/7 personal tutor for students, featuring question answering, quiz generation, note summarization, and voice-based communication practice powered by Google Gemini AI.

## Features

### 🤖 AI Question Answering
- Natural language question input
- Three explanation styles: Simple, Exam-oriented, Real-world application
- Topic and concept extraction
- Confidence scoring
- Complete question history

### 📝 AI Quiz Generation
- Generate quizzes from topics or uploaded files (PDF, DOCX, TXT)
- Customizable difficulty levels (Easy, Medium, Hard)
- Multiple question types (MCQ, True/False, Short Answer)
- Auto-grading with detailed explanations
- Performance tracking and analytics

### 📚 Note Summarization
- Text and file upload support
- Four summary formats: Bullet points, Paragraph, Outline, Key concepts
- Key term extraction
- Length comparison metrics
- Summary history

### 🎤 Voice Assistant
- Three conversation modes:
  - **Casual Mode**: Fluency and confidence building
  - **Interview Mode**: Mock interviews with STAR feedback
  - **Presentation Mode**: Public speaking coaching
- Text-to-Speech integration
- Context-aware conversations
- Session feedback and improvement suggestions

### 👤 User Management
- Secure authentication (JWT tokens)
- Password hashing (SHA-256)
- Student profile customization
- Learning preferences
- Progress analytics dashboard

## Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Database**: SQLite (dev), PostgreSQL (prod-ready)
- **ORM**: SQLAlchemy 2.0+
- **Validation**: Pydantic v2
- **AI**: Google Gemini API
- **Authentication**: JWT (python-jose)
- **File Processing**: PyPDF2, python-docx

### Frontend
- **Framework**: React 18+ with TypeScript
- **Routing**: React Router v6
- **Styling**: TailwindCSS (Black & Gold theme)
- **State Management**: Context API
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Voice**: Web Speech API

## Project Structure

```
student-learning-buddy/
├── backend/
│   ├── app/
│   │   ├── routers/          # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── profile.py
│   │   │   ├── questions.py
│   │   │   ├── quizzes.py
│   │   │   ├── notes.py
│   │   │   ├── voice.py
│   │   │   └── analytics.py
│   │   ├── services/         # Business logic
│   │   │   ├── auth_service.py
│   │   │   ├── ai_service.py
│   │   │   └── file_service.py
│   │   ├── models.py         # Database models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── database.py       # Database config
│   │   ├── config.py         # App configuration
│   │   ├── dependencies.py   # FastAPI dependencies
│   │   └── main.py           # Application entry
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── pages/            # React pages
│   │   │   ├── Login.tsx
│   │   │   ├── Signup.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Questions.tsx
│   │   │   ├── Quizzes.tsx
│   │   │   ├── Notes.tsx
│   │   │   ├── VoiceChat.tsx
│   │   │   └── Profile.tsx
│   │   ├── components/       # Reusable components
│   │   │   └── Layout.tsx
│   │   ├── contexts/         # React contexts
│   │   │   └── AuthContext.tsx
│   │   ├── hooks/            # Custom hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useQuestions.ts
│   │   │   ├── useQuiz.ts
│   │   │   ├── useNotes.ts
│   │   │   ├── useVoice.ts
│   │   │   └── useProfile.ts
│   │   ├── lib/
│   │   │   └── api.ts        # Axios configuration
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
└── docs/
    ├── PROJECT_ARCHITECTURE.md
    ├── DATABASE_SCHEMA.md
    ├── API_ENDPOINTS.md
    ├── GEMINI_PROMPTS.md
    └── DEPLOYMENT.md
```

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Google Gemini API key

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

5. **Run the server**
```bash
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment**
```bash
cp .env.example .env
```

4. **Run development server**
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## API Documentation

Complete API documentation is available at:
- Interactive docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Markdown: [API_ENDPOINTS.md](API_ENDPOINTS.md)

## Database Schema

Detailed database schema documentation: [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)

### Key Tables
- `users` - Authentication
- `students` - Profile & preferences
- `questions` - Question history
- `quizzes` - Generated quizzes
- `quiz_attempts` - Quiz performance
- `notes` - Note summaries
- `voice_sessions` - Voice conversations

## Architecture

Comprehensive architecture documentation: [PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md)

### Design Principles
- **Separation of Concerns**: Routes, Services, Models, Schemas
- **Security First**: JWT auth, password hashing, input validation
- **Scalability**: Service layer abstraction, async operations
- **User Experience**: Responsive design, real-time feedback

## AI Integration

Google Gemini prompt templates: [GEMINI_PROMPTS.md](GEMINI_PROMPTS.md)

### Features
- Centralized AI service
- Retry logic with exponential backoff
- Context-aware conversations
- Structured output parsing
- Token management

## Deployment

Production deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)

### Deployment Options
- Traditional server (Nginx + Systemd)
- Docker containers
- Cloud platforms (Heroku, AWS, GCP)

## Security Features

- JWT token-based authentication
- SHA-256 password hashing with salt
- Input validation at every layer
- SQL injection prevention (ORM)
- XSS prevention (React)
- CORS configuration
- User data isolation
- Secure file uploads

## Analytics & Tracking

- Questions asked
- Quizzes taken and scores
- Average performance
- Voice session duration
- Note summaries created
- Recent activity timeline

## Future Enhancements

### Phase 2
- Real-time collaboration
- Study groups
- Gamification (badges, leaderboards)
- Mobile app (React Native)
- Offline mode

### Phase 3
- Advanced analytics dashboard
- Teacher/parent portal
- Custom learning paths
- Integration with LMS
- Multi-language support

### Scalability
- PostgreSQL with connection pooling
- Redis for caching
- Celery for async tasks
- S3 for file storage
- Microservices architecture

## Contributing

This is a final-year engineering project. Contributions, suggestions, and feedback are welcome!

## License

This project is developed for educational purposes.

## Contact

For questions or collaboration:
- Project showcase: [LinkedIn Profile]
- Documentation: See `/docs` folder

## Acknowledgments

- Google Gemini AI for powering the intelligent features
- FastAPI for the excellent backend framework
- React and TailwindCSS for the modern frontend
- Open-source community for amazing tools

---

**Built with ❤️ for students, by students**
