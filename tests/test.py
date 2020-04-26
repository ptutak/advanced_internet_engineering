import requests
import json
from pprint import pformat

session = requests.Session()

response = session.post(
    "http://127.0.0.1:5000/auth/login", data={"username": "admin", "password": "admin"}
)

response = session.get("http://127.0.0.1:5000/api/v1/users")

print(pformat(response.json()))

response = session.get("http://127.0.0.1:5000/api/v1/profiles")

print(pformat(response.json()))

response = session.get("http://127.0.0.1:5000/api/v1/orders")

print(pformat(response.json()))

response = session.get("http://127.0.0.1:5000/api/v1/products")

print(pformat(response.json()))
