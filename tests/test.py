import requests

session = requests.Session()

session.post("http://127.0.0.1:5000/auth/login", {"username": "admin", "password": "admin"})

response = session.get("http://127.0.0.1:5000/api/users/read")

print(response.text)
