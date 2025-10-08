# Troubleshooting Guide

## Quiz and Notes Not Working

### Quick Fix Steps:

1. **Stop the backend** (Press Ctrl+C in the backend terminal)

2. **Restart using the startup script:**
   ```bash
   start_backend.bat
   ```

3. **Verify the API key is loaded:**
   - Look for "Application startup complete" in the terminal
   - No errors about API key

4. **Test the backend directly:**
   - Open: http://localhost:8000/docs
   - Try the `/api/quiz` endpoint with test data
   - Try the `/api/notes` endpoint with test data

5. **Check frontend console:**
   - Open browser DevTools (F12)
   - Go to Console tab
   - Look for any red error messages

### Common Issues and Solutions:

#### Issue 1: "API key not valid" or "No API key found"

**Cause:** Environment variable not set

**Solution:**
```bash
# Use the startup script
start_backend.bat

# OR set manually before starting:
set GEMINI_API_KEY=AIzaSyBiS_m146g3MVXN2D8VefxvEq8Hk5IBbxA
python -m uvicorn app.main:app --reload
```

#### Issue 2: Frontend shows "Network Error" or "Failed to fetch"

**Cause:** Backend not running or wrong URL

**Solution:**
1. Make sure backend is running on port 8000
2. Check http://localhost:8000/health works
3. Check frontend is using correct API URL

#### Issue 3: "Model not found" error

**Cause:** Wrong Gemini model name

**Solution:** Already fixed - using `gemini-2.5-flash`

#### Issue 4: Quiz/Notes buttons don't do anything

**Cause:** JavaScript errors in frontend

**Solution:**
1. Open browser console (F12)
2. Look for error messages
3. Make sure frontend dependencies are installed:
   ```bash
   cd frontend
   npm install
   ```

#### Issue 5: "Rate limit exceeded"

**Cause:** Too many API requests

**Solution:** Wait 60 seconds and try again (free tier limit: 15 requests/minute)

### Detailed Debugging Steps:

#### Step 1: Verify Backend is Running
```bash
# Should show "healthy"
curl http://localhost:8000/health
```

#### Step 2: Test AI Service Directly
```bash
# Set environment variable
set GEMINI_API_KEY=AIzaSyBiS_m146g3MVXN2D8VefxvEq8Hk5IBbxA

# Run test
python test_api.py
```

Expected output:
```
✅ Question service works!
✅ Quiz service works!
✅ Notes service works!
```

#### Step 3: Test API Endpoints
Open http://localhost:8000/docs and test:
- POST /api/quiz
- POST /api/notes
- POST /api/ask

#### Step 4: Check Frontend API Calls
1. Open browser DevTools (F12)
2. Go to Network tab
3. Try generating a quiz
4. Look at the request/response

**If request fails:**
- Check the error message
- Verify backend URL is correct
- Check CORS settings

**If response is empty:**
- Check backend logs
- Verify API key is set
- Test endpoint in /docs

### Environment Variable Checklist:

- [ ] GEMINI_API_KEY is set
- [ ] API key is 39 characters long
- [ ] No quotes around the API key
- [ ] Backend started AFTER setting the variable

### Verification Commands:

```bash
# Check if backend is running
curl http://localhost:8000/health

# Check if frontend is running
curl http://localhost:3000

# Test Gemini API directly
python test_gemini_direct.py

# Test all services
python test_api.py
```

### Still Not Working?

1. **Restart everything:**
   ```bash
   # Stop backend (Ctrl+C)
   # Stop frontend (Ctrl+C)
   
   # Start backend
   start_backend.bat
   
   # In new terminal, start frontend
   cd frontend
   npm run dev
   ```

2. **Check logs:**
   - Backend terminal: Look for errors
   - Browser console: Look for JavaScript errors
   - Network tab: Look for failed requests

3. **Verify installations:**
   ```bash
   # Backend dependencies
   pip list | findstr google-generativeai
   
   # Frontend dependencies
   cd frontend
   npm list react
   ```

4. **Test with curl:**
   ```bash
   # Test quiz endpoint
   curl -X POST http://localhost:8000/api/quiz ^
     -H "Content-Type: application/json" ^
     -d "{\"topic\":\"Math\",\"question_count\":3,\"difficulty\":\"easy\",\"question_types\":[\"multiple_choice\"]}"
   ```

### Success Indicators:

✅ Backend shows "Application startup complete"
✅ http://localhost:8000/health returns "healthy"
✅ http://localhost:8000/docs loads
✅ test_api.py shows all ✅
✅ Frontend loads at http://localhost:3000
✅ Browser console has no errors
✅ Can ask questions successfully
✅ Can generate quizzes successfully
✅ Can summarize notes successfully

If all checkboxes are ✅, everything is working!
