#!/usr/bin/env python3
"""Test Gemini API connection with direct key"""

import google.generativeai as genai

api_key = "AIzaSyBiS_m146g3MVXN2D8VefxvEq8Hk5IBbxA"

print(f"Testing Gemini API...")
print(f"API Key length: {len(api_key)}")
print(f"Model: gemini-2.5-flash")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    print("\nSending test request...")
    response = model.generate_content("What is 2+2? Answer in one sentence.")
    
    print(f"\n✅ Success!")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print(f"Error type: {type(e).__name__}")
