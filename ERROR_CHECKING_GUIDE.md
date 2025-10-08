# Error Checking Guide

## How to Check for Errors

### 1. Browser Console Errors
Open your browser DevTools (F12) and check:

**Console Tab:**
- Look for red error messages
- Check for warnings (yellow)
- Note any failed network requests

**Common Errors to Look For:**
```
❌ "Cannot read property 'X' of undefined"
❌ "Network Error"
❌ "404 Not Found"
❌ "500 Internal Server Error"
❌ "Uncaught TypeError"
```

### 2. Network Tab Errors
In DevTools Network tab:

**Check for:**
- ❌ Red/failed requests
- ❌ 404 errors (endpoint not found)
- ❌ 500 errors (server error)
- ❌ 422 errors (validation error)
- ❌ CORS errors

**How to Check:**
1. Open Network tab
2. Refresh page
3. Look for red items
4. Click on failed requests
5. Check Response tab for error details

### 3. Backend Terminal Errors
Check the terminal where backend is running:

**Look for:**
```
❌ Traceback (Python errors)
❌ "Error: ..."
❌ "Failed to ..."
❌ "Exception: ..."
```

### 4. Frontend Terminal Errors
Check the terminal where frontend is running:

**Look for:**
```
❌ "ERROR in ..."
❌ "Failed to compile"
❌ "Module not found"
❌ "Cannot find module"
```

## Common Issues & Solutions

### Issue 1: Profile Menu Not Showing
**Symptoms:**
- No avatar in top right
- "Create Profile" button not showing

**Check:**
1. Is profile created? (localStorage has studentId)
2. Is backend running?
3. Console errors?

**Solution:**
```bash
# Check localStorage
localStorage.getItem('studentId')

# If null, create profile first
# Go to /profile and create one
```

### Issue 2: Edit Profile Not Working
**Symptoms:**
- Form doesn't pre-fill
- Save button doesn't work
- Gets 500 error

**Check:**
1. Backend terminal for errors
2. Network tab for failed request
3. Console for JavaScript errors

**Solution:**
```bash
# Restart backend
start_backend.bat

# Clear browser cache
Ctrl+Shift+Delete

# Try again
```

### Issue 3: Profile Not Updating in Header
**Symptoms:**
- Edit profile saves
- But header still shows old name

**Check:**
1. Did page refresh?
2. Is React Query cache stale?

**Solution:**
```javascript
// Hard refresh
Ctrl+Shift+R

// Or clear cache and reload
```

### Issue 4: API Calls Failing
**Symptoms:**
- Network errors
- 404 errors
- CORS errors

**Check:**
1. Is backend running on port 8000?
2. Is frontend running on port 3000?
3. Check CORS settings

**Solution:**
```bash
# Check backend
curl http://localhost:8000/health

# Should return: {"status":"healthy"...}

# If not, restart backend
start_backend.bat
```

### Issue 5: TypeScript Errors
**Symptoms:**
- Red squiggly lines in code
- "Type 'X' is not assignable to type 'Y'"

**Check:**
1. Run diagnostics
2. Check type definitions

**Solution:**
```bash
# In frontend directory
npm run build

# Check for errors
```

## Debugging Steps

### Step 1: Check Backend Health
```bash
# Open in browser
http://localhost:8000/health

# Should show:
{
  "status": "healthy",
  "environment": "development",
  "version": "1.0.0",
  "ai_provider": "Google Gemini"
}
```

### Step 2: Check Frontend Running
```bash
# Open in browser
http://localhost:3000

# Should show the app
```

### Step 3: Check Profile API
```bash
# If you have studentId = 1
http://localhost:8000/api/profile/1

# Should return profile data
```

### Step 4: Check Browser Console
```javascript
// In browser console, type:
localStorage.getItem('studentId')

// Should return a number or null
```

### Step 5: Test Profile Creation
1. Go to http://localhost:3000/profile
2. Fill in form
3. Click "Create Profile"
4. Check console for errors
5. Check Network tab for API call

### Step 6: Test Profile Edit
1. Go to profile page
2. Click "Edit Profile"
3. Change name
4. Click "Update Profile"
5. Check console for errors
6. Check if header updates

## Error Messages Explained

### "Cannot read property 'name' of undefined"
**Meaning:** Profile data not loaded yet
**Solution:** Add loading state or null check

### "Network Error"
**Meaning:** Can't reach backend
**Solution:** Check backend is running

### "404 Not Found"
**Meaning:** API endpoint doesn't exist
**Solution:** Check URL is correct

### "500 Internal Server Error"
**Meaning:** Backend crashed
**Solution:** Check backend terminal for error

### "422 Unprocessable Entity"
**Meaning:** Validation error
**Solution:** Check request data format

### "CORS Error"
**Meaning:** Cross-origin request blocked
**Solution:** Check CORS settings in backend

## Quick Fixes

### Fix 1: Clear Everything and Restart
```bash
# Stop both servers (Ctrl+C)

# Clear browser data
Ctrl+Shift+Delete
- Clear cache
- Clear localStorage

# Restart backend
start_backend.bat

# Restart frontend
cd frontend
npm run dev

# Try again
```

### Fix 2: Reset Profile
```javascript
// In browser console
localStorage.removeItem('studentId')
location.reload()

// Create new profile
```

### Fix 3: Check API Key
```bash
# In backend terminal
python -c "from app.config import settings; print('Key:', settings.GEMINI_API_KEY[:10])"

# Should show first 10 chars of key
```

### Fix 4: Reinstall Dependencies
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## What to Report

If you're still having issues, please provide:

1. **Error message** (exact text)
2. **Where it occurs** (which page/action)
3. **Console errors** (screenshot or copy)
4. **Network errors** (from Network tab)
5. **Backend errors** (from terminal)

## Success Indicators

✅ Backend shows "Application startup complete"
✅ Frontend shows "Local: http://localhost:3000"
✅ http://localhost:8000/health returns "healthy"
✅ Profile menu shows in top right
✅ Can create profile
✅ Can edit profile
✅ Can ask questions
✅ Can generate quizzes
✅ Can summarize notes

If all ✅, everything is working!

## Still Having Issues?

Try this complete reset:

```bash
# 1. Stop everything
Ctrl+C (in both terminals)

# 2. Clear browser
Ctrl+Shift+Delete
- Clear everything
- Close browser

# 3. Restart backend
start_backend.bat

# 4. Restart frontend (new terminal)
cd frontend
npm run dev

# 5. Open fresh browser
http://localhost:3000

# 6. Create profile
# 7. Test features
```

This should fix most issues! 🔧
