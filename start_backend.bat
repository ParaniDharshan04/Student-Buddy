@echo off
REM Batch script to start the backend with environment variables

echo Starting Student Learning Buddy Backend...

REM Set environment variables
set GEMINI_API_KEY=AIzaSyBiS_m146g3MVXN2D8VefxvEq8Hk5IBbxA
set DATABASE_URL=sqlite:///./student_learning_buddy.db
set ENVIRONMENT=development
set DEBUG=True

echo Environment variables set
echo.
echo Starting uvicorn server...
python -m uvicorn app.main:app --reload
