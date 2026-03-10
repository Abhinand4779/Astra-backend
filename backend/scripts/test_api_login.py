import requests

def test_login():
    url = "http://localhost:8000/api/auth/login"
    data = {
        "username": "admin@astra.in",
        "password": "admin123"
    }
    response = requests.post(url, data=data)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print(f"Raw Response: {response.text}")

if __name__ == "__main__":
    try:
        test_login()
    except Exception as e:
        print(f"Error: {e}")
