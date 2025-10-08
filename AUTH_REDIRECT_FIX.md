# Authentication Redirect Issue - Fixed

## Problem
When on login/signup pages, selecting options or clicking links was redirecting back to the sign-in page.

## Root Causes Fixed

### 1. API Interceptor Issue
**Problem**: The API interceptor was redirecting to `/login` on 401 errors even when already on auth pages.

**Fix**: Updated response interceptor to check current path before redirecting:
```typescript
if (error.response?.status === 401) {
  const currentPath = window.location.pathname
  if (currentPath !== '/login' && currentPath !== '/signup') {
    localStorage.removeItem('user')
    window.location.href = '/login'
  }
}
```

### 2. Auth Token on Auth Endpoints
**Problem**: The request interceptor was adding auth tokens to login/signup requests.

**Fix**: Exclude auth endpoints from token injection:
```typescript
const isAuthEndpoint = config.url?.includes('/auth/')
if (!isAuthEndpoint) {
  // Add auth token
}
```

## Files Modified

- `frontend/src/lib/api.ts` - Fixed both interceptors

## How It Works Now

### Login/Signup Flow
1. User visits `/login` or `/signup`
2. No auth token added to requests
3. Login/signup requests work normally
4. On success, token saved and user redirected to home
5. No unwanted redirects during the process

### Protected Routes
1. User tries to access protected route without login
2. ProtectedRoute component redirects to `/login`
3. User logs in
4. Redirected to originally requested page

### API Errors
1. 401 error on protected pages → Redirect to login
2. 401 error on login/signup pages → No redirect (stay on page)
3. Other errors → Handled normally

## Testing

### Test Login
```bash
1. Go to http://localhost:3000/login
2. Enter credentials
3. Click "Sign In"
4. Should redirect to home (no loop)
```

### Test Signup
```bash
1. Go to http://localhost:3000/signup
2. Fill in all fields
3. Click "Create Account"
4. Should redirect to home (no loop)
```

### Test Invalid Credentials
```bash
1. Go to login page
2. Enter wrong password
3. Should show error message
4. Should stay on login page (no redirect)
```

### Test Protected Routes
```bash
1. Logout
2. Try to access http://localhost:3000/question
3. Should redirect to /login
4. Login
5. Should redirect back to /question
```

## Common Issues & Solutions

### Still getting redirects?

**Check 1: Clear browser cache and localStorage**
```javascript
// In browser console:
localStorage.clear()
location.reload()
```

**Check 2: Verify backend is running**
```bash
# Backend should be on port 8000
curl http://localhost:8000/health
```

**Check 3: Check browser console for errors**
- Open DevTools (F12)
- Look for red errors
- Check Network tab for failed requests

### Login works but immediately logs out?

**Possible cause**: Token not being saved properly

**Fix**: Check AuthContext is saving token:
```javascript
// Should see this in localStorage after login:
localStorage.getItem('user')
// Should return: {"user_id":1,"email":"...","token":"..."}
```

### Can't access any pages after login?

**Possible cause**: Token not being sent with requests

**Fix**: Check Network tab in DevTools:
- Click on any API request
- Check Headers
- Should see: `Authorization: Bearer <token>`

## Architecture

### Auth Flow
```
Login/Signup Page
    ↓
AuthContext.login/signup()
    ↓
Direct fetch() to /api/auth/*
    ↓
Save user + token to localStorage
    ↓
Navigate to home
    ↓
ProtectedRoute checks isAuthenticated
    ↓
Render protected content
```

### API Request Flow
```
Component makes API call
    ↓
axios interceptor checks URL
    ↓
If NOT /auth/* → Add Authorization header
    ↓
Make request
    ↓
If 401 error AND NOT on /login or /signup
    ↓
Redirect to /login
```

## Security Notes

1. **Tokens in localStorage**: Acceptable for MVP, consider httpOnly cookies for production
2. **Token expiration**: Not implemented yet, tokens don't expire
3. **HTTPS**: Use HTTPS in production to protect tokens in transit
4. **CORS**: Currently allows localhost, restrict in production

## Next Steps (Optional Enhancements)

1. **Token Refresh**: Implement token refresh before expiration
2. **Remember Me**: Add option to persist login longer
3. **Session Timeout**: Auto-logout after inactivity
4. **Better Error Messages**: More specific error feedback
5. **Loading States**: Better loading indicators during auth

---

**Your authentication flow is now working correctly! No more redirect loops! 🎉**
