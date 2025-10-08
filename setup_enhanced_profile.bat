@echo off
echo ========================================
echo Enhanced Profile Fields Setup
echo ========================================
echo.

echo Step 1: Running database migration...
python migrate_profile_fields.py
if %errorlevel% neq 0 (
    echo ERROR: Migration failed
    pause
    exit /b 1
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo New profile fields added:
echo   - Date of Birth
echo   - Phone Number
echo   - School/College Name
echo   - Grade Level
echo   - Major/Field of Study
echo   - Study Goals
echo   - Bio
echo.
echo Next steps:
echo 1. Restart backend: start_backend.bat
echo 2. Restart frontend: cd frontend ^&^& npm run dev
echo 3. Login and update your profile!
echo.
pause
