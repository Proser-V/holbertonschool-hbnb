import requests

BASE_URL = "http://localhost:5001/api/v1"

print("========== Running the users tests ==========")

# Testing user creation
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
    elif res.status_code == 400 and res.json().get("error") == "Email already registered":
        return None
    else:
        raise Exception(f"Unexpected response: {res.status_code} - {res.text}")

user1_id = register("user1@example.com")
assert user1_id is not None
user2_id = register("user1@example.com")
assert user2_id is None
user3_id = register("user2@example.com")
assert user3_id is not None

# Testing admin creation without login
res = requests.post(f"{BASE_URL}/users/admin_creation", json={
    "email": "admin@mail.com",
    "password": "password",
    "first_name": "AdminTest",
    "last_name": "AdminTest"
})

print("Status:", res.status_code)
try:
    print("Body:", res.json())
except ValueError:
    print("Body (non-JSON):", res.text)

# Login user
res = requests.post(f"{BASE_URL}/users/login", json={
    "email": "user1@example.com",
    "password": "123456"
})

token = res.json().get("access_token")
assert token, "No access token received"

# Add Authorization header
headers = {
    "Authorization": f"Bearer {token}"
}

# User tries to create an admin
res = requests.post(f"{BASE_URL}/users/admin_creation", json={
    "email": "admin@mail.com",
    "password": "password",
    "first_name": "Admin",
    "last_name": "Test"
}, headers=headers)

print("Admin creation status:", res.status_code)
try:
    print("Admin creation response:", res.json())
except ValueError:
    print("Non-JSON response:", res.text)

# User tries to delete another user
res = requests.delete(f"{BASE_URL}/users/{user3_id}", headers=headers)
print("Status:", res.status_code)
try:
    print("Body:", res.json())
except ValueError:
    print("Body (non-JSON):", res.text)

# User try to update another user
res = requests.put(f"{BASE_URL}/users/{user3_id}", headers=headers)
print("Status:", res.status_code)
try:
    print("Body:", res.json())
except ValueError:
    print("Body (non-JSON):", res.text)

# User try to update itself
payload = {
    "first_name": "UpdatedName",
    "last_name": "UpdatedLast"
}
res = requests.put(f"{BASE_URL}/users/{user1_id}", json=payload, headers=headers)
print("Status:", res.status_code)
try:
    print("Body:", res.json())
except ValueError:
    print("Body (non-JSON):", res.text)

# User deletes itself
res = requests.delete(f"{BASE_URL}/users/{user1_id}", headers=headers)
print("Status:", res.status_code)
try:
    print("Body:", res.json())
except ValueError:
    print("Body (non-JSON):", res.text)


# Login an admin
res = requests.post(f"{BASE_URL}/users/login", json= {
    "email": "admin@hbnb.com",
    "password": "Iamanadmin"
})

token = res.json().get("access_token")

# Add Authorization header
headers = {
    "Authorization": f"Bearer {token}"
}

# Create a new admin
res = requests.post(f"{BASE_URL}/users/admin_creation", json={
    "email": "admin@mail.com",
    "password": "password",
    "first_name": "Admin",
    "last_name": "Test",
    "is_admin": True
}, headers=headers)
try:
    data = res.json()
except ValueError:
    print("Non-JSON response:", res.text)
    raise

admin_id = data.get("id")
print("Admin creation status:", res.status_code)
print("Admin creation response:", data)

# Delete an user
res = requests.delete(f"{BASE_URL}/users/{user3_id}", headers=headers)
print("Status:", res.status_code)
try:
    print("Body:", res.json())
except ValueError:
    print("Body (non-JSON):", res.text)

# Delete the admin
res = requests.delete(f"{BASE_URL}/users/{admin_id}", headers=headers)
print("Status:", res.status_code)
try:
    print("Body:", res.json())
except ValueError:
    print("Body (non-JSON):", res.text)
