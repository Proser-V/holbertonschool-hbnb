"""
This module provides a testing suite for places CRUD.
"""


import requests

BASE_URL = "http://localhost:5001/api/v1"

print("========== Running the places tests ==========")


# Create a new set of users
def register(email):
    res = requests.post(f"{BASE_URL}/users", json={
        "email": email,
        "password": "123456",
        "first_name": "User",
        "last_name": "Test"
    })
    print(f"Register {email} => {res.status_code} | {res.json()}")

    if res.status_code == 201:
        return res.json()["id"]
    elif (res.status_code == 400 and res.json().get("error")
          == "Email already registered"):
        return None
    else:
        raise Exception(f"Unexpected response: {res.status_code} - {res.text}")


user1_id = register("user1@example.com")
user2_id = register("user2@example.com")

# Login user
res = requests.post(f"{BASE_URL}/users/login", json={
    "email": "user1@example.com",
    "password": "123456"
})

token = res.json().get("access_token")

# Add Authorization header
headers = {
    "Authorization": f"Bearer {token}"
}

# Register a new place
res = requests.post(f"{BASE_URL}/places", json={
    "title": "Maion de test",
    "description": "C'est une maison en forme de maison",
    "price": 23.4243,
    "latitude": 23.4232,
    "longitude": 42.424242
}, headers=headers)
print("Status:", res.status_code)
try:
    data = res.json()
except ValueError:
    print("Body (Non-JSON):", res.text)

place_id = data.get("id")

# Update the place
res = requests.put(f"{BASE_URL}/places/{place_id}", json={
    "title": "C'est une maison modifiée"
}, headers=headers)
print("Status:", res.status_code)
try:
    print("Body:", res.json())
except ValueError:
    print("Body (Non-JSON):", res.text)

# Login the second user
res = requests.post(f"{BASE_URL}/users/login", json={
    "email": "user2@example.com",
    "password": "123456"
})

token = res.json().get("access_token")
assert token, "No access token"

# Modify the authorization header
headers = {"Authorization": f"Bearer {token}"}

# User2 tries to delete user1 place
res = requests.delete(f"{BASE_URL}/places/{place_id}", headers=headers)
print("Status", res.status_code)
try:
    print("Body:", res.json())
except ValueError:
    print("Body (Non-JSON):", res.text)

# User2 deletes itself (keep the DB clean)
res = requests.delete(f"{BASE_URL}/users/{user2_id}", headers=headers)
print("Status:", res.status_code)
try:
    print("Body:", res.json())
except ValueError:
    print("Body (Non-JSON):", res.text)

# User1 log again
res = requests.post(f"{BASE_URL}/users/login", json={
    "email": "user1@example.com",
    "password": "123456"
})

token = res.json().get("access_token")

# Return the good authorization header
headers = {"Authorization": f"Bearer {token}"}


# Delete an user, this also delete the place created
res = requests.delete(f"{BASE_URL}/users/{user1_id}", headers=headers)
print("Status:", res.status_code)
try:
    print("Body:", res.json())
except ValueError:
    print("Body (non-JSON):", res.text)
