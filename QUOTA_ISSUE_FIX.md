# 402 Error - API Quota Issue Fix

## What's Happening

The 402 error means the Gemini API has quota limits:

**Free Tier Limits:**
- 15 requests per minute
- 1 million tokens per day
- 1,500 requests per day

When you upload a large PDF/document, it might:
1. Exceed the token limit per request
2. Hit the rate limit if you make multiple requests quickly

## Solutions

### Solution 1: Use Smaller Documents (Immediate Fix)

**For Quiz Generation:**
- Upload documents under 5 pages
- Or paste text instead of uploading (max ~1000 words)

**For Notes Summarization:**
- Upload documents under 10 pages
- Or paste text instead of uploading (max ~2000 words)

### Solution 2: Wait Between Requests

If you get a 402 error:
1. Wait 60 seconds
2. Try again with a smaller document
3. Or use manual text input instead

### Solution 3: Check Your API Quota

1. Go to: https://aistudio.google.com/app/apikey
2. Click on your API key
3. Check "Usage" to see your quota
4. If exceeded, wait until it resets (daily reset)

### Solution 4: Upgrade to Paid Tier (If Needed)

If you need more quota:
1. Go to: https://console.cloud.google.com/
2. Enable billing for your project
3. Gemini API will have higher limits

## What I've Fixed

1. **Added content length limits** - Documents are now truncated to 15,000 characters (~3000 words)
2. **Better error messages** - You'll see a clear message about quota limits
3. **Improved error handling** - The app won't crash on quota errors

## Workarounds for Large Documents

### For Quiz Generation:
Instead of uploading a 50-page PDF, try:
1. Copy 2-3 pages of text
2. Paste it in the topic field
3. Generate quiz from that

### For Notes Summarization:
Instead of uploading a large document:
1. Copy the most important sections
2. Paste them in the text area
3. Summarize that portion

## Testing Your Quota

Run this to test if your API key is working:
```bash
python test_gemini_direct.py
```

If it works, your quota is fine. If you get 402, you've hit the limit.

## Quota Reset Times

- **Rate limit (15 req/min)**: Resets every minute
- **Daily token limit**: Resets at midnight UTC
- **Daily request limit**: Resets at midnight UTC

## Best Practices

1. **Don't upload huge PDFs** - Keep documents under 10 pages
2. **Wait between requests** - Don't spam the generate button
3. **Use text input for small content** - Faster and uses less quota
4. **Monitor your usage** - Check the API console regularly

## Current Limits Applied

- **File upload**: Max 10MB file size
- **Text extraction**: Truncated to 15,000 characters
- **Quiz generation**: Max 10 questions per request
- **Notes summarization**: Max 5,000 characters per request

These limits help prevent quota issues!

## If You Still Get 402 Errors

1. **Check your API key** - Make sure it's valid
2. **Wait 24 hours** - Daily quota resets
3. **Use smaller documents** - Break large docs into chunks
4. **Consider paid tier** - If you need more quota

## Alternative: Use Manual Input

Instead of file upload:
- **For Quiz**: Type the topic manually
- **For Notes**: Copy/paste text directly

This uses less tokens and is more reliable!
