
import requests
import json

try:
    r = requests.get("http://localhost:8000/api/products/")
    if r.status_code == 200:
        data = r.json()
        if data:
            p = data[0]
            if 'images' in p:
                p['images'] = [f"{len(img)} bytes" for img in p['images']]
            print(json.dumps(p, indent=2))
        else:
            print("Empty list")
    else:
        print(f"Error {r.status_code}")
except Exception as e:
    print(e)
