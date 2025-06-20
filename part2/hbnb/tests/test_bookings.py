import uuid
from datetime import datetime, timedelta, timezone
import pytest
from unittest.mock import patch

"""
Unit tests for the Bookings API endpoints.

These tests mock the facade layer to simulate database
operations without real persistence.

The tests cover:
- Creating a booking (including conflict detection)
- Retrieving bookings by ID
- Handling booking not found cases
- Updating bookings
- Listing all bookings (including empty list case)

A `MockBooking` class mimics the Booking model with the necessary attributes
and a `model_dump` method.

Test fixtures `client` and `user_token` are assumed to be provided by
the test environment.
"""


# MockBooking simulates the Booking model for tests
class MockBooking:
    def __init__(self, user=None, place=None, status="PENDING",
                 start_date=None, end_date=None, id=None):
        self.id = id or uuid.uuid4()
        self.user = user or uuid.uuid4()
        self.place = place or uuid.uuid4()
        self.status = status
        now = datetime.now(timezone.utc)
        self.start_date = start_date or now
        self.end_date = end_date or (now + timedelta(days=1))

    def model_dump(self, mode="json"):
        # Serialize the booking instance to dict (JSON-like)
        return {
            "id": str(self.id),
            "user_id": str(self.user),
            "place_id": str(self.place),
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "status": self.status
        }

    def set_status(self, new_status):
        self.status = new_status


@patch('app.api.v1.bookings.facade')
def test_create_booking(mock_facade, client, user_token):
    # Arrange: user token and place, no existing bookings for place
    token, user_id = user_token
    place_id = uuid.uuid4()
    mock_facade.get_booking_list_by_place.return_value = []

    # Booking to be created
    mock_booking = MockBooking(user=user_id, place=place_id)
    mock_facade.create_booking.return_value = mock_booking

    payload = {
        "place_id": str(place_id),
        "start_date": mock_booking.start_date.isoformat(),
        "end_date": mock_booking.end_date.isoformat()
    }

    # Act: create booking via POST
    response = client.post(
        '/api/v1/bookings/',
        json=payload,
        headers={'Authorization': f'Bearer {token}'}
    )

    # Assert: booking created successfully with status PENDING
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == "PENDING"
    assert data['place_id'] == str(place_id)
    assert 'id' in data


@patch('app.api.v1.bookings.facade')
def test_create_booking_conflict(mock_facade, client, user_token):
    # Arrange: existing booking that conflicts with requested dates
    token, user_id = user_token
    place_id = uuid.uuid4()

    existing_booking = MockBooking(
        user=user_id,
        place=place_id,
        start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
        end_date=datetime(2025, 1, 10, tzinfo=timezone.utc)
    )
    mock_facade.get_booking_list_by_place.return_value = [existing_booking]

    payload = {
        "place_id": str(place_id),
        "start_date": "2025-01-05T00:00:00+00:00",
        "end_date": "2025-01-15T00:00:00+00:00"
    }

    # Act: try to create conflicting booking
    response = client.post(
        '/api/v1/bookings/',
        json=payload,
        headers={'Authorization': f'Bearer {token}'}
    )

    # Assert: error returned due to booking conflict
    assert response.status_code == 400
    data = response.get_json()
    assert "Already booked" in data['error']


@patch('app.api.v1.bookings.facade')
def test_get_booking_by_id(mock_facade, client):
    # Arrange: mock a booking returned by facade
    booking_id = uuid.uuid4()
    mock_booking = MockBooking(id=booking_id)
    mock_facade.get_booking.return_value = mock_booking

    # Act: get booking by ID
    response = client.get(f'/api/v1/bookings/{booking_id}')

    # Assert: booking returned successfully
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == str(booking_id)


@patch('app.api.v1.bookings.facade')
def test_get_booking_not_found(mock_facade, client):
    # Arrange: no booking found by facade
    mock_facade.get_booking.return_value = None
    booking_id = uuid.uuid4()

    # Act: attempt to get nonexistent booking
    response = client.get(f'/api/v1/bookings/{booking_id}')

    # Assert: 404 error returned
    assert response.status_code == 404
    data = response.get_json()
    assert "Booking not found" in data['error']


@patch('app.api.v1.bookings.facade')
def test_update_booking(mock_facade, client, user_token):
    # Arrange: existing booking owned by user, place owned by user
    token, user_id = user_token
    booking_id = uuid.uuid4()

    existing_booking = MockBooking(id=booking_id, user=user_id)
    mock_facade.get_booking.return_value = existing_booking

    class MockPlace:
        owner_id = user_id

    mock_facade.get_place.return_value = MockPlace()

    updated_booking = MockBooking(
        id=booking_id,
        user=user_id,
        status="DONE",
        start_date=datetime.now(timezone.utc),
        end_date=datetime.now(timezone.utc) + timedelta(days=1)
    )
    mock_facade.update_booking.return_value = updated_booking

    payload = {"status": "DONE"}

    # Act: update booking status
    response = client.put(
        f'/api/v1/bookings/{booking_id}',
        json=payload,
        headers={'Authorization': f'Bearer {token}'}
    )

    # Assert: status updated and returned as list with one item
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]['status'] == "DONE"


@patch('app.api.v1.bookings.facade')
def test_update_booking_not_found(mock_facade, client, user_token):
    # Arrange: booking not found for update
    token, user_id = user_token
    booking_id = uuid.uuid4()
    mock_facade.get_booking.return_value = None

    payload = {"status": "DONE"}

    # Act: attempt update on nonexistent booking
    response = client.put(
        f'/api/v1/bookings/{booking_id}',
        json=payload,
        headers={'Authorization': f'Bearer {token}'}
    )

    # Assert: 404 error returned
    assert response.status_code == 404
    data = response.get_json()
    assert "Booking not found" in data['error']


@patch('app.api.v1.bookings.facade')
def test_get_all_bookings(mock_facade, client):
    # Arrange: facade returns a list with one booking
    mock_booking = MockBooking()
    mock_facade.get_all_bookings.return_value = [mock_booking]

    # Act: get all bookings
    response = client.get('/api/v1/bookings/')

    # Assert: list contains the mocked booking
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(b['id'] == str(mock_booking.id) for b in data)


@patch('app.api.v1.bookings.facade')
def test_get_all_bookings_empty(mock_facade, client):
    # Arrange: facade returns an empty list
    mock_facade.get_all_bookings.return_value = []

    # Act: get all bookings
    response = client.get('/api/v1/bookings/')

    # Assert: empty message returned
    assert response.status_code == 200
    data = response.get_json()
    assert "No booking yet" in data['message']
