# Fix 500 Internal Server Error

## Quick Diagnosis

Run this diagnostic script:
```bash
python diagnose_500_error.py
```

This will test each endpoint and show where the 500 error occurs.

## Common Causes & Fixes

### 1. Backend Not Restarted
**Symptom**: Code changes not taking effect

**Fix**:
```bash
# Stop backend (Ctrl+C)
# Start again
start_backend.bat
```

### 2. Database Schema Mismatch
**Symptom**: Errors about missing columns or tables

**Fix**:
```bash
# Recreate database tables
python create_users_table.py
```

### 3. Missing Student Profile
**Symptom**: Error about student_id being None

**Fix**: The signup process should create a student profile automatically. If it doesn't:
```bash
# Clear users and try again
python clear_all_users.py
# Restart backend
start_backend.bat
# Sign up again
```

### 4. Import Errors
**Symptom**: ModuleNotFoundError or ImportError

**Fix**:
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### 5. Database Lock
**Symptom**: "database is locked" error

**Fix**:
```bash
# Close all connections to database
# Restart backend
start_backend.bat
```

## How to Find the Exact Error

### Step 1: Check Backend Terminal
Look for error messages like:
```
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "...", line X, in ...
    ...
SomeError: Error message here
```

### Step 2: Check Backend Logs
If using logging to file:
```bash
type backend.log
```

### Step 3: Enable Debug Mode
In `app/main.py`, add:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Specific Error Solutions

### Error: "User does not have an associated student profile"

**Cause**: User was created without student_id

**Fix**:
```bash
python clear_all_users.py
# Sign up again (will create student profile)
```

### Error: "No such table: users"

**Cause**: Database tables not created

**Fix**:
```bash
python create_users_table.py
```

### Error: "Invalid token"

**Cause**: Token storage cleared (backend restart)

**Fix**:
```bash
# Just login again
# Tokens are in-memory and cleared on restart
```

### Error: "NoneType has no attribute..."

**Cause**: Missing data in database

**Fix**:
```bash
# Check which field is None
# Recreate database if needed
python clear_all_users.py
python create_users_table.py
```

## Testing After Fix

1. **Restart backend**:
   ```bash
   start_backend.bat
   ```

2. **Clear browser data**:
   ```javascript
   // In browser console (F12)
   localStorage.clear()
   location.reload()
   ```

3. **Sign up as new user**

4. **Test each feature**:
   - Ask a question
   - Generate a quiz
   - Create notes
   - View profile

## Still Getting 500 Errors?

### Share This Information:

1. **Backend error message** (from terminal)
2. **Which endpoint** is failing (question, quiz, notes, profile)
3. **When it happens** (after login, after clicking something)
4. **Browser console errors** (F12 → Console tab)

### Example Error Report:
```
Endpoint: POST /api/ask
Error: AttributeError: 'NoneType' object has no attribute 'id'
When: After asking a question
Backend traceback: [paste full error]
```

## Prevention

### Always Do After Code Changes:
1. Restart backend
2. Clear browser localStorage
3. Login again
4. Test features

### Keep Database Clean:
```bash
# Periodically clear test data
python clear_all_users.py
```

### Monitor Backend Logs:
- Watch terminal for errors
- Check for warnings
- Look for unusual behavior

---

**Most 500 errors are fixed by restarting the backend and clearing browser data!**
