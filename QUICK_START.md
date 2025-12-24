# Quick Start Guide

Get Student Learning Buddy running in 5 minutes!

## Prerequisites

Before you begin, ensure you have:
- ✅ Python 3.9 or higher
- ✅ Node.js 18 or higher
- ✅ Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## Option 1: Automated Setup (Recommended)

### Linux/Mac

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### Windows

```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then run
.\setup.ps1
```

The script will:
1. Create Python virtual environment
2. Install backend dependencies
3. Install frontend dependencies
4. Create .env files
5. Initialize database

## Option 2: Manual Setup

### Step 1: Backend Setup (5 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your-api-key-here

# Initialize database
python -c "from app.database import init_db; init_db()"
```

### Step 2: Frontend Setup (3 minutes)

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env
```

### Step 3: Run the Application (1 minute)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Access the Application

- 🌐 **Frontend**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs

## First Steps

### 1. Create an Account
- Navigate to http://localhost:3000
- Click "Sign up"
- Enter email and password (min 6 characters)
- You'll be automatically logged in

### 2. Complete Your Profile
- Click on the profile icon (top right)
- Fill in your details:
  - Full name
  - Education level
  - Grade
  - Learning style
- Click "Save"

### 3. Try the Features

#### Ask a Question
1. Go to "Questions" page
2. Type your question (e.g., "What is photosynthesis?")
3. Select explanation style
4. Click "Ask Question"
5. View the AI-generated answer

#### Generate a Quiz
1. Go to "Quizzes" page
2. Enter a topic (e.g., "Python Programming")
3. Select difficulty and question count
4. Click "Generate Quiz"
5. Answer the questions
6. Submit and view your score

#### Summarize Notes
1. Go to "Notes" page
2. Enter a title
3. Paste text or upload a file
4. Select summary format
5. Click "Generate Summary"
6. View the summarized content

#### Practice with Voice
1. Go to "Voice Chat" page
2. Select a mode (Casual, Interview, or Presentation)
3. Click "Start Session"
4. Type your message
5. Receive AI response with feedback

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError`
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

**Problem**: Database errors
```bash
# Solution: Reinitialize database
python -c "from app.database import init_db; init_db()"
```

**Problem**: Gemini API errors
```bash
# Solution: Check your API key in .env
# Verify at: https://makersuite.google.com/app/apikey
```

### Frontend Issues

**Problem**: `npm install` fails
```bash
# Solution: Clear cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Problem**: API connection errors
```bash
# Solution: Verify backend is running
# Check: http://localhost:8000/health
```

**Problem**: Build errors
```bash
# Solution: Clear build cache
rm -rf node_modules/.vite
npm run dev
```

### Common Issues

**CORS Errors**
- Ensure CORS_ORIGINS in backend/.env includes frontend URL
- Default: `http://localhost:3000,http://localhost:5173`

**Port Already in Use**
```bash
# Backend (port 8000)
uvicorn app.main:app --reload --port 8001

# Frontend (port 3000)
npm run dev -- --port 3001
```

## Environment Variables

### Backend (.env)
```env
# Required
GEMINI_API_KEY=your-api-key-here
SECRET_KEY=your-secret-key-here

# Optional (defaults provided)
DATABASE_URL=sqlite:///./student_buddy.db
DEBUG=True
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend (.env)
```env
# Optional (defaults to localhost:8000)
VITE_API_URL=http://localhost:8000
```

## Testing the Setup

### Backend Health Check
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

### API Documentation
Visit: http://localhost:8000/docs
- Try the "GET /health" endpoint
- Should return 200 OK

### Frontend Check
Visit: http://localhost:3000
- Should see login page
- No console errors

## Next Steps

1. **Explore Features**: Try all the main features
2. **Read Documentation**: Check out the docs folder
3. **Customize**: Modify colors, add features
4. **Deploy**: Follow DEPLOYMENT.md for production

## Getting Help

### Documentation
- 📖 [README.md](README.md) - Project overview
- 🏗️ [PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) - System design
- 🗄️ [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) - Database structure
- 🔌 [API_ENDPOINTS.md](API_ENDPOINTS.md) - API reference
- 🤖 [GEMINI_PROMPTS.md](GEMINI_PROMPTS.md) - AI prompts
- 🚀 [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide

### Common Commands

**Backend**
```bash
# Start server
uvicorn app.main:app --reload

# Start with different port
uvicorn app.main:app --reload --port 8001

# View logs
# Logs appear in terminal
```

**Frontend**
```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

**Database**
```bash
# Initialize
python -c "from app.database import init_db; init_db()"

# Reset (delete and recreate)
rm student_buddy.db
python -c "from app.database import init_db; init_db()"
```

## Development Tips

### Hot Reload
- Backend: Automatically reloads on file changes
- Frontend: Automatically reloads on file changes

### API Testing
- Use the Swagger UI: http://localhost:8000/docs
- Or use tools like Postman, Thunder Client

### Debugging
- Backend: Add `print()` statements or use debugger
- Frontend: Use browser DevTools (F12)

### Code Formatting
```bash
# Backend (optional)
pip install black
black app/

# Frontend (optional)
npm install -D prettier
npx prettier --write src/
```

## Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can access API docs
- [ ] Can create account
- [ ] Can log in
- [ ] Can ask questions
- [ ] Can generate quizzes
- [ ] Can create summaries
- [ ] Can use voice chat
- [ ] Can update profile
- [ ] Dashboard shows stats

## Ready to Go! 🚀

You're all set! Start exploring the features and building your learning journey.

For detailed information about each feature, check the main [README.md](README.md).

Happy learning! 🎓
