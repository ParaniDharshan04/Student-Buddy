#!/usr/bin/env python3
"""Test API endpoints"""

import asyncio
import os

# Set environment variable
os.environ["GEMINI_API_KEY"] = "AIzaSyBiS_m146g3MVXN2D8VefxvEq8Hk5IBbxA"

from app.services.ai_service import AIService
from app.services.quiz_service import QuizService
from app.services.notes_service import NotesService

async def test_question():
    print("\n=== Testing Question Service ===")
    try:
        ai_service = AIService()
        result = await ai_service.answer_question("What is 2+2?", "simple")
        print("✅ Question service works!")
        print(f"Answer: {result['answer'][:100]}...")
    except Exception as e:
        print(f"❌ Question service failed: {e}")

async def test_quiz():
    print("\n=== Testing Quiz Service ===")
    try:
        quiz_service = QuizService()
        result = await quiz_service.generate_quiz("Mathematics", 3, "easy")
        print("✅ Quiz service works!")
        print(f"Generated {len(result['questions'])} questions")
    except Exception as e:
        print(f"❌ Quiz service failed: {e}")

async def test_notes():
    print("\n=== Testing Notes Service ===")
    try:
        notes_service = NotesService()
        result = await notes_service.summarize_content(
            "Python is a programming language. It is easy to learn and powerful.",
            "bullet_points"
        )
        print("✅ Notes service works!")
        print(f"Summary length: {result['summary_length']} chars")
    except Exception as e:
        print(f"❌ Notes service failed: {e}")

async def main():
    await test_question()
    await test_quiz()
    await test_notes()

if __name__ == "__main__":
    asyncio.run(main())
