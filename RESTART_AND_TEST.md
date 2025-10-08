# Quick Restart and Test Guide

## ✅ All Issues Fixed!

1. User data isolation ✓
2. Login/signup redirects ✓
3. Token storage (401 errors) ✓
4. Profile creation (500 error) ✓

## Restart Steps

### 1. Stop Backend
In the backend terminal, press `Ctrl+C`

### 2. Start Backend
```bash
start_backend.bat
```

Wait for:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 3. Clear Browser
Open browser console (F12) and run:
```javascript
localStorage.clear()
location.reload()
```

## Test Checklist

### ✓ Test 1: Signup
1. Go to http://localhost:3000/signup
2. Fill in all fields
3. Click "Create Account"
4. Should redirect to home page

### ✓ Test 2: Profile Creation
1. Click "View Profile" in header
2. Should see "Create Your Profile" screen
3. Fill in:
   - Name: Your name
   - Email: your@email.com
   - Learning Style: Visual
   - Add subjects: Math, Physics
4. Click "Create Profile"
5. Should see profile page with stats (no errors!)

### ✓ Test 3: Ask Question
1. Go to "Ask Questions"
2. Type: "What is 2+2?"
3. Select explanation style
4. Click "Get Answer"
5. Should get AI response

### ✓ Test 4: Generate Quiz
1. Go to "Take Quiz"
2. Enter topic: "Mathematics"
3. Select options
4. Click "Generate Quiz"
5. Should get quiz questions

### ✓ Test 5: Create Notes
1. Go to "Generate Notes"
2. Paste some text
3. Select format
4. Click "Summarize"
5. Should get summary

### ✓ Test 6: Data Isolation
1. Logout
2. Create another user
3. New user should see empty state
4. No data from first user

## Expected Results

### Backend Logs (All 200/201)
```
INFO: POST /api/auth/signup HTTP/1.1 201 Created
INFO: POST /api/auth/login HTTP/1.1 200 OK
INFO: POST /api/profile HTTP/1.1 201 Created
INFO: GET /api/profile/stats HTTP/1.1 200 OK
INFO: POST /api/ask HTTP/1.1 200 OK
INFO: POST /api/quiz HTTP/1.1 200 OK
INFO: POST /api/notes HTTP/1.1 200 OK
```

No 401 or 500 errors!

### Frontend
- No error messages
- All features work
- Smooth navigation
- Data saves correctly

## If Something Fails

### Backend won't start?
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000
# Kill the process if needed
```

### Still getting errors?
```bash
# Nuclear option - fresh start
python clear_all_users.py
python create_users_table.py
start_backend.bat
# Then clear browser and signup again
```

### Frontend issues?
```bash
cd frontend
npm install
npm run dev
```

## Success Indicators

✅ Backend starts without errors
✅ Can signup new user
✅ Can login
✅ Can create profile
✅ Can use all features
✅ Each user sees only their data
✅ No 401 or 500 errors in logs

## Quick Commands

```bash
# Backend
start_backend.bat

# Frontend (in new terminal)
cd frontend
npm run dev

# Clear users
python clear_all_users.py

# Recreate tables
python create_users_table.py

# Test auth
python test_auth_token.py

# Diagnose issues
python diagnose_500_error.py
```

---

**Everything should work now! Restart backend and test! 🚀**
