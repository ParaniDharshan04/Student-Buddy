"""
Test script to verify authentication token system
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_auth_flow():
    print("=" * 60)
    print("Testing Authentication Token Flow")
    print("=" * 60)
    
    # Test 1: Signup
    print("\n1. Testing Signup...")
    signup_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "full_name": "Test User"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        token = data.get("token")
        print(f"   ✓ Signup successful")
        print(f"   Token: {token[:20]}...")
        
        # Test 2: Use token to access protected endpoint
        print("\n2. Testing Protected Endpoint (Profile)...")
        headers = {"Authorization": f"Bearer {token}"}
        
        profile_response = requests.get(f"{BASE_URL}/api/profile", headers=headers)
        print(f"   Status: {profile_response.status_code}")
        
        if profile_response.status_code == 200:
            print(f"   ✓ Profile access successful")
        elif profile_response.status_code == 404:
            print(f"   ℹ Profile not found (expected for new user)")
        else:
            print(f"   ✗ Failed: {profile_response.text}")
        
        # Test 3: Try without token
        print("\n3. Testing Without Token...")
        no_auth_response = requests.get(f"{BASE_URL}/api/profile")
        print(f"   Status: {no_auth_response.status_code}")
        
        if no_auth_response.status_code == 401:
            print(f"   ✓ Correctly rejected (401)")
        else:
            print(f"   ✗ Should have been rejected")
        
        # Test 4: Login with same credentials
        print("\n4. Testing Login...")
        login_data = {
            "email": "testuser",
            "password": "password123"
        }
        
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"   Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            new_token = login_data.get("token")
            print(f"   ✓ Login successful")
            print(f"   New Token: {new_token[:20]}...")
            
            # Test 5: Use new token
            print("\n5. Testing New Token...")
            headers = {"Authorization": f"Bearer {new_token}"}
            
            profile_response = requests.get(f"{BASE_URL}/api/profile", headers=headers)
            print(f"   Status: {profile_response.status_code}")
            
            if profile_response.status_code in [200, 404]:
                print(f"   ✓ New token works")
            else:
                print(f"   ✗ New token failed: {profile_response.text}")
        else:
            print(f"   ✗ Login failed: {login_response.text}")
    
    elif response.status_code == 400:
        print(f"   ℹ User already exists (run clear_all_users.py first)")
    else:
        print(f"   ✗ Signup failed: {response.text}")
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    test_auth_flow()
