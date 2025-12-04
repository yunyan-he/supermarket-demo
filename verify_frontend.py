import requests

BASE_URL = "http://127.0.0.1:8000"

def verify_frontend():
    print("Verifying Frontend Routes...")
    
    # 1. Verify Root (POS)
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200 and "<title>Lab Supermarket POS</title>" in response.text:
            print("✅ GET / (POS) - OK")
        else:
            print(f"❌ GET / (POS) - Failed. Status: {response.status_code}")
    except Exception as e:
        print(f"❌ GET / (POS) - Exception: {e}")

    # 2. Verify Admin (Dashboard)
    try:
        response = requests.get(f"{BASE_URL}/admin")
        if response.status_code == 200 and "<title>Research Dashboard</title>" in response.text:
            print("✅ GET /admin (Dashboard) - OK")
        else:
            print(f"❌ GET /admin (Dashboard) - Failed. Status: {response.status_code}")
    except Exception as e:
        print(f"❌ GET /admin (Dashboard) - Exception: {e}")

if __name__ == "__main__":
    verify_frontend()
