"""
Diagnostic script to identify 500 errors
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def diagnose():
    print("=" * 60)
    print("Diagnosing 500 Error")
    print("=" * 60)
    
    # Step 1: Check if backend is running
    print("\n1. Checking backend health...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✓ Backend is running")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ✗ Backend returned: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ Cannot connect to backend: {e}")
        print(f"   Make sure backend is running on port 8000")
        return
    
    # Step 2: Test signup
    print("\n2. Testing signup...")
    signup_data = {
        "email": "diagnostic@test.com",
        "username": "diaguser",
        "password": "test123",
        "full_name": "Diagnostic User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            print(f"   ✓ Signup successful")
            data = response.json()
            token = data.get("token")
            user_id = data.get("user_id")
            student_id = data.get("student_id")
            print(f"   User ID: {user_id}")
            print(f"   Student ID: {student_id}")
            print(f"   Token: {token[:20]}...")
            
            # Step 3: Test protected endpoint
            print("\n3. Testing protected endpoint (profile)...")
            headers = {"Authorization": f"Bearer {token}"}
            
            try:
                profile_response = requests.get(f"{BASE_URL}/api/profile", headers=headers, timeout=10)
                print(f"   Status: {profile_response.status_code}")
                
                if profile_response.status_code == 200:
                    print(f"   ✓ Profile retrieved successfully")
                    print(f"   Data: {profile_response.json()}")
                elif profile_response.status_code == 404:
                    print(f"   ℹ Profile not found (expected for new user)")
                elif profile_response.status_code == 500:
                    print(f"   ✗ 500 ERROR FOUND!")
                    print(f"   Response: {profile_response.text}")
                    print(f"\n   Check backend logs for detailed error message")
                else:
                    print(f"   Status: {profile_response.status_code}")
                    print(f"   Response: {profile_response.text}")
            except Exception as e:
                print(f"   ✗ Request failed: {e}")
            
            # Step 4: Test question endpoint
            print("\n4. Testing question endpoint...")
            question_data = {
                "question": "What is 2+2?",
                "explanation_style": "simple"
            }
            
            try:
                question_response = requests.post(
                    f"{BASE_URL}/api/ask",
                    json=question_data,
                    headers=headers,
                    timeout=30
                )
                print(f"   Status: {question_response.status_code}")
                
                if question_response.status_code == 200:
                    print(f"   ✓ Question answered successfully")
                elif question_response.status_code == 500:
                    print(f"   ✗ 500 ERROR FOUND!")
                    print(f"   Response: {question_response.text}")
                    print(f"\n   Check backend logs for detailed error message")
                else:
                    print(f"   Response: {question_response.text}")
            except Exception as e:
                print(f"   ✗ Request failed: {e}")
                
        elif response.status_code == 400:
            print(f"   ℹ User already exists")
            print(f"   Run: python clear_all_users.py")
            print(f"   Then run this diagnostic again")
        elif response.status_code == 500:
            print(f"   ✗ 500 ERROR FOUND!")
            print(f"   Response: {response.text}")
            print(f"\n   Check backend logs for detailed error message")
        else:
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ✗ Request failed: {e}")
    
    print("\n" + "=" * 60)
    print("Diagnostic Complete")
    print("=" * 60)
    print("\nIf you see 500 errors above:")
    print("1. Check the backend terminal for error details")
    print("2. Look for Python traceback messages")
    print("3. Share the error message for help")

if __name__ == "__main__":
    diagnose()
