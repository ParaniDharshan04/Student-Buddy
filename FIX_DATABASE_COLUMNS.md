# Fix Database Columns Issue

## Problem
The database table doesn't have the new columns that the Student model expects.

## Solution

### Step 1: Stop Backend
In the backend terminal, press **Ctrl+C** to stop the server.

### Step 2: Delete Database File
```bash
del student_learning_buddy.db
```

If you get "file is being used" error, make sure backend is completely stopped.

### Step 3: Recreate Database
```bash
python create_users_table.py
```

### Step 4: Start Backend
```bash
start_backend.bat
```

### Step 5: Clear Browser
Open browser console (F12) and run:
```javascript
localStorage.clear()
location.reload()
```

### Step 6: Sign Up Again
All old users are deleted, so create a new account.

## Or Use the Automated Script

```bash
# 1. Stop backend first (Ctrl+C)
# 2. Run this:
reset_database_complete.bat
# 3. Start backend: start_backend.bat
```

## Why This Happened

The Student model in `app/models/student.py` has these columns:
- date_of_birth
- phone_number
- school_name
- grade_level
- major_field
- study_goals
- bio

But your database table was created before these columns were added.

SQLAlchemy's `create_all()` only creates NEW tables, it doesn't ALTER existing tables.

So we need to:
1. Delete the old database
2. Create a new one with all columns

## After Fix

You should be able to:
- ✅ Sign up new users
- ✅ Create profiles
- ✅ Use all features
- ✅ No more 500 errors

---

**Stop backend → Delete database → Recreate → Start backend → Test!**
