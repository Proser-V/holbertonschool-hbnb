import uuid
from unittest.mock import patch, MagicMock

"""
Unit tests for the Reviews API endpoints.

These tests mock the facade layer to simulate data operations
without hitting the database.

Test cases cover:
- Creating a review (valid, booking not done, invalid UUID)
- Retrieving all reviews
- Getting a review by ID (valid and invalid UUID)
- Updating a review (valid and invalid UUID)
- Deleting a review (valid and invalid UUID)
- Getting reviews by place (valid and invalid UUID)

Fixtures `client` and `user_token` are assumed to be
provided by the test framework.
"""


@patch('app.api.v1.reviews.facade')
def test_create_review(mock_facade, client, user_token):
    token, user_id = user_token

    # Mock booking with DONE status
    booking_id = uuid.uuid4()
    mock_booking = MagicMock()
    mock_booking.id = booking_id
    mock_booking.status = "DONE"
    mock_booking.place = uuid.uuid4()

    # Mock created review
    mock_review = MagicMock()
    mock_review.id = uuid.uuid4()
    mock_review.comment = "C'était vraiment naze, lol"
    mock_review.rating = 0.2

    mock_facade.get_booking.return_value = mock_booking
    mock_facade.create_review.return_value = mock_review

    payload = {
        "booking": str(booking_id),
        "comment": "C'était vraiment naze, lol",
        "rating": 0.2
    }

    response = client.post(
        '/api/v1/reviews/',
        json=payload,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data['comment'] == "C'était vraiment naze, lol"
    assert data['rating'] == 0.2


@patch('app.api.v1.reviews.facade')
def test_create_review_booking_not_done(mock_facade, client, user_token):
    token, user_id = user_token

    # Booking with status not DONE
    booking_id = uuid.uuid4()
    mock_booking = MagicMock()
    mock_booking.id = booking_id
    mock_booking.status = "PENDING"
    mock_booking.place = uuid.uuid4()

    mock_facade.get_booking.return_value = mock_booking

    payload = {
        "booking": str(booking_id),
        "comment": "Le rat de la cuisine m'a bien tenu compagnie",
        "rating": 4.5
    }

    response = client.post(
        '/api/v1/reviews/',
        json=payload,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 403
    assert "Booking not completed" in response.get_json()['error']


@patch('app.api.v1.reviews.facade')
def test_create_review_invalid_booking_uuid(mock_facade, client, user_token):
    token, user_id = user_token

    payload = {
        "booking": "invalid-uuid",
        "comment": "Là j'avoue, j'ai plus d'idées. Tant pis.",
        "rating": 3.2
    }

    response = client.post(
        '/api/v1/reviews/',
        json=payload,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 400
    assert "Invalid booking UUID format" in response.get_json()['error']


@patch('app.api.v1.reviews.facade')
def test_get_reviews(mock_facade, client):
    mock_review = MagicMock()
    mock_review.id = uuid.uuid4()
    mock_review.comment = "C'était presque pas chiant comme la mort!"
    mock_review.rating = 4.9

    mock_facade.get_all_reviews.return_value = [mock_review]

    response = client.get('/api/v1/reviews/')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['comment'] == "C'était presque pas chiant comme la mort!"


@patch('app.api.v1.reviews.facade')
def test_get_review_by_id(mock_facade, client):
    review_id = uuid.uuid4()
    mock_review = MagicMock()
    mock_review.id = review_id
    mock_review.comment = "Au secours il y a un gobelin dans les toilettes"
    mock_review.rating = 2.1

    mock_facade.get_review.return_value = mock_review

    response = client.get(f'/api/v1/reviews/{review_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['comment'] == "Au secours il y a un gobelin dans les toilettes"
    assert data['rating'] == 2.1


@patch('app.api.v1.reviews.facade')
def test_get_review_by_id_invalid_uuid(mock_facade, client):
    response = client.get('/api/v1/reviews/invalid-uuid')
    assert response.status_code == 400
    assert "Invalid UUID format" in response.get_json()['error']


@patch('app.api.v1.reviews.facade')
def test_update_review(mock_facade, client):
    review_id = uuid.uuid4()

    mock_existing_review = MagicMock()
    mock_existing_review.id = review_id
    mock_existing_review.comment = "Ouais pas mal"
    mock_existing_review.rating = 4.0

    mock_updated_review = MagicMock()
    mock_updated_review.id = review_id
    mock_updated_review.comment = "En fait c'était cool"
    mock_updated_review.rating = 5.0

    mock_facade.get_review.return_value = mock_existing_review
    mock_facade.update_review.return_value = mock_updated_review

    payload = {
        "booking": str(uuid.uuid4()),  # still required in input model
        "comment": "En fait c'était cool",
        "rating": 5.0
    }

    response = client.put(
        f'/api/v1/reviews/{review_id}',
        json=payload
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data['comment'] == "En fait c'était cool"
    assert data['rating'] == 5.0


@patch('app.api.v1.reviews.facade')
def test_update_review_invalid_uuid(mock_facade, client):
    response = client.put('/api/v1/reviews/invalid-uuid', json={})
    assert response.status_code == 400
    assert "Invalid UUID format" in response.get_json()['error']


@patch('app.api.v1.reviews.facade')
def test_delete_review(mock_facade, client, user_token):
    access_token, user_id = user_token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    review_id = uuid.uuid4()
    mock_review = MagicMock()
    mock_review.id = review_id
    mock_review.user = user_id

    mock_facade.get_review.return_value = mock_review

    response = client.delete(f'/api/v1/reviews/{review_id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "Review deleted successfully"


@patch('app.api.v1.reviews.facade')
def test_delete_review_invalid_uuid(mock_facade, client, user_token):
    access_token, user_id = user_token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = client.delete('/api/v1/reviews/invalid-uuid', headers=headers)
    assert response.status_code == 400
    assert "Invalid UUID format" in response.get_json()['error']


@patch('app.api.v1.reviews.facade')
def test_get_reviews_by_place(mock_facade, client):
    place_id = uuid.uuid4()

    mock_review = MagicMock()
    mock_review.id = uuid.uuid4()
    mock_review.comment = "C'était vraiment un hôtel ça???"
    mock_review.rating = 0.9

    mock_facade.get_reviews_by_place.return_value = [mock_review]

    response = client.get(f'/api/v1/reviews/places/{place_id}/reviews')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['comment'] == "C'était vraiment un hôtel ça???"


@patch('app.api.v1.reviews.facade')
def test_get_reviews_by_place_invalid_uuid(mock_facade, client):
    response = client.get('/api/v1/reviews/places/invalid-uuid/reviews')
    assert response.status_code == 400
    assert "Invalid UUID format" in response.get_json()['error']
