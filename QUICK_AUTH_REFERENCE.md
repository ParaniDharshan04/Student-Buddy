# Quick Authentication Reference

## 🚀 Quick Start

1. **Setup Database**:
   ```bash
   python create_users_table.py
   ```

2. **Start Backend**:
   ```bash
   start_backend.bat
   ```

3. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

4. **Open Browser**: http://localhost:3000

## 📝 First Time User

1. You'll see the **Login Page**
2. Click **"Sign up"** at the bottom
3. Fill in the form:
   - Full Name: Your name
   - Email: your@email.com
   - Username: choose a username (3+ chars)
   - Password: create password (6+ chars)
   - Confirm Password: same as above
4. Click **"Create Account"**
5. You're automatically logged in! 🎉

## 🔐 Returning User

1. Go to http://localhost:3000
2. Enter your **email or username**
3. Enter your **password**
4. Click **"Sign In"**
5. Welcome back! 🎉

## 👤 User Menu

Click your profile icon in the header to:
- View your profile
- Logout

## 🔒 What's Protected

All these pages require login:
- ✅ Home (/)
- ✅ Ask Questions (/question)
- ✅ Take Quiz (/quiz)
- ✅ Generate Notes (/notes)
- ✅ Profile (/profile)

## 💾 Data Storage

**Your data is stored in**:
- User credentials → SQLite database
- Login session → Browser localStorage
- Questions, quizzes, notes → Database (linked to your account)

## 🎨 Features

- ✅ Secure password hashing
- ✅ Persistent login (stays logged in after refresh)
- ✅ Beautiful black & gold theme
- ✅ Responsive design
- ✅ Error handling with helpful messages
- ✅ Form validation

## ⚠️ Common Issues

**"Email already registered"**
→ Use a different email or login with existing account

**"Username already taken"**
→ Choose a different username

**"Passwords do not match"**
→ Make sure both password fields are identical

**Can't access pages**
→ Make sure you're logged in

**Stuck on login page**
→ Check that backend is running on port 8000

## 🔄 Reset Everything

To start fresh:
```bash
python reset_database.py
```
This will delete all users and data.

## 📱 Pages

- `/login` - Sign in page
- `/signup` - Create account page
- `/` - Home (protected)
- `/question` - Ask questions (protected)
- `/quiz` - Take quizzes (protected)
- `/notes` - Generate notes (protected)
- `/profile` - Your profile (protected)

---

**Enjoy your personalized learning experience! 🎓**
