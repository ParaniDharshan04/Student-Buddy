# PowerShell script to start the backend with environment variables

Write-Host "Starting Student Learning Buddy Backend..." -ForegroundColor Green

# Set environment variables
$env:GEMINI_API_KEY = "AIzaSyBiS_m146g3MVXN2D8VefxvEq8Hk5IBbxA"
$env:DATABASE_URL = "sqlite:///./student_learning_buddy.db"
$env:ENVIRONMENT = "development"
$env:DEBUG = "True"

Write-Host "Environment variables set" -ForegroundColor Yellow
Write-Host "API Key length: $($env:GEMINI_API_KEY.Length)" -ForegroundColor Yellow

# Start the server
Write-Host "`nStarting uvicorn server..." -ForegroundColor Green
python -m uvicorn app.main:app --reload
