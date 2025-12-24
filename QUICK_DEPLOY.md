# ⚡ Quick Deploy Guide - 15 Minutes to Live!

## 🎯 Fastest Way to Deploy (Render + Vercel)

### Prerequisites
- GitHub account
- Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

---

## 📦 Step 1: Prepare Your Code (2 minutes)

1. **Push to GitHub**:
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Generate a SECRET_KEY**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Copy this key - you'll need it!

---

## 🔧 Step 2: Deploy Backend to Render (5 minutes)

1. **Go to [render.com](https://render.com)** and sign up with GitHub

2. **Click "New +" → "Web Service"**

3. **Connect your repository**

4. **Configure the service**:
   - **Name**: `student-buddy-api`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Build Command**: 
     ```
     pip install -r backend/requirements.txt
     ```
   - **Start Command**: 
     ```
     cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

5. **Add Environment Variables** (Click "Advanced" → "Add Environment Variable"):
   ```
   GEMINI_API_KEY = your_gemini_api_key_here
   SECRET_KEY = your_generated_secret_key_here
   ALGORITHM = HS256
   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   ```

6. **Click "Create Web Service"**

7. **Wait 5-10 minutes** for deployment

8. **Copy your backend URL**: `https://student-buddy-api.onrender.com`

---

## 🎨 Step 3: Deploy Frontend to Vercel (5 minutes)

1. **Update frontend/.env.production**:
   ```env
   VITE_API_URL=https://student-buddy-api.onrender.com
   ```
   (Replace with YOUR actual Render URL)

2. **Commit and push**:
   ```bash
   git add frontend/.env.production
   git commit -m "Update production API URL"
   git push
   ```

3. **Go to [vercel.com](https://vercel.com)** and sign up with GitHub

4. **Click "Add New..." → "Project"**

5. **Import your repository**

6. **Configure the project**:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)

7. **Add Environment Variable**:
   - Click "Environment Variables"
   - **Key**: `VITE_API_URL`
   - **Value**: `https://student-buddy-api.onrender.com` (your Render URL)

8. **Click "Deploy"**

9. **Wait 2-3 minutes**

10. **Your app is LIVE!** 🎉
    - Copy your URL: `https://your-app.vercel.app`

---

## 🔄 Step 4: Update CORS (2 minutes)

1. **Update `backend/app/config.py`**:
   
   Find the `ALLOWED_ORIGINS` line and add your Vercel URL:
   ```python
   ALLOWED_ORIGINS: str = "http://localhost:3000,https://your-app.vercel.app"
   ```

2. **Commit and push**:
   ```bash
   git add backend/app/config.py
   git commit -m "Update CORS for production"
   git push
   ```

3. **Render will auto-deploy** (wait 2-3 minutes)

---

## ✅ Step 5: Test Your App (1 minute)

1. **Visit your Vercel URL**: `https://your-app.vercel.app`

2. **Test the features**:
   - Sign up with a new account
   - Ask a question
   - Generate a quiz
   - Try voice chat

3. **If something doesn't work**:
   - Check Render logs: Dashboard → Logs
   - Check Vercel logs: Dashboard → Deployments → View Function Logs
   - Verify environment variables are set correctly

---

## 🎊 You're Done!

Your AI Learning Platform is now live and accessible worldwide!

### Share Your Project:
- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://student-buddy-api.onrender.com`
- **API Docs**: `https://student-buddy-api.onrender.com/docs`

### Add to Your Portfolio:
- LinkedIn Projects section
- GitHub README
- Resume/CV
- Final year project report

---

## 💡 Pro Tips

### Free Tier Limitations:
- **Render Free**: Backend sleeps after 15 min of inactivity (first request takes ~30 seconds to wake up)
- **Vercel Free**: 100GB bandwidth/month (plenty for personal projects)

### To Keep Backend Always On:
- Upgrade to Render paid plan ($7/month)
- Or use a cron job to ping your backend every 10 minutes

### Custom Domain (Optional):
1. Buy a domain (e.g., from Namecheap, GoDaddy)
2. In Vercel: Settings → Domains → Add your domain
3. Update DNS records as instructed

---

## 🆘 Common Issues

### Backend Error 500:
- Check `GEMINI_API_KEY` is set correctly
- Verify `SECRET_KEY` is set
- Check Render logs for details

### Frontend Can't Connect:
- Verify `VITE_API_URL` in Vercel environment variables
- Check CORS settings in backend
- Make sure backend is running (visit the URL)

### Database Errors:
- SQLite works fine for free tier
- For production with many users, upgrade to PostgreSQL

---

## 📊 Monitor Your App

### Render Dashboard:
- View logs
- Check metrics
- Monitor uptime

### Vercel Dashboard:
- View analytics
- Check deployment status
- Monitor bandwidth usage

---

## 🚀 Next Steps

1. **Add Custom Domain** (optional)
2. **Set up PostgreSQL** for better performance
3. **Add monitoring** (e.g., Sentry for error tracking)
4. **Optimize performance** (caching, CDN)
5. **Add more features** and iterate!

---

**Congratulations!** 🎉 Your project is now live and ready to showcase!
