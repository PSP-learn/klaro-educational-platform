#!/usr/bin/env python3
"""
Quick test script to verify health check endpoint works
"""
import requests
import json

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        # Test locally if running
        local_url = "http://localhost:8000/health"
        
        print("🔍 Testing health check endpoint...")
        
        try:
            response = requests.get(local_url, timeout=10)
            print(f"✅ Status Code: {response.status_code}")
            print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        except requests.exceptions.ConnectionError:
            print("⚠️ Local server not running - this is expected if testing remotely")
        
        # You can also test Railway deployment URL here
        # railway_url = "https://your-app.railway.app/health"
        # response = requests.get(railway_url, timeout=10)
        
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")

def test_root_endpoint():
    """Test the root endpoint"""
    try:
        local_url = "http://localhost:8000/"
        
        print("\n🔍 Testing root endpoint...")
        
        try:
            response = requests.get(local_url, timeout=10)
            print(f"✅ Status Code: {response.status_code}")
            print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        except requests.exceptions.ConnectionError:
            print("⚠️ Local server not running - this is expected if testing remotely")
        
    except Exception as e:
        print(f"❌ Error testing root endpoint: {e}")

if __name__ == "__main__":
    test_root_endpoint()
    test_health_endpoint()
