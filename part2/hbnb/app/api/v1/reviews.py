"""
This module contains all the API endpoints for the reviews.
It calls the basic business logic from the facade (/app/services/facade).
It defines the CRUD methods for the reviews.
"""
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from pydantic import ValidationError
import uuid
from app.models.review import ReviewCreate
from app.models.booking import Booking
from app.models.place import Place
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'booking': fields.String(required=True, description='ID of the booking'),
    'comment': fields.String(required=True, description='Text of the review'),
    'rating': fields.Float(required=True,
                           description='Rating of the place (1-5)'),
    })


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'User must visit the place to post a review')
    @api.response(404, 'Place not found')
    def post(self):
        """Register a new review"""
        user_id = get_jwt_identity()

        try:
            review_data = ReviewCreate(**request.json)
        except ValidationError as e:
            return {"error": json.loads(e.json())}, 400
        try:
            booking_id = uuid.UUID(review_data.booking)
        except ValueError:
            return {"error": "Invalid booking UUID format"}, 400
        booking = facade.get_booking(booking_id)
        if booking is None:
            return {"error": "Booking not found"}, 404
        if booking.status != "DONE":
            return {"error": "Booking not completed"}, 403
        place_id = booking.place

        try:
            new_review = facade.create_review(
                review_data, booking_id, place_id, user_id
                )
        except PermissionError as e:
            return {"error": str(e)}, 403
        except ValueError as e:
            return {"error": str(e)}, 400

        return {
            'id': str(new_review.id),  # UUID -> str pour le JSON
            'comment': new_review.comment,
            'rating': new_review.rating,
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews_list = facade.get_all_reviews()
        if not reviews_list:
            return {"message": "No review yet"}, 200
        return [
            {
                'id': str(review.id),  # UUID -> str pour le JSON
                'comment': review.comment,
                'rating': review.rating,
            } for review in reviews_list
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(400, 'Invalide UUID format')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review_uuid = uuid.UUID(review_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400

        review = facade.get_review(review_uuid)
        if not review:
            return {'error': 'Review not found'}, 404

        return {
                'id': str(review.id),  # UUID -> str pour le JSON
                'comment': review.comment,
                'rating': review.rating,
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data or UUID format')
    def put(self, review_id):
        """Update a review's information"""
        try:
            review_uuid = uuid.UUID(review_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400

        review = facade.get_review(review_uuid)
        if not review:
            return {'error': 'Review not found'}, 404

        update_data = request.json

        try:
            updated_review = facade.update_review(review_uuid, update_data)
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400

        return {
            'id': str(updated_review.id),  # UUID -> str pour le JSON
            'comment': updated_review.comment,
            'rating': updated_review.rating,
        }, 200

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(400, 'Invalide UUID format')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        user_id = get_jwt_identity()
        """Delete a review"""
        try:
            review_uuid = uuid.UUID(review_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400

        review_to_delete = facade.get_review(review_uuid)
        if not review_to_delete:
            return {'error': 'Review not found'}, 404

        if user_id != str(review_to_delete.user):
            return {'error': "You must be the review's"
                    " creator to delete it"}, 403

        facade.delete_review(review_uuid)
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(400, 'Invalid UUID format')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            place_uuid = uuid.UUID(place_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400
        review_list = facade.get_reviews_by_place(place_uuid)
        if not review_list:
            return {'message': 'No review for this place yet'}, 200

        return [
            {
                'id': str(review.id),  # UUID -> str pour le JSON
                'comment': review.comment,
                'rating': review.rating,
            } for review in review_list
        ], 200
