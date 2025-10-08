# Fix Voice Assistant Network Error

## The Problem
"Network error. Speech recognition requires internet connection."

This error occurs because browser speech recognition uses Google's servers, and sometimes the connection fails.

## Quick Fixes (Try in Order)

### Fix 1: Check Internet Connection
```bash
# Test if you can reach Google
ping google.com
```
- Make sure you have active internet
- Try opening google.com in browser
- Check if other websites load

### Fix 2: Use HTTPS or Localhost
Speech recognition requires secure connection:
- ✅ `http://localhost:3000` (should work)
- ✅ `https://yourdomain.com` (should work)
- ❌ `http://192.168.x.x` (won't work)

**Check your URL** - it should be localhost!

### Fix 3: Restart Browser
1. Close ALL browser windows
2. Reopen browser
3. Go to http://localhost:3000/voice-assistant
4. Try microphone again

### Fix 4: Clear Browser Cache
1. Press Ctrl+Shift+Delete
2. Select "Cached images and files"
3. Click "Clear data"
4. Refresh page

### Fix 5: Try Different Browser
- Chrome (Recommended) ✅
- Edge (Recommended) ✅
- Safari (Mac only) ⚠️
- Firefox (Not recommended) ❌

### Fix 6: Check Firewall/Antivirus
Some security software blocks speech recognition:
1. Temporarily disable firewall
2. Try microphone
3. If it works, add exception for browser

### Fix 7: Use VPN (if available)
Sometimes ISP blocks Google speech API:
1. Connect to VPN
2. Try microphone again

## Alternative: Use Text Input

While troubleshooting, you can still use the feature:
1. Type your message in the text box
2. Press Enter or click Send
3. AI will respond with voice
4. Works exactly the same!

## Technical Details

### Why This Happens
Browser speech recognition (Web Speech API) sends audio to Google's servers for processing. The "network" error means:
1. Can't reach Google's servers
2. Connection timeout
3. Firewall blocking
4. ISP restrictions
5. Temporary Google service issue

### Check Browser Support
Open console (F12) and run:
```javascript
console.log('Speech Recognition:', 'webkitSpeechRecognition' in window)
console.log('User Agent:', navigator.userAgent)
```

Should show:
```
Speech Recognition: true
User Agent: Chrome/... or Edge/...
```

### Test Connection to Google
```javascript
fetch('https://www.google.com')
  .then(() => console.log('✓ Can reach Google'))
  .catch(() => console.log('✗ Cannot reach Google'))
```

## Advanced Troubleshooting

### Check Browser Permissions
1. Go to: chrome://settings/content/microphone
2. Check if localhost is allowed
3. Remove any blocks

### Check System Microphone
Windows:
```
Settings → Privacy → Microphone → Allow apps to access microphone
```

Mac:
```
System Preferences → Security & Privacy → Microphone → Allow Chrome
```

### Test Microphone Directly
Open console (F12) and run:
```javascript
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    console.log('✓ Microphone works')
    stream.getTracks().forEach(track => track.stop())
  })
  .catch(err => console.log('✗ Microphone error:', err))
```

### Check Network Requests
1. Open DevTools (F12)
2. Go to Network tab
3. Click microphone
4. Look for requests to Google
5. Check if any are blocked

## Still Not Working?

### Option 1: Use Text Input
The text input works perfectly and gives you the same experience:
- Type instead of speak
- AI still responds with voice
- All features work

### Option 2: Wait and Retry
Sometimes Google's speech service has temporary issues:
- Wait 5-10 minutes
- Try again
- Usually resolves itself

### Option 3: Different Network
Try on different network:
- Mobile hotspot
- Different WiFi
- Different location

## Report Issue

If none of these work, provide:
1. Browser and version
2. Operating system
3. URL you're using
4. Console errors (F12)
5. Network tab screenshot

## Success Checklist

✅ Using Chrome or Edge
✅ URL is http://localhost:3000
✅ Internet connection working
✅ Can access google.com
✅ Microphone permissions allowed
✅ No firewall blocking
✅ Browser cache cleared

If all checked, microphone should work!

---

**Most Common Solution:**
1. Use Chrome browser
2. Make sure URL is localhost
3. Check internet connection
4. Click microphone and allow permissions
5. If still fails, use text input instead
