# Authentication System Setup Guide

## Overview
Complete authentication system with user registration, login, and protected routes.

## Features Implemented

### Backend (FastAPI)
- ✅ User registration with email, username, password
- ✅ User login with email/username and password
- ✅ Password hashing with SHA-256
- ✅ Token-based authentication
- ✅ User data storage in SQLite database
- ✅ Automatic student profile creation on signup

### Frontend (React + TypeScript)
- ✅ Login page with email/username and password
- ✅ Signup page with full registration form
- ✅ Protected routes (requires authentication)
- ✅ Auth context for global state management
- ✅ User info display in header
- ✅ Logout functionality
- ✅ Persistent login (localStorage)
- ✅ Black and gold theme matching the app

## Setup Instructions

### 1. Create Database Tables
```bash
python create_users_table.py
```

### 2. Start Backend
```bash
python -m uvicorn app.main:app --reload
```

### 3. Start Frontend
```bash
cd frontend
npm run dev
```

## How It Works

### User Flow

1. **New User**:
   - Visit http://localhost:3000
   - Redirected to `/login`
   - Click "Sign up" link
   - Fill registration form (email, username, password, full name)
   - Account created + automatic login
   - Redirected to home page

2. **Existing User**:
   - Visit http://localhost:3000
   - Redirected to `/login`
   - Enter email/username and password
   - Click "Sign In"
   - Redirected to home page

3. **Logged In User**:
   - Access all features (questions, quiz, notes, profile)
   - See user info in header
   - Click profile menu to logout

### Data Storage

**Backend (SQLite Database)**:
- User credentials (email, username, hashed password)
- User profile (full name, created date, last login)
- Student profile (linked to user)
- All user activity (questions, quizzes, notes)

**Frontend (localStorage)**:
- User session data (user_id, email, username, token)
- Persists across browser sessions
- Cleared on logout

## API Endpoints

### POST /api/auth/signup
Create new user account
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "password123",
  "full_name": "John Doe"
}
```

### POST /api/auth/login
Login with credentials
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### POST /api/auth/logout
Logout user (invalidate token)

## File Structure

### Backend
```
app/
├── api/
│   └── auth.py              # Auth endpoints
├── services/
│   └── auth_service.py      # Auth business logic
├── schemas/
│   └── auth.py              # Request/response models
├── models/
│   └── user.py              # User database model
└── main.py                  # Include auth router
```

### Frontend
```
frontend/src/
├── pages/
│   ├── LoginPage.tsx        # Login form
│   └── SignupPage.tsx       # Registration form
├── contexts/
│   └── AuthContext.tsx      # Auth state management
├── components/
│   ├── ProtectedRoute.tsx   # Route guard
│   └── Header.tsx           # Updated with user menu
├── App.tsx                  # Updated routing
└── main.tsx                 # Wrapped with AuthProvider
```

## Security Features

1. **Password Hashing**: SHA-256 hashing (consider bcrypt for production)
2. **Token-Based Auth**: Secure token generation
3. **Protected Routes**: Unauthorized users redirected to login
4. **Input Validation**: Email format, password length, username rules
5. **Error Handling**: Secure error messages (no info leakage)

## Testing

### Test Signup
1. Go to http://localhost:3000/signup
2. Fill form with valid data
3. Should create account and redirect to home

### Test Login
1. Go to http://localhost:3000/login
2. Enter credentials
3. Should login and redirect to home

### Test Protected Routes
1. Logout
2. Try to access http://localhost:3000/question
3. Should redirect to login

### Test Persistence
1. Login
2. Refresh page
3. Should stay logged in

## Troubleshooting

### "Email already registered"
- Email must be unique
- Use different email or login with existing account

### "Username already taken"
- Username must be unique
- Choose different username

### "Invalid email/username or password"
- Check credentials are correct
- Username is case-insensitive

### Not redirecting after login
- Check browser console for errors
- Verify backend is running on port 8000
- Check CORS settings in backend

### Database errors
- Run `python create_users_table.py`
- Check `student_learning_buddy.db` exists
- Verify database permissions

## Next Steps

### Recommended Enhancements
1. **Password Reset**: Email-based password recovery
2. **Email Verification**: Verify email on signup
3. **Better Password Hashing**: Use bcrypt instead of SHA-256
4. **Session Management**: Redis for token storage
5. **OAuth Integration**: Google/GitHub login
6. **2FA**: Two-factor authentication
7. **Profile Pictures**: Upload and display avatars
8. **Account Settings**: Update email, password, profile

## Database Schema

### users table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME,
    last_login DATETIME,
    student_id INTEGER
);
```

## Support

If you encounter issues:
1. Check backend logs for errors
2. Check browser console for frontend errors
3. Verify database tables exist
4. Ensure ports 8000 and 3000 are available
5. Clear browser cache and localStorage if needed

---

**Your authentication system is now ready! Users can sign up, login, and securely access all features of the Student Learning Buddy.**
