import requests

BASE_URL = "http://127.0.0.1:8000"

def verify_validation():
    print("Verifying Participant Validation Endpoint...")
    
    # 1. Test Valid Participant
    try:
        response = requests.get(f"{BASE_URL}/api/participant/P-101")
        if response.status_code == 200:
            data = response.json()
            if data['external_id'] == 'P-101':
                print("✅ Valid Participant (P-101) - OK")
            else:
                print(f"❌ Valid Participant - Data Mismatch: {data}")
        else:
            print(f"❌ Valid Participant - Failed. Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Valid Participant - Exception: {e}")

    # 2. Test Invalid Participant
    try:
        response = requests.get(f"{BASE_URL}/api/participant/INVALID-ID")
        if response.status_code == 404:
            print("✅ Invalid Participant (404) - OK")
        else:
            print(f"❌ Invalid Participant - Failed. Expected 404, got {response.status_code}")
    except Exception as e:
        print(f"❌ Invalid Participant - Exception: {e}")

if __name__ == "__main__":
    verify_validation()
