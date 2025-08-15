import time
import requests
import os

# Get your Dhan API token from environment variables (Render -> Environment)
DHAN_API_KEY = os.getenv("DHAN_API_KEY")

# Example endpoint - you can replace with actual strategy logic
BASE_URL = "https://api.dhan.co"

def place_order():
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "access-token": DHAN_API_KEY
    }
    
    payload = {
        "transactionType": "BUY",
        "exchangeSegment": "NSE_EQ",
        "productType": "INTRADAY",
        "orderType": "MARKET",
        "validity": "DAY",
        "securityId": "11536",  # Example: RELIANCE
        "quantity": 1
    }
    
    r = requests.post(f"{BASE_URL}/orders", json=payload, headers=headers)
    print("Order Response:", r.json())

if __name__ == "__main__":
    while True:
        place_order()
        time.sleep(60)  # wait 1 min before next order
