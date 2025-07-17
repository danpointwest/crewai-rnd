import requests
import json

url = "https://gwoo0j57e4.execute-api.us-east-1.amazonaws.com/dev/trigger"

payload = {
    "message": "Hello test streamlitss"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status code:", response.status_code)
try:
    print("Response JSON:", response.json())
except Exception:
    print("Response Text:", response.text)
