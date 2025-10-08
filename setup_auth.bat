@echo off
echo ========================================
echo Student Learning Buddy - Auth Setup
echo ========================================
echo.

echo Step 1: Creating database tables...
python create_users_table.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to create tables
    pause
    exit /b 1
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start backend: start_backend.bat
echo 2. Start frontend: cd frontend ^&^& npm run dev
echo 3. Visit: http://localhost:3000
echo.
echo You will be redirected to login page.
echo Click "Sign up" to create your account!
echo.
pause
