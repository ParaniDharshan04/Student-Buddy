# Quick Fix for 402 Error

## The Problem
When uploading PDFs/documents, you get a 402 error. This is a **Gemini API quota limit**.

## Immediate Solutions

### Option 1: Use Smaller Documents ✅
- **Quiz**: Upload documents under 5 pages
- **Notes**: Upload documents under 10 pages
- The app now automatically truncates to safe limits

### Option 2: Use Manual Input Instead ✅
**For Quiz:**
1. Don't check "Upload study material"
2. Type the topic manually (e.g., "World War II")
3. Generate quiz

**For Notes:**
1. Don't check "Upload document"
2. Copy/paste text directly (max ~2000 words)
3. Summarize

### Option 3: Wait and Retry ✅
If you hit the limit:
1. Wait 60 seconds
2. Try again with smaller content
3. Or use manual input

## What I Fixed

✅ **Content length limits** - Large documents are now truncated automatically
✅ **Better error messages** - You'll see helpful tips when quota is exceeded
✅ **Improved handling** - App won't crash on quota errors

## Restart Backend to Apply Fixes

```bash
# Stop current backend (Ctrl+C)
# Restart:
start_backend.bat
```

## Test It

1. Try uploading a small PDF (1-2 pages) ✅
2. Or use manual text input ✅
3. Should work now!

## Why This Happens

Gemini Free Tier Limits:
- 15 requests per minute
- 1 million tokens per day
- Large documents use many tokens

## Long-term Solution

If you need to process large documents regularly:
1. Enable billing on Google Cloud
2. Get higher quota limits
3. Or break documents into smaller chunks

## For Now

**Best practice:**
- Use manual input for topics/questions
- Upload only small documents (1-5 pages)
- Wait between requests if you get errors

This will work reliably! 🎉
