import requests
import json
from pprint import pformat

session = requests.Session()

response = session.post(
    "http://127.0.0.1:5000/auth/login", data={"username": "admin", "password": "admin"}
)

response = session.get("http://127.0.0.1:5000/api/users")

print(pformat(response.json()))

response = session.get("http://127.0.0.1:5000/api/profiles")

print(pformat(response.json()))

response = session.get("http://127.0.0.1:5000/api/orders")

print(pformat(response.json()))

response = session.post(
    "http://127.0.0.1:5000/api/products",
    json={
        "name": "Red Table",
        "image": "red_table.png",
        "price": "2.50",
        "id_category": 1,
    },
)

print(response.text)

response = session.get("http://127.0.0.1:5000/api/products")

print(pformat(response))
