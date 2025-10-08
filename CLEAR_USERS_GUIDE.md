# Clear User Credentials Guide

## Quick Clear (No Confirmation)

```bash
python clear_all_users.py
```

This will instantly remove all user credentials from the database.

## Clear with Confirmation

```bash
python clear_users.py
```

This will ask for confirmation before deleting users.

## What Gets Deleted

- ✅ All user accounts (email, username, password)
- ✅ All user profile data
- ✅ User login history

## What Stays

- ✅ Student profiles (can be reused)
- ✅ Study sessions
- ✅ Quiz attempts
- ✅ Database structure

## When to Use

- Starting fresh with new accounts
- Testing signup functionality
- Removing test accounts
- Clearing old credentials

## After Clearing

Users can create new accounts by:
1. Going to http://localhost:3000
2. Clicking "Sign up"
3. Creating a new account

## Status Check

To see if there are any users:
```bash
python -c "from app.database import SessionLocal; from app.models import User; db = SessionLocal(); print(f'Users in database: {db.query(User).count()}'); db.close()"
```

---

**Current Status**: ✅ Database is clean - No user credentials stored
