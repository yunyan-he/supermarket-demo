import requests
import pandas as pd
import io

BASE_URL = "http://127.0.0.1:8000"

def verify_export():
    print("Verifying Export Endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/export/csv")
        
        if response.status_code == 200:
            print("✅ GET /api/export/csv - OK")
            
            # Verify Content-Type
            content_type = response.headers.get("Content-Type")
            if "text/csv" in content_type:
                print("✅ Content-Type is text/csv")
            else:
                print(f"❌ Content-Type mismatch: {content_type}")
            
            # Verify Content
            csv_content = response.content.decode('utf-8')
            df = pd.read_csv(io.StringIO(csv_content))
            
            print("CSV Columns:", df.columns.tolist())
            print(f"Rows: {len(df)}")
            
            required_columns = [
                "transaction_id", "timestamp", "participant_external_id",
                "participant_group", "product_name", "product_barcode",
                "quantity", "price_paid"
            ]
            
            missing_cols = [col for col in required_columns if col not in df.columns]
            if not missing_cols:
                print("✅ All required columns present")
            else:
                print(f"❌ Missing columns: {missing_cols}")
                
        else:
            print(f"❌ GET /api/export/csv - Failed. Status: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    verify_export()
