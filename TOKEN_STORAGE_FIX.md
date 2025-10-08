# Token Storage Fix - 401 Unauthorized Issue

## Problem
After successful login (200 OK), subsequent API calls were getting 401 Unauthorized errors.

## Root Cause
The `AuthService` class was creating a new `active_tokens` dictionary for each instance. When:
1. User logs in via `/api/auth/login` → Token stored in auth.py's AuthService instance
2. User makes API call → dependencies.py creates NEW AuthService instance
3. New instance has empty `active_tokens` dictionary
4. Token verification fails → 401 Unauthorized

## Solution
Made the token storage shared across all `AuthService` instances using a module-level variable.

### Code Change

**File**: `app/services/auth_service.py`

**Before**:
```python
class AuthService:
    def __init__(self):
        self.active_tokens = {}  # Each instance has its own dict
```

**After**:
```python
# Shared token storage across all instances
_active_tokens = {}

class AuthService:
    def __init__(self):
        self.active_tokens = _active_tokens  # All instances share same dict
```

## How It Works Now

1. **Login**: Token stored in `_active_tokens` (module-level)
2. **API Call**: New AuthService instance references same `_active_tokens`
3. **Token Verification**: Finds token in shared storage
4. **Success**: Request proceeds with authenticated user

## Testing

### Manual Test
1. Clear existing users: `python clear_all_users.py`
2. Start backend: `start_backend.bat`
3. Start frontend: `cd frontend && npm run dev`
4. Sign up as new user
5. Try to access any feature (questions, quiz, notes, profile)
6. Should work without 401 errors

### Automated Test
```bash
python test_auth_token.py
```

This will:
- Create a test user
- Get auth token
- Test protected endpoints with token
- Verify token works correctly

## Expected Backend Logs

### Successful Flow
```
INFO: POST /api/auth/login HTTP/1.1 200 OK
INFO: GET /api/profile/stats HTTP/1.1 200 OK
INFO: POST /api/quiz HTTP/1.1 200 OK
```

### Before Fix (Broken)
```
INFO: POST /api/auth/login HTTP/1.1 200 OK
INFO: GET /api/profile/stats HTTP/1.1 401 Unauthorized  ← Token not found
INFO: POST /api/quiz HTTP/1.1 401 Unauthorized  ← Token not found
```

## Files Modified

- `app/services/auth_service.py` - Shared token storage
- `app/dependencies.py` - Added debug logging
- `test_auth_token.py` - NEW test script

## Architecture

### Token Flow
```
Login Request
    ↓
AuthService.login() in auth.py
    ↓
Token stored in _active_tokens (module-level)
    ↓
Token returned to client
    ↓
Client stores token in localStorage
    ↓
Client makes API request with token
    ↓
dependencies.py creates AuthService instance
    ↓
AuthService.verify_token() checks _active_tokens
    ↓
Token found! Returns user_id
    ↓
Request proceeds with authenticated user
```

## Production Considerations

### Current Implementation (Development)
- In-memory token storage
- Tokens lost on server restart
- Not suitable for multiple server instances

### Production Recommendations
1. **Redis**: Store tokens in Redis for persistence and scalability
2. **JWT**: Use JSON Web Tokens (self-contained, no storage needed)
3. **Database**: Store tokens in database with expiration
4. **Token Expiration**: Implement token refresh mechanism

### Example Redis Implementation
```python
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

class AuthService:
    def login(self, db, email, password):
        # ... authentication logic ...
        token = secrets.token_urlsafe(32)
        redis_client.setex(f"token:{token}", 3600, user.id)  # 1 hour expiry
        return user, token
    
    def verify_token(self, token):
        user_id = redis_client.get(f"token:{token}")
        return int(user_id) if user_id else None
```

## Troubleshooting

### Still getting 401 errors?

**Step 1: Check backend logs**
```bash
# Look for these messages:
INFO: User testuser logged in
WARNING: Invalid token attempted: ...
```

**Step 2: Verify token is being sent**
- Open browser DevTools (F12)
- Go to Network tab
- Make an API request
- Check request headers
- Should see: `Authorization: Bearer <token>`

**Step 3: Check token in localStorage**
```javascript
// In browser console:
const user = JSON.parse(localStorage.getItem('user'))
console.log(user.token)
```

**Step 4: Restart backend**
```bash
# Stop backend (Ctrl+C)
# Start again
start_backend.bat
```

**Step 5: Clear and re-login**
```javascript
// In browser console:
localStorage.clear()
// Then login again
```

### Token not persisting?

**Check**: Backend restart clears tokens (in-memory storage)
**Solution**: Login again after backend restart

### Multiple users interfering?

**Check**: All users share same token storage (correct behavior)
**Note**: Each user has unique token, no interference

## Security Notes

1. **Token Storage**: In-memory is fine for development
2. **Token Format**: Random 32-byte URL-safe string
3. **Token Transmission**: Sent in Authorization header (secure)
4. **Token Validation**: Checked on every protected request
5. **User Verification**: User existence and active status checked

## Next Steps

1. ✅ Token storage fixed
2. ✅ Authentication working
3. ✅ Protected endpoints accessible
4. Consider: Token expiration (1 hour, 24 hours, etc.)
5. Consider: Token refresh mechanism
6. Consider: Redis for production

---

**Your authentication system is now fully functional! 🎉**

All API calls should work correctly after login.
