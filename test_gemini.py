#!/usr/bin/env python3
"""Test Gemini API connection"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API key directly
api_key = os.getenv("GEMINI_API_KEY", "").strip("'\"")

print(f"Testing Gemini API...")
print(f"API Key loaded: {'Yes' if api_key else 'No'}")
print(f"API Key length: {len(api_key)}")
print(f"API Key preview: {api_key[:10]}..." if api_key else "No key found")
print(f"Model: gemini-2.5-flash")

try:
    if not api_key:
        raise ValueError("No API key found in .env file")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    print("\nSending test request...")
    response = model.generate_content("What is 2+2? Answer in one sentence.")
    
    print(f"\n✅ Success!")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print(f"Error type: {type(e).__name__}")
