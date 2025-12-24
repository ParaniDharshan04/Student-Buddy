# 🚀 Cloud Deployment Guide - Student Learning Buddy

This guide covers multiple deployment options for your AI-powered learning platform.

---

## 📋 Table of Contents
1. [Quick Deploy Options](#quick-deploy-options)
2. [Backend Deployment (FastAPI)](#backend-deployment)
3. [Frontend Deployment (React)](#frontend-deployment)
4. [Database Setup](#database-setup)
5. [Environment Variables](#environment-variables)
6. [Post-Deployment Steps](#post-deployment-steps)

---

## 🎯 Quick Deploy Options

### **Option 1: Render (Recommended - Free Tier Available)**
- ✅ Free tier for both frontend and backend
- ✅ Easy setup with GitHub integration
- ✅ Automatic deployments
- ✅ Built-in PostgreSQL database

### **Option 2: Railway**
- ✅ Simple deployment
- ✅ Free $5 monthly credit
- ✅ Great for full-stack apps

### **Option 3: Vercel (Frontend) + Render (Backend)**
- ✅ Best performance for React apps
- ✅ Free tier available
- ✅ Excellent for production

### **Option 4: AWS / Google Cloud / Azure**
- ✅ Most scalable
- ❌ More complex setup
- ❌ Costs can add up

---

## 🔧 Backend Deployment (FastAPI)

### **Option A: Deploy to Render**

#### Step 1: Prepare Your Backend

1. **Create `requirements.txt`** (already exists, verify it has):
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
google-genai==0.2.0
PyPDF2==3.0.1
python-docx==1.1.0
```

2. **Create `render.yaml`** (for backend):
```yaml
services:
  - type: web
    name: student-buddy-api
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: student-buddy-db
          property: connectionString
      - key: GEMINI_API_KEY
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: ALGORITHM
        value: HS256
      - key: ACCESS_TOKEN_EXPIRE_MINUTES
        value: 30

databases:
  - name: student-buddy-db
    databaseName: student_buddy
    user: student_buddy_user
```

#### Step 2: Deploy on Render

1. **Sign up at [render.com](https://render.com)**
2. **Connect your GitHub repository**
3. **Create New Web Service**
   - Select your repository
   - Name: `student-buddy-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Add Environment Variables**:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `SECRET_KEY`: Generate a secure random string
   - `DATABASE_URL`: (Auto-generated if using Render PostgreSQL)
5. **Create PostgreSQL Database** (optional, or use SQLite)
6. **Deploy!**

Your backend will be live at: `https://student-buddy-backend.onrender.com`

---

### **Option B: Deploy to Railway**

1. **Install Railway CLI**:
```bash
npm install -g @railway/cli
```

2. **Login and Initialize**:
```bash
railway login
railway init
```

3. **Deploy Backend**:
```bash
cd backend
railway up
```

4. **Add Environment Variables** in Railway Dashboard:
   - `GEMINI_API_KEY`
   - `SECRET_KEY`
   - `DATABASE_URL` (if using PostgreSQL)

---

## 🎨 Frontend Deployment (React + Vite)

### **Option A: Deploy to Vercel (Recommended)**

#### Step 1: Prepare Frontend

1. **Update `frontend/.env.production`**:
```env
VITE_API_URL=https://your-backend-url.onrender.com
```

2. **Create `vercel.json`** in frontend folder:
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ],
  "buildCommand": "npm run build",
  "outputDirectory": "dist"
}
```

#### Step 2: Deploy to Vercel

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Deploy**:
```bash
cd frontend
vercel
```

3. **Follow prompts**:
   - Link to existing project or create new
   - Set build command: `npm run build`
   - Set output directory: `dist`

4. **Add Environment Variable** in Vercel Dashboard:
   - `VITE_API_URL`: Your backend URL

Your frontend will be live at: `https://your-app.vercel.app`

---

### **Option B: Deploy Frontend to Render**

1. **Create `render.yaml`** for frontend:
```yaml
services:
  - type: web
    name: student-buddy-frontend
    env: static
    buildCommand: cd frontend && npm install && npm run build
    staticPublishPath: frontend/dist
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
    envVars:
      - key: VITE_API_URL
        value: https://your-backend-url.onrender.com
```

2. **Deploy on Render**:
   - Create New Static Site
   - Connect repository
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`

---

### **Option C: Deploy to Netlify**

1. **Create `netlify.toml`** in frontend folder:
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

2. **Deploy**:
```bash
cd frontend
npm install -g netlify-cli
netlify deploy --prod
```

---

## 🗄️ Database Setup

### **Option 1: SQLite (Simple, for testing)**
- Already configured
- File-based database
- ⚠️ Not recommended for production with multiple users

### **Option 2: PostgreSQL (Recommended for Production)**

#### On Render:
1. Create PostgreSQL database in Render dashboard
2. Copy connection string
3. Update backend environment variable:
```env
DATABASE_URL=postgresql://user:password@host:port/database
```

#### Update `backend/app/database.py`:
```python
# For PostgreSQL, change:
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./student_buddy.db"
)

# Add for PostgreSQL compatibility:
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "postgres://", "postgresql://", 1
    )
```

---

## 🔐 Environment Variables

### **Backend Environment Variables**

Create these in your hosting platform:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_super_secret_key_here_min_32_chars

# Optional (with defaults)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./student_buddy.db
ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
```

### **Frontend Environment Variables**

```env
VITE_API_URL=https://your-backend-url.onrender.com
```

---

## 📝 Pre-Deployment Checklist

### Backend:
- [ ] Update CORS origins in `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-url.vercel.app",
        "https://your-frontend-url.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

- [ ] Set secure `SECRET_KEY` (generate with):
```python
import secrets
print(secrets.token_urlsafe(32))
```

- [ ] Add `Procfile` for some platforms:
```
web: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend:
- [ ] Update API URL in `frontend/src/lib/api.ts`:
```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

- [ ] Build and test locally:
```bash
cd frontend
npm run build
npm run preview
```

---

## 🚀 Complete Deployment Steps (Render + Vercel)

### Step 1: Deploy Backend to Render

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your repository
4. Configure:
   - **Name**: student-buddy-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (see above)
6. Click "Create Web Service"
7. Wait for deployment (5-10 minutes)
8. Copy your backend URL: `https://student-buddy-api.onrender.com`

### Step 2: Deploy Frontend to Vercel

1. Update `frontend/.env.production`:
```env
VITE_API_URL=https://student-buddy-api.onrender.com
```

2. Push changes to GitHub
3. Go to [vercel.com](https://vercel.com) → New Project
4. Import your repository
5. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: frontend
   - **Build Command**: `npm run build`
   - **Output Directory**: dist
6. Add environment variable:
   - `VITE_API_URL`: Your Render backend URL
7. Click "Deploy"
8. Your app is live! 🎉

### Step 3: Update CORS

Update `backend/app/main.py` with your Vercel URL:
```python
allow_origins=[
    "https://your-app.vercel.app",
]
```

Push changes and Render will auto-deploy.

---

## 🔍 Post-Deployment Testing

1. **Test Backend API**:
```bash
curl https://your-backend-url.onrender.com/
```

2. **Test Frontend**:
   - Visit your Vercel URL
   - Try signing up
   - Test all features

3. **Check Logs**:
   - Render: Dashboard → Logs
   - Vercel: Dashboard → Deployments → View Function Logs

---

## 💰 Cost Estimates

### Free Tier (Recommended for Students):
- **Render**: Free (with limitations: sleeps after 15 min inactivity)
- **Vercel**: Free (100GB bandwidth/month)
- **Total**: $0/month ✅

### Paid Tier (For Production):
- **Render**: $7/month (always on)
- **Vercel**: Free or $20/month (Pro)
- **PostgreSQL**: $7/month (Render)
- **Total**: ~$14-34/month

---

## 🆘 Troubleshooting

### Backend won't start:
- Check environment variables are set
- Verify `requirements.txt` is complete
- Check logs for errors

### Frontend can't connect to backend:
- Verify `VITE_API_URL` is correct
- Check CORS settings in backend
- Ensure backend is running

### Database errors:
- Check `DATABASE_URL` format
- Verify database is created
- Run migrations if needed

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Deployment](https://vitejs.dev/guide/static-deploy.html)

---

## 🎓 Your Project is Now Live!

Share your deployed app:
- Frontend: `https://your-app.vercel.app`
- Backend API: `https://your-backend.onrender.com`

**Perfect for:**
- Portfolio showcase
- LinkedIn projects
- Final year project demonstration
- Resume/CV

---

**Need Help?** Check the logs in your hosting platform dashboard or refer to the troubleshooting section above.
