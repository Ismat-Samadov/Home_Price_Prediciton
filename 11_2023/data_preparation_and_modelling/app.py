import json

import requests

url = "http://localhost:8000/predict/"
data = {
    "is_near_metro": 1,
    "seller_type_encoded": 0,
    "flat": 2,
    "total_flat": 5,
    "room_count": 3,
    "area_converted": 80.5,
    "category_encoded": 1,
    "documents_encoded": 0,
    "is_repair_encoded": 1
}

response = requests.post(url, json=data)
if response.status_code == 200:
    try:
        result = response.json()
        print(result)
    except json.decoder.JSONDecodeError:
        print("Invalid JSON response from the server")
else:
    print(f"Request failed with status code {response.status_code}")