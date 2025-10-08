# Quick Start Guide

## Installation Steps

### 1. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

This will install the new dependencies:
- PyPDF2 (for PDF processing)
- python-docx (for Word document processing)

### 2. Initialize Database (if not done already)
```bash
python init_db.py
```

### 3. Start Backend Server
```bash
python -m uvicorn app.main:app --reload
```

Backend will run on: http://localhost:8000
API docs available at: http://localhost:8000/docs

### 4. Start Frontend (in a new terminal)
```bash
cd frontend
npm install  # if not done already
npm run dev
```

Frontend will run on: http://localhost:3000

## Testing the Features

### 1. Create Your Profile
- Navigate to "Student Profile"
- Fill in your name, email (optional), learning style, and subjects
- Click "Create Profile"
- Your profile will be saved and statistics will start tracking

### 2. Ask Questions
- Go to "Ask a Question"
- Type: "What is photosynthesis?"
- Choose explanation style: "Simple"
- Click "Ask Question"
- You'll get a detailed step-by-step answer

### 3. Generate Quiz from File
- Go to "Take a Quiz"
- Check "Upload study material"
- Upload a PDF, TXT, or DOCX file with study content
- Select difficulty: "Medium"
- Select 5 questions
- Click "Generate Quiz"
- Answer the questions and see your score

### 4. Summarize Notes from File
- Go to "Summarize Notes"
- Check "Upload document"
- Upload your study material
- Choose format: "Bullet Points"
- Click "Summarize Notes"
- Get a concise summary with key terms

## Supported File Formats

- **PDF** (.pdf) - Portable Document Format
- **Text** (.txt) - Plain text files
- **Word** (.docx, .doc) - Microsoft Word documents

**Maximum file size**: 10MB

## Troubleshooting

### Backend Issues

**Error: "GEMINI_API_KEY is required"**
- Make sure you have a `.env` file with your Gemini API key
- Get your key from: https://makersuite.google.com/app/apikey

**Error: "Module not found: PyPDF2"**
```bash
pip install PyPDF2 python-docx
```

**Error: "Could not extract text from file"**
- Make sure the file contains readable text
- Scanned PDFs (images) won't work - they need OCR

### Frontend Issues

**Error: "Cannot connect to backend"**
- Make sure backend is running on port 8000
- Check CORS settings in `app/main.py`

**Profile not saving**
- Check browser console for errors
- Make sure localStorage is enabled

## Features Overview

### ✅ Ask Questions
- Get AI-powered answers to any academic question
- Choose from 3 explanation styles
- See step-by-step explanations
- Discover related topics

### ✅ Generate Quizzes
- Create quizzes from any topic OR uploaded materials
- Multiple choice and true/false questions
- Adjustable difficulty levels
- Instant feedback with explanations

### ✅ Summarize Notes
- Convert long documents into concise summaries
- 4 different summary formats
- Extract key terms and main topics
- Calculate reading time and compression ratio

### ✅ Student Profile
- Track your learning progress
- View comprehensive statistics
- Monitor learning streaks
- See most studied topics

## Next Steps

1. Create your student profile
2. Upload some study materials
3. Generate quizzes to test your knowledge
4. Summarize long documents for quick review
5. Ask questions when you need clarification

Happy learning! 📚✨
