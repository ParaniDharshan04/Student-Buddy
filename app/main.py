from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import routers
from app.api.question import router as question_router
from app.api.quiz import router as quiz_router
from app.api.notes import router as notes_router
from app.api.profile import router as profile_router
from app.api.upload import router as upload_router
from app.api.auth import router as auth_router
from app.api.voice_chat import router as voice_chat_router

app = FastAPI(
    title="Student Learning Buddy API",
    description="AI-powered personal tutor for students using Google Gemini",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(question_router)
app.include_router(quiz_router)
app.include_router(notes_router)
app.include_router(profile_router)
app.include_router(upload_router)
app.include_router(voice_chat_router)

@app.get("/")
async def root():
    return {"message": "Student Learning Buddy API is running with Google Gemini!"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": "1.0.0",
        "ai_provider": "Google Gemini"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)