#!/bin/bash

# Student Learning Buddy - Deployment Helper Script
# This script helps you prepare your project for deployment

echo "🚀 Student Learning Buddy - Deployment Helper"
echo "=============================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Git repository not initialized!"
    echo "Run: git init"
    exit 1
fi

echo "✅ Git repository found"
echo ""

# Check for uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo "⚠️  You have uncommitted changes!"
    echo "Commit them before deploying:"
    echo "  git add ."
    echo "  git commit -m 'Ready for deployment'"
    echo ""
fi

# Generate SECRET_KEY
echo "🔐 Generating SECRET_KEY..."
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || python -c "import secrets; print(secrets.token_urlsafe(32))")
echo "Your SECRET_KEY: $SECRET_KEY"
echo "⚠️  Save this key! You'll need it for deployment."
echo ""

# Check for required files
echo "📋 Checking deployment files..."

files=(
    "backend/requirements.txt"
    "frontend/package.json"
    "render.yaml"
    "Procfile"
    "frontend/vercel.json"
)

all_good=true
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (missing)"
        all_good=false
    fi
done

echo ""

if [ "$all_good" = true ]; then
    echo "✅ All deployment files are ready!"
else
    echo "❌ Some files are missing. Please check the deployment guide."
    exit 1
fi

# Check environment variables
echo "🔍 Checking environment variables..."
echo ""

if [ -f "backend/.env" ]; then
    if grep -q "GEMINI_API_KEY" backend/.env; then
        echo "✅ GEMINI_API_KEY found in backend/.env"
    else
        echo "⚠️  GEMINI_API_KEY not found in backend/.env"
    fi
else
    echo "⚠️  backend/.env file not found"
fi

echo ""
echo "📝 Deployment Checklist:"
echo "========================"
echo ""
echo "Backend (Render):"
echo "  1. Push code to GitHub"
echo "  2. Create Web Service on Render"
echo "  3. Set environment variables:"
echo "     - GEMINI_API_KEY"
echo "     - SECRET_KEY (use the one generated above)"
echo "     - ALGORITHM=HS256"
echo "  4. Deploy and copy backend URL"
echo ""
echo "Frontend (Vercel):"
echo "  1. Update frontend/.env.production with backend URL"
echo "  2. Push changes to GitHub"
echo "  3. Import project on Vercel"
echo "  4. Set VITE_API_URL environment variable"
echo "  5. Deploy"
echo ""
echo "Final Step:"
echo "  Update CORS in backend/app/config.py with your Vercel URL"
echo ""
echo "📚 For detailed instructions, see:"
echo "  - DEPLOYMENT_GUIDE.md (comprehensive guide)"
echo "  - QUICK_DEPLOY.md (15-minute quick start)"
echo ""
echo "🎉 Good luck with your deployment!"
