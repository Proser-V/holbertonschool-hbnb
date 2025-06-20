import uuid
from unittest.mock import patch, MagicMock

"""
Unit tests for the Places API endpoints.

These tests mock the facade layer to simulate database
interactions without real persistence.

Covered tests include:
- Creating a place
- Retrieving all places
- Getting a place by ID
- Updating a place
- Deleting a place

The `MagicMock` class is used to simulate Place model instances.

Test fixtures `client` and `user_token` are assumed
available from the test setup.
"""


@patch('app.api.v1.places.facade')
def test_create_place(mock_facade, client, user_token):
    # Arrange: mock token, user ID, and the created place object
    token, user_id = user_token
    mock_place = MagicMock()
    mock_place.id = str(uuid.uuid4())
    mock_place.title = "Maison"
    mock_place.description = "En pain d'épices"
    mock_place.price = 42.0
    mock_place.latitude = 45.0
    mock_place.longitude = 5.0
    mock_place.amenities = []
    mock_place.owner_id = user_id
    mock_facade.create_place.return_value = mock_place

    payload = {
        "title": "Maison",
        "description": "En pain d'épices",
        "price": 100.0,
        "latitude": 45.0,
        "longitude": 5.0,
        "amenity_ids": []
    }

    # Act: send POST request to create place
    response = client.post(
        '/api/v1/places/',
        json=payload,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )

    # Assert: place created successfully, title matches
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == "Maison"


@patch('app.api.v1.places.facade')
def test_get_places(mock_facade, client):
    # Arrange: mock a list with one place
    mock_place = MagicMock()
    mock_place.id = str(uuid.uuid4())
    mock_place.title = "Château"
    mock_place.description = "Ambulant (ou dans le Ciel)"
    mock_place.price = 26473.0
    mock_place.latitude = 27.0
    mock_place.longitude = -121.0
    mock_place.amenities = []

    mock_facade.place_repo.get_all.return_value = [mock_place]

    # Act: send GET request to list places
    response = client.get('/api/v1/places/')

    # Assert: returns list containing our mocked place
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == "Château"


@patch('app.api.v1.places.facade')
def test_get_place_by_id(mock_facade, client):
    # Arrange: mock a specific place with known ID
    place_id = uuid.uuid4()

    mock_place = MagicMock()
    mock_place.id = place_id
    mock_place.title = "Manoir"
    mock_place.description = "Luigi non inclus"
    mock_place.price = 100.0
    mock_place.latitude = 45.0
    mock_place.longitude = 5.0
    mock_place.amenities = []

    mock_facade.get_place.return_value = mock_place

    # Act: get place by ID
    response = client.get(f'/api/v1/places/{place_id}')

    # Assert: place details returned correctly
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == "Manoir"
    assert data['place_id'] == str(place_id)


@patch('app.api.v1.places.facade')
def test_update_place(mock_facade, client, user_token):
    # Arrange: existing place owned by user, and updated place
    token, user_id = user_token
    place_id = str(uuid.uuid4())

    mock_existing_place = MagicMock()
    mock_existing_place.id = place_id
    mock_existing_place.owner_id = user_id  # Important for ownership check
    mock_existing_place.amenities = []

    mock_updated_place = MagicMock()
    mock_updated_place.id = place_id
    mock_updated_place.title = "Grotte"
    mock_updated_place.description = "Amenez votre gourdin"
    mock_updated_place.price = 200.0
    mock_updated_place.latitude = 50.0
    mock_updated_place.longitude = 10.0
    mock_updated_place.owner_id = user_id
    mock_updated_place.amenities = []

    mock_facade.get_place.return_value = mock_existing_place
    mock_facade.update_place.return_value = mock_updated_place

    payload = {
        "title": "Grotte",
        "price": 200.0
    }

    # Act: update place via PUT
    response = client.put(
        f'/api/v1/places/{place_id}',
        json=payload,
        headers={'Authorization': f'Bearer {token}'}
    )

    # Assert: update successful, title updated
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == "Grotte"


@patch('app.api.v1.places.facade')
def test_delete_place(mock_facade, client, user_token):
    # Arrange: existing place owned by user for deletion
    token, user_id = user_token
    place_id = str(uuid.uuid4())

    mock_existing_place = MagicMock()
    mock_existing_place.id = place_id
    mock_existing_place.owner_id = user_id  # Ownership important
    mock_existing_place.amenities = []

    mock_facade.get_place.return_value = mock_existing_place

    # Act: delete place via DELETE
    response = client.delete(
        f'/api/v1/places/{place_id}',
        headers={'Authorization': f'Bearer {token}'}
    )

    # Assert: deletion successful with confirmation message
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "Place deleted successfully"
