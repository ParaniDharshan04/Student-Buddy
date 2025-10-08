# 🔄 Restart Instructions - AI Features Fixed!

## What Was Fixed

✅ Updated Gemini model from `gemini-pro` to `gemini-2.5-flash`
✅ Fixed API key loading (removed quotes)
✅ Fixed async/sync compatibility issue
✅ All AI features should now work!

## How to Restart

### Step 1: Stop Current Backend
If your backend is running, press `Ctrl+C` to stop it.

### Step 2: Restart Backend
```bash
python -m uvicorn app.main:app --reload
```

### Step 3: Test the Connection (Optional)
In a new terminal:
```bash
python test_gemini.py
```

You should see:
```
✅ Success!
Response: 2 + 2 = 4
```

### Step 4: Test in Browser
1. Open http://localhost:3000 (make sure frontend is running)
2. Try each feature:

#### Test Questions
- Go to "Ask a Question"
- Type: "What is photosynthesis?"
- Click "Ask Question"
- ✅ Should get detailed answer

#### Test Quiz
- Go to "Take a Quiz"
- Topic: "Solar System"
- Difficulty: Medium
- Questions: 5
- Click "Generate Quiz"
- ✅ Should get 5 quiz questions

#### Test Notes
- Go to "Summarize Notes"
- Paste some text (or upload a file)
- Format: Bullet Points
- Click "Summarize Notes"
- ✅ Should get summary

## If Something Still Doesn't Work

### Check Backend Logs
Look at the terminal where backend is running for error messages.

### Common Issues

**"API key not valid"**
- Get a new API key from: https://aistudio.google.com/apikey
- Update `.env` file with new key (no quotes!)
- Restart backend

**"Rate limit exceeded"**
- Free tier: 15 requests per minute
- Wait 60 seconds and try again

**"Model not found"**
- Make sure you're using `gemini-2.5-flash`
- Check `app/config.py` has correct model name

**Frontend shows error**
- Check browser console (F12)
- Make sure backend is running on port 8000
- Check CORS settings

### Still Having Issues?

1. Check your API key is valid:
   ```bash
   python -c "from app.config import settings; print('Key length:', len(settings.GEMINI_API_KEY))"
   ```
   Should show: `Key length: 39`

2. Test Gemini directly:
   ```bash
   python test_gemini.py
   ```

3. Check backend is running:
   - Visit http://localhost:8000/health
   - Should show: `{"status":"healthy",...}`

4. Check frontend is running:
   - Visit http://localhost:3000
   - Should show the app

## Quick Command Reference

```bash
# Start backend
python -m uvicorn app.main:app --reload

# Start frontend (in another terminal)
cd frontend
npm run dev

# Test Gemini API
python test_gemini.py

# Check API key
python -c "from app.config import settings; print(settings.GEMINI_API_KEY[:10])"
```

## Success Checklist

- [ ] Backend running without errors
- [ ] Frontend running on port 3000
- [ ] Can ask questions and get answers
- [ ] Can generate quizzes
- [ ] Can summarize notes
- [ ] Can upload files

Once all checkboxes are ✅, everything is working! 🎉
