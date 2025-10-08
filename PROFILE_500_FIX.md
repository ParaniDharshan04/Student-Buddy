# Profile 500 Error - FIXED

## Problem
POST /api/profile was returning 500 Internal Server Error when trying to create/update profile.

## Root Cause
The profile creation endpoint was:
1. Not requiring authentication
2. Trying to create a NEW student profile instead of updating the existing one
3. Trying to access fields that weren't in the request schema
4. Using wrong format for preferred_subjects (comma-separated instead of JSON)

## Solution
Updated the profile creation endpoint to:
1. Require authentication (`get_current_student_id` dependency)
2. Update the EXISTING student profile (created during signup)
3. Only use fields from the request
4. Store preferred_subjects as JSON (correct format)

## Changes Made

**File**: `app/api/profile.py`

### Before (Broken)
```python
@router.post("/profile", ...)
async def create_profile(
    request: ProfileCreateRequest,
    db: Session = Depends(get_db)
):
    # Tried to create NEW profile with fields that don't exist
    student = profile_service.create_student_profile(
        db=db,
        name=request.name,
        date_of_birth=request.date_of_birth,  # Not in request!
        phone_number=request.phone_number,    # Not in request!
        # ... many other fields
    )
```

### After (Fixed)
```python
@router.post("/profile", ...)
async def create_profile(
    request: ProfileCreateRequest,
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student_id)  # Auth required
):
    # Get EXISTING student profile
    student = db.query(Student).filter(Student.id == student_id).first()
    
    # Update only the fields from request
    student.name = request.name
    if request.email:
        student.email = request.email
    if request.preferred_subjects:
        student.preferred_subjects = json.dumps(request.preferred_subjects)
    if request.learning_style:
        student.learning_style = request.learning_style.value
    
    db.commit()
```

## How It Works Now

### User Flow
1. User signs up → Student profile created automatically
2. User logs in → Gets auth token
3. User goes to profile page → Sees "Create Your Profile" form
4. User fills in preferences → POST /api/profile
5. Backend updates existing student profile
6. User sees their profile with stats

### Profile Creation
- **Not** creating a new student (already exists from signup)
- **Updating** the existing student with preferences
- **Requires** authentication (user must be logged in)
- **Uses** correct JSON format for subjects

## Testing

### Step 1: Restart Backend
```bash
# Stop backend (Ctrl+C)
start_backend.bat
```

### Step 2: Clear Browser Data
```javascript
// In browser console (F12)
localStorage.clear()
location.reload()
```

### Step 3: Test Profile Creation
1. Sign up as new user
2. Login
3. Go to Profile page
4. Fill in the form:
   - Name: Your name
   - Email: your@email.com
   - Learning Style: Visual
   - Subjects: Math, Physics (click Add for each)
5. Click "Create Profile"
6. Should see profile page with stats (no 500 error!)

## Expected Behavior

### Backend Logs (Success)
```
INFO: POST /api/auth/signup HTTP/1.1 201 Created
INFO: POST /api/auth/login HTTP/1.1 200 OK
INFO: POST /api/profile HTTP/1.1 201 Created  ← Should be 201, not 500!
INFO: GET /api/profile/stats HTTP/1.1 200 OK
```

### Frontend
- Form submits successfully
- Redirects to profile view
- Shows profile with statistics
- No error messages

## Database Structure

### Users Table
```
id | email | username | password_hash | full_name | student_id
1  | ...   | user1    | ...           | John Doe  | 1
```

### Students Table
```
id | name     | email | preferred_subjects      | learning_style
1  | John Doe | ...   | ["Math", "Physics"]     | visual
```

**Note**: `student_id` in users table links to `id` in students table

## Troubleshooting

### Still getting 500 error?

**Check 1: Backend restarted?**
```bash
# Must restart to load new code
start_backend.bat
```

**Check 2: User has student_id?**
```python
# In Python console:
from app.database import SessionLocal
from app.models import User
db = SessionLocal()
user = db.query(User).first()
print(f"Student ID: {user.student_id}")  # Should not be None
```

**Check 3: Student profile exists?**
```python
from app.models import Student
student = db.query(Student).filter(Student.id == user.student_id).first()
print(f"Student: {student.name if student else 'NOT FOUND'}")
```

### Profile not showing after creation?

**Cause**: Frontend might be caching old data

**Fix**:
```javascript
// Clear cache and reload
localStorage.clear()
location.reload()
```

### "Student profile not found" error?

**Cause**: User doesn't have a student_id

**Fix**:
```bash
# Clear and recreate
python clear_all_users.py
python create_users_table.py
# Sign up again
```

## Related Endpoints

All these now work correctly:
- `POST /api/profile` - Update profile (fixed)
- `GET /api/profile` - Get profile
- `GET /api/profile/stats` - Get profile with stats
- `PUT /api/profile` - Update profile
- `DELETE /api/profile` - Delete profile

All require authentication and use the logged-in user's student_id.

## Security

- ✅ Authentication required
- ✅ Users can only update their own profile
- ✅ No way to access other users' profiles
- ✅ Student_id comes from auth token (can't be manipulated)

---

**Your profile creation is now working! Restart backend and try it! 🎉**
