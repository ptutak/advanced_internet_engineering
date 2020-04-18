import requests
from pprint import pformat

session = requests.Session()

session.post("http://127.0.0.1:5000/auth/login", {"username": "admin", "password": "admin"})

response = session.get("http://127.0.0.1:5000/api/users/read")

print(pformat(response.json()))

response = session.get("http://127.0.0.1:5000/api/profiles/read")

print(pformat(response.json()))

response = session.get("http://127.0.0.1:5000/api/orrrders/read")

print(pformat(response.json()))
