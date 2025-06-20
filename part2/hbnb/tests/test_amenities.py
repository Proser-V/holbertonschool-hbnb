import uuid
import json
from unittest.mock import patch, MagicMock

"""
Unit tests for the Amenities API endpoints.

These tests use unittest.mock to patch the facade layer, simulating
the behavior of the backend without hitting a real database.

Tests cover:
- Creating amenities as admin and non-admin users
- Retrieving all amenities
- Retrieving a single amenity by ID
- Handling amenity not found cases
- Updating amenities as admin users and handling update errors

Fixtures `client`, `admin_token`, and `user_token` are assumed to be
provided by the test environment.
"""


@patch('app.api.v1.amenities.facade')
def test_create_amenity_as_admin(mock_facade, client, admin_token):
    # Arrange: setup admin user and mock facade behavior
    token, admin_id = admin_token

    mock_admin = MagicMock()
    mock_admin.is_admin = True
    mock_facade.get_user.return_value = mock_admin

    mock_facade.get_amenity.return_value = None  # No existing amenity

    mock_amenity = MagicMock()
    mock_amenity.id = uuid.uuid4()
    mock_amenity.name = "Oxygène"
    mock_amenity.description = "En supplément payant"
    mock_facade.create_amenity.return_value = mock_amenity

    payload = {
        "name": "Oxygène",
        "description": "En supplément payant"
    }

    # Act: perform the POST request to create an amenity
    response = client.post(
        '/api/v1/amenities/',
        json=payload,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    )

    # Assert: verify the response is as expected
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == "Oxygène"
    assert data['description'] == "En supplément payant"


@patch('app.api.v1.amenities.facade')
def test_create_amenity_as_non_admin(mock_facade, client, user_token):
    # Arrange: setup a regular (non-admin) user
    token, user_id = user_token

    mock_user = MagicMock()
    mock_user.is_admin = False
    mock_facade.get_user.return_value = mock_user

    payload = {
        "name": "Sans cafards",
        "description": "Aucune garantie"
    }

    # Act: attempt to create amenity as non-admin user
    response = client.post(
        '/api/v1/amenities/',
        json=payload,
        headers={'Authorization': f'Bearer {token}'}
    )

    # Assert: creation is forbidden for non-admin users
    assert response.status_code == 403
    data = response.get_json()
    assert "Admin privileges required" in data['error']


@patch('app.api.v1.amenities.facade')
def test_get_all_amenities(mock_facade, client):
    # Arrange: mock facade to return one amenity
    mock_amenity = MagicMock()
    mock_amenity.id = uuid.uuid4()
    mock_amenity.name = "Escaliers"
    mock_amenity.description = "En papier"

    mock_facade.get_all_amenities.return_value = [mock_amenity]

    # Act: send GET request to list amenities
    response = client.get('/api/v1/amenities/')

    # Assert: response contains the mocked amenity
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['name'] == "Escaliers"
    assert data[0]['description'] == "En papier"


@patch('app.api.v1.amenities.facade')
def test_get_amenity_by_id(mock_facade, client):
    # Arrange: create a mock amenity with specific ID
    amenity_id = uuid.uuid4()
    mock_amenity = MagicMock()
    mock_amenity.id = amenity_id
    mock_amenity.name = "Vers"
    mock_amenity.description = "Plus trop luisants"

    mock_facade.get_amenity.return_value = mock_amenity

    # Act: retrieve amenity by ID
    response = client.get(f'/api/v1/amenities/{amenity_id}')

    # Assert: returned data matches mock
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == str(amenity_id)
    assert data['name'] == "Vers"


@patch('app.api.v1.amenities.facade')
def test_get_amenity_not_found(mock_facade, client):
    # Arrange: simulate amenity not found
    amenity_id = uuid.uuid4()
    mock_facade.get_amenity.return_value = None

    # Act: attempt to get nonexistent amenity
    response = client.get(f'/api/v1/amenities/{amenity_id}')

    # Assert: 404 returned with error message
    assert response.status_code == 404
    data = response.get_json()
    assert "Amenity not found" in data['error']


@patch('app.api.v1.amenities.facade')
def test_update_amenity_as_admin(mock_facade, client, admin_token):
    # Arrange: admin user, existing amenity and updated data
    token, admin_id = admin_token
    amenity_id = uuid.uuid4()

    mock_admin = MagicMock()
    mock_admin.is_admin = True
    mock_facade.get_user.return_value = mock_admin

    mock_existing = MagicMock()
    mock_existing.id = amenity_id
    mock_facade.get_amenity.return_value = mock_existing

    mock_updated = MagicMock()
    mock_updated.id = amenity_id
    mock_updated.name = "Papier toilette"
    mock_updated.description = "Réutilisable"
    mock_facade.update_amenity.return_value = mock_updated

    payload = {
        "name": "Papier toilette",
        "description": "Réutilisable"
    }

    # Act: send PUT request to update the amenity
    response = client.put(
        f'/api/v1/amenities/{amenity_id}',
        json=payload,
        headers={'Authorization': f'Bearer {token}'}
    )

    # Assert: updated data is returned correctly
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == "Papier toilette"


@patch('app.api.v1.amenities.facade')
def test_update_amenity_not_found(mock_facade, client, admin_token):
    # Arrange: admin tries to update nonexistent amenity
    token, admin_id = admin_token
    amenity_id = uuid.uuid4()

    mock_admin = MagicMock()
    mock_admin.is_admin = True
    mock_facade.get_user.return_value = mock_admin

    mock_facade.get_amenity.return_value = None

    payload = {
        "name": "Gouvernement compétent",
        "description": "Pas vu depuis des années"
    }

    # Act: update attempt on nonexistent amenity
    response = client.put(
        f'/api/v1/amenities/{amenity_id}',
        json=payload,
        headers={'Authorization': f'Bearer {token}'}
    )

    # Assert: 404 returned with proper error message
    assert response.status_code == 404
    data = response.get_json()
    assert "Amenity not found" in data['error']
