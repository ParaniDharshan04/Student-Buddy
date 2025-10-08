# Voice Assistant Troubleshooting

## Microphone Not Working

### Check 1: Browser Permissions
1. Click the 🔒 lock icon in the address bar
2. Check if microphone is "Allowed"
3. If "Blocked", change to "Allow"
4. Refresh the page

### Check 2: Browser Support
**Supported Browsers:**
- ✅ Chrome (Recommended)
- ✅ Edge (Recommended)
- ✅ Safari (Mac)
- ❌ Firefox (Limited support)

**Check if supported:**
Open browser console (F12) and run:
```javascript
'webkitSpeechRecognition' in window || 'SpeechRecognition' in window
```
Should return `true`

### Check 3: System Microphone
1. Check if microphone is connected
2. Test in system settings:
   - Windows: Settings → Privacy → Microphone
   - Mac: System Preferences → Security & Privacy → Microphone
3. Ensure browser has microphone access

### Check 4: HTTPS Required
Speech recognition requires HTTPS or localhost. Check your URL:
- ✅ `http://localhost:3000`
- ✅ `https://yourdomain.com`
- ❌ `http://192.168.x.x` (won't work)

## Common Errors

### "Speech recognition not supported"
**Solution**: Use Chrome or Edge browser

### "Could not start microphone"
**Solutions**:
1. Check browser permissions
2. Close other apps using microphone (Zoom, Teams, etc.)
3. Refresh the page
4. Restart browser

### "Speech recognition error: not-allowed"
**Solution**: 
1. Click lock icon in address bar
2. Allow microphone access
3. Refresh page

### "Speech recognition error: no-speech"
**Solutions**:
1. Speak louder
2. Check microphone volume
3. Reduce background noise
4. Move closer to microphone

### "Speech recognition error: network"
**Solutions**:
1. Check internet connection
2. Try again in a few seconds
3. Refresh the page

## Testing Microphone

### Quick Test
1. Go to Voice Assistant page
2. Click microphone button
3. Browser should ask for permission
4. Allow microphone
5. Speak: "Testing one two three"
6. Should see text appear

### Browser Console Test
Open console (F12) and run:
```javascript
const recognition = new webkitSpeechRecognition()
recognition.start()
recognition.onresult = (e) => console.log(e.results[0][0].transcript)
recognition.onerror = (e) => console.error(e.error)
```

Speak something. Should see transcript in console.

## Backend Issues

### AI Not Responding
**Check backend logs for errors:**
```
ERROR: Error in voice chat: ...
```

**Solutions**:
1. Check backend is running
2. Verify Gemini API key is set
3. Check internet connection
4. Look for error in browser console

### 401 Unauthorized
**Solution**: 
1. Logout and login again
2. Check token in localStorage
3. Verify authentication is working

### 500 Internal Server Error
**Solution**:
1. Check backend logs
2. Verify database is working
3. Restart backend

## Browser-Specific Issues

### Chrome/Edge
Usually works best. If issues:
1. Update to latest version
2. Check chrome://settings/content/microphone
3. Clear cache and cookies

### Safari
1. Check Safari → Preferences → Websites → Microphone
2. Ensure site has permission
3. May need to allow in System Preferences too

### Firefox
Limited support. Recommend using Chrome instead.

## Still Not Working?

### Debug Steps
1. **Open Browser Console** (F12)
2. **Click Microphone Button**
3. **Check for errors**
4. **Share error message**

### Common Console Errors

**"DOMException: The user has denied permission"**
→ Allow microphone in browser settings

**"DOMException: Requested device not found"**
→ No microphone connected

**"DOMException: The operation is insecure"**
→ Need HTTPS or localhost

**"Failed to fetch"**
→ Backend not running or network issue

## Alternative: Type Instead of Speak

If microphone doesn't work, you can still use the feature by:
1. Using the text input (if we add it)
2. Or use other features (Questions, Quiz, Notes)

## Report Issues

If none of these solutions work:
1. Note your browser and version
2. Copy error from console
3. Check backend logs
4. Share details for help

---

**Most issues are solved by:**
1. Using Chrome/Edge
2. Allowing microphone permissions
3. Refreshing the page
