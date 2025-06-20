import uuid
import hashlib

"""
Unit tests for the Users API endpoints.

Tests cover:
- User creation (success, email already exists)
- Retrieving all users
- Getting user by ID (found and not found)
- Updating a user
- User login with password verification

Mocks the facade layer to simulate database operations.

Assumes `client` and `mocker` fixtures are provided by the test framework.
"""


def test_create_user_success(client, mocker):
    user_data = {
        "first_name": "Jeanne",
        "last_name": "Oscur",
        "email": "j.oscur@example.com",
        "password": "secret123"
    }

    # Mock no existing user found by email
    mocker.patch("app.api.v1.users.facade.get_user_by_email",
                 return_value=None)

    # Mock created user returned by facade
    mock_user = mocker.Mock()
    mock_user.id = uuid.uuid4()
    mock_user.first_name = user_data["first_name"]
    mock_user.last_name = user_data["last_name"]
    mock_user.email = user_data["email"]

    mocker.patch("app.api.v1.users.facade.create_user", return_value=mock_user)

    response = client.post('/api/v1/users/', json=user_data)

    assert response.status_code == 201
    data = response.get_json()
    assert data["email"] == user_data["email"]
    assert data["first_name"] == user_data["first_name"]
    assert data["last_name"] == user_data["last_name"]


def test_create_user_email_exists(client, mocker):
    user_data = {
        "first_name": "Jean",
        "last_name": "Peuplu",
        "email": "jean@example.com",
        "password": "pass"
    }

    # Mock existing user found by email
    existing_user = mocker.Mock()
    mocker.patch("app.api.v1.users.facade.get_user_by_email",
                 return_value=existing_user)

    response = client.post('/api/v1/users/', json=user_data)

    assert response.status_code == 400
    data = response.get_json()
    assert 'Email already registered' in data['error']


def test_get_all_users(client, mocker):
    # Mock two users returned by facade
    user1 = mocker.Mock(id=uuid.uuid4(), first_name="Sylvain",
                        last_name="Téhain", email="sylvain@example.com")
    user2 = mocker.Mock(id=uuid.uuid4(), first_name="Le",
                        last_name="Caillou", email="RoCk@example.com")

    # Simulate model_dump method returning dicts for serialization
    user1.model_dump.return_value = {
        "id": str(user1.id),
        "first_name": user1.first_name,
        "last_name": user1.last_name,
        "email": user1.email
    }
    user2.model_dump.return_value = {
        "id": str(user2.id),
        "first_name": user2.first_name,
        "last_name": user2.last_name,
        "email": user2.email
    }

    mocker.patch("app.api.v1.users.facade.get_all_users",
                 return_value=[user1, user2])

    response = client.get('/api/v1/users/')

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2


def test_get_user_by_id_success(client, mocker):
    user_id = uuid.uuid4()
    user = mocker.Mock(id=user_id, first_name="Lily",
                       last_name="Putien", email="lily@example.com")

    mocker.patch("app.api.v1.users.facade.get_user", return_value=user)

    response = client.get(f'/api/v1/users/{user_id}')

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == str(user_id)


def test_get_user_by_id_not_found(client, mocker):
    user_id = uuid.uuid4()
    mocker.patch("app.api.v1.users.facade.get_user", return_value=None)

    response = client.get(f'/api/v1/users/{user_id}')

    assert response.status_code == 404


def test_update_user_success(client, mocker):
    user_id = uuid.uuid4()
    existing_user = mocker.Mock(id=user_id, first_name="Jean-Philipe",
                                last_name="Smedt", email="jean@example.com")
    updated_user = mocker.Mock(id=user_id, first_name="Johnny",
                               last_name="Halliday", email="ahque@mail.com")

    mocker.patch("app.api.v1.users.facade.get_user",
                 return_value=existing_user)
    mocker.patch("app.api.v1.users.facade.update_user",
                 return_value=updated_user)

    payload = {"first_name": "Johnny"}
    response = client.put(f'/api/v1/users/{user_id}', json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert data["first_name"] == "Johnny"


def test_login_success(client, mocker):
    password = "my_password"
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = mocker.Mock(id=uuid.uuid4(), hashed_password=hashed_password)

    mocker.patch("app.api.v1.users.facade.get_user_by_email",
                 return_value=user)

    payload = {
        "email": "jeann@example.com",

        "password": password
    }

    response = client.post('/api/v1/users/login', json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert "access token" in data
