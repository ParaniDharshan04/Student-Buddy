# Test Backend is Working

## Step 1: Make sure backend is running with the API key

Stop your current backend (Ctrl+C) and restart it using:

```bash
start_backend.bat
```

## Step 2: Test the health endpoint

Open your browser or use curl:
```
http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "environment": "development",
  "version": "1.0.0",
  "ai_provider": "Google Gemini"
}
```

## Step 3: Test the quiz endpoint directly

Open: http://localhost:8000/docs

Find the `/api/quiz` endpoint and click "Try it out"

Use this test data:
```json
{
  "topic": "Solar System",
  "question_count": 3,
  "difficulty": "easy",
  "question_types": ["multiple_choice"]
}
```

Click "Execute"

You should get back quiz questions!

## Step 4: Test the notes endpoint

In the same docs page, find `/api/notes` and click "Try it out"

Use this test data:
```json
{
  "content": "Python is a high-level programming language. It is known for its simple syntax and readability. Python is widely used in web development, data science, and artificial intelligence.",
  "format": "bullet_points"
}
```

Click "Execute"

You should get back a summary!

## If tests fail:

### Check backend logs
Look at the terminal where backend is running for error messages.

### Common issues:

1. **"API key not valid"** - The environment variable isn't set
   - Solution: Use `start_backend.bat` to start the server

2. **"Connection refused"** - Backend isn't running
   - Solution: Start the backend first

3. **"404 Not Found"** - Wrong URL
   - Solution: Make sure you're using http://localhost:8000

4. **Frontend shows errors** - Backend is working but frontend can't connect
   - Check browser console (F12)
   - Make sure frontend is using correct API URL

## Success indicators:

✅ Health endpoint returns "healthy"
✅ API docs page loads at /docs
✅ Quiz endpoint returns questions
✅ Notes endpoint returns summary
✅ No errors in backend terminal

Once all these work, the frontend should work too!
