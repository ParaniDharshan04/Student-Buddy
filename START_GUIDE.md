# 🚀 How to Start the Application

## Quick Start (Recommended)

### Option 1: Using Batch File (Easiest)
```bash
start_backend.bat
```

### Option 2: Using PowerShell Script
```powershell
.\start_backend.ps1
```

### Option 3: Manual Start
```bash
# Set environment variable first
set GEMINI_API_KEY=AIzaSyBiS_m146g3MVXN2D8VefxvEq8Hk5IBbxA

# Then start backend
python -m uvicorn app.main:app --reload
```

## Start Frontend (In Another Terminal)
```bash
cd frontend
npm run dev
```

## Verify Everything Works

### 1. Check Backend is Running
Open: http://localhost:8000/health

Should show:
```json
{
  "status": "healthy",
  "environment": "development",
  "version": "1.0.0",
  "ai_provider": "Google Gemini"
}
```

### 2. Check API Docs
Open: http://localhost:8000/docs

You should see all the API endpoints.

### 3. Test AI Features
Open: http://localhost:3000

Try:
- ✅ Ask a Question
- ✅ Generate Quiz
- ✅ Summarize Notes
- ✅ Create Profile

## Troubleshooting

### Backend won't start
- Make sure you're in the project root directory
- Check Python is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Frontend won't start
```bash
cd frontend
npm install
npm run dev
```

### AI features not working
- The startup scripts automatically set the API key
- If using manual start, make sure to set the environment variable first

## What the Startup Scripts Do

1. Set the GEMINI_API_KEY environment variable
2. Set other configuration variables
3. Start the uvicorn server with auto-reload

## Success Indicators

✅ Backend terminal shows: "Application startup complete"
✅ Frontend terminal shows: "Local: http://localhost:3000"
✅ Can access http://localhost:8000/health
✅ Can access http://localhost:3000
✅ AI features work (questions, quiz, notes)

## Next Steps

Once both servers are running:
1. Open http://localhost:3000
2. Create your student profile
3. Try asking a question
4. Generate a quiz
5. Summarize some notes

Everything should work now! 🎉
