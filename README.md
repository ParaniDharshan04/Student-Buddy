# 🎓 Student Learning Buddy

An AI-powered personal tutor application that helps students learn, practice, and improve their skills through interactive conversations, quizzes, and voice assistance.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![React](https://img.shields.io/badge/React-18-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)

## ✨ Features

### 🤖 AI-Powered Learning
- **Ask Questions**: Get detailed, step-by-step explanations on any topic
- **Generate Quizzes**: Create custom quizzes with multiple choice, true/false questions
- **Summarize Notes**: Convert long text into concise, organized summaries
- **Voice Assistant**: Practice communication skills with AI conversation partner

### 🎙️ Voice Assistant (NEW!)
- **Three Practice Modes**:
  - 💬 Casual Practice - Improve fluency and confidence
  - 👔 Interview Practice - Prepare for job interviews
  - 🎤 Presentation Practice - Enhance public speaking skills
- Text-to-Speech responses from AI
- Real-time conversation with context awareness
- Feedback and suggestions for improvement

### 👤 User Management
- Secure authentication (signup/login)
- Personal profiles with learning preferences
- Progress tracking and statistics
- Data isolation per user

### 📁 File Upload
- Support for PDF, TXT, and DOCX files
- Extract text for quiz generation or summarization
- Process study materials automatically

### 🎨 Modern UI
- Beautiful black and gold theme
- Responsive design
- Smooth animations
- Intuitive navigation

## 🚀 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **Google Gemini AI** - AI model for responses
- **SQLite** - Database
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **React Router** - Navigation
- **TanStack Query** - Data fetching
- **Web Speech API** - Voice features

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- Google Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/student-learning-buddy.git
cd student-learning-buddy
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Create .env file
copy .env.example .env  # Windows
# cp .env.example .env  # Mac/Linux
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./student_learning_buddy.db
ENVIRONMENT=development
DEBUG=True
```

5. **Initialize database**
```bash
python create_users_table.py
```

6. **Start backend**
```bash
start_backend.bat  # Windows
# uvicorn app.main:app --reload  # Mac/Linux
```

Backend will run on http://localhost:8000

### Frontend Setup

1. **Navigate to frontend**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm run dev
```

Frontend will run on http://localhost:3000

## 🎯 Usage

1. **Sign Up**: Create an account at http://localhost:3000/signup
2. **Login**: Sign in with your credentials
3. **Create Profile**: Set up your learning preferences
4. **Start Learning**:
   - Ask questions on any topic
   - Generate quizzes to test knowledge
   - Summarize study materials
   - Practice communication with Voice Assistant

## 📖 Features Guide

### Ask Questions
- Type any question
- Choose explanation style (Simple, Exam-style, Real-world)
- Get detailed step-by-step answers
- View related topics

### Generate Quiz
- Enter a topic or upload study material
- Select difficulty level
- Choose question types
- Take quiz and get instant feedback

### Summarize Notes
- Paste text or upload document
- Choose summary format (Bullet points, Paragraph, Outline, Key concepts)
- Get concise summary with key terms

### Voice Assistant
- Choose practice mode
- Type your message (or speak if microphone works)
- AI responds with text and voice
- Get feedback and suggestions

## 🗂️ Project Structure

```
student-learning-buddy/
├── app/                      # Backend
│   ├── api/                  # API endpoints
│   ├── models/               # Database models
│   ├── schemas/              # Pydantic schemas
│   ├── services/             # Business logic
│   ├── config.py             # Configuration
│   ├── database.py           # Database setup
│   └── main.py               # FastAPI app
├── frontend/                 # Frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── hooks/            # Custom hooks
│   │   ├── contexts/         # React contexts
│   │   ├── lib/              # Utilities
│   │   └── types/            # TypeScript types
│   └── package.json
├── .env                      # Environment variables (not in git)
├── .gitignore
├── requirements.txt          # Python dependencies
└── README.md
```

## 🔧 Configuration

### Environment Variables

```env
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./student_learning_buddy.db
ENVIRONMENT=development
DEBUG=True
```

### Database Management

**Create tables:**
```bash
python create_users_table.py
```

**Clear all users:**
```bash
python clear_all_users.py
```

**Reset database:**
```bash
python force_recreate_db.py
```

## 🐛 Troubleshooting

### Backend Issues
- **Port 8000 in use**: Change port in `start_backend.bat`
- **Database errors**: Run `python force_recreate_db.py`
- **API key errors**: Check `.env` file has valid Gemini API key

### Frontend Issues
- **Port 3000 in use**: Change port in `vite.config.ts`
- **Build errors**: Delete `node_modules` and run `npm install`
- **API connection**: Ensure backend is running on port 8000

### Voice Assistant Issues
- **Microphone not working**: Use text input instead
- **No voice output**: Check browser volume and permissions
- **Network errors**: Use Chrome or Edge browser

## 📝 API Documentation

Once backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Google Gemini AI** for powering the AI features
- **FastAPI** for the excellent backend framework
- **React** for the frontend library
- **TailwindCSS** for the styling system

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ for students everywhere**
