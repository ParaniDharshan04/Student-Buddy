@echo off
echo ========================================
echo Complete Database Reset
echo ========================================
echo.
echo IMPORTANT: Stop the backend first (Ctrl+C in backend terminal)
echo.
pause
echo.

echo Deleting old database file...
del student_learning_buddy.db 2>nul
if exist student_learning_buddy.db (
    echo ERROR: Could not delete database file.
    echo Make sure backend is stopped!
    pause
    exit /b 1
)
echo ✓ Database file deleted
echo.

echo Creating new database with all columns...
python create_users_table.py
echo.

echo ========================================
echo Database Reset Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start backend: start_backend.bat
echo 2. Clear browser: localStorage.clear() in console
echo 3. Sign up as new user
echo.
pause
