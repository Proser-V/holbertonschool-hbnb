import requests


BASE_URL = "http://localhost:5001/api/v1"

print("========== Running the amenities test ==========")

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

# Create a new amenity
res = requests.post(f"{BASE_URL}/amenities", json={
    "name": "Un tabouret d'entraînement",
    "description": "Un tabouret tout ce qu'il y a de plus normal"
}, headers=headers)

print("Status:", res.status_code)
try:
    data = res.json()
except ValueError:
    print("Body (Non-JSON):", res.text)

amenity_id = data.get("id")

# Create a user
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

user_id = register("user1@example.com")
assert user_id is not None

# Login the user
res = requests.post(f"{BASE_URL}/users/login", json={
    "email": "user1@example.com",
    "password": "123456"
})

token = res.json().get("access_token")

# Update the authorization header
headers = {"Authorization": f"Bearer {token}"}

# User try to create an amenity
res = requests.post(f"{BASE_URL}/amenities", json={
    "name": "Amenity test",
    "description": "C'est une description"
}, headers=headers)

print("Status:", res.status_code)
try:
    print("Body:", res.json())
except ValueError:
    print("Body (Non-JSON):", res.text)

# Re log the admin
res = requests.post(f"{BASE_URL}/users/login", json={
    "email": "admin@hbnb.com",
    "password": "Iamanadmin"
})

token = res.json().get("access_token")

# Update the Authorization header
headers = {"Authorization": f"Bearer {token}"}


# Update the amenity
res = requests.put(f"{BASE_URL}/amenities/{amenity_id}", json={
    "name": "Le tabouret est changé"
}, headers=headers)

print("Status:", res.status_code)
try:
    print("Body:", res.json())
except ValueError:
    print("Body (Non-JSON):", res.text)

# Delete the amenity
res = requests.delete(f"{BASE_URL}/amenities/{amenity_id}", headers=headers)
print("Status:", res.status_code)
try:
    print("Body:", res.json())
except ValueError:
    print("Body (Non-JSON):", res.text)

# Delete the user
res = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
print("Status:", res.status_code)
try:
    print("Body:", res.json())
except ValueError:
    print("Body (Non-JSON):", res.text)
