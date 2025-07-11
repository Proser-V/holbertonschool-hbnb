"""
This module contains all the API endpoints for the reviews.
It calls the basic business logic from the facade (/app/services/facade).
It defines the CRUD methods for the reviews.
"""
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from pydantic import ValidationError
from uuid import UUID
from app.models.review import ReviewCreate, ReviewPublic, ReviewUpdate
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'comment': fields.String(required=True, description='Text of the review'),
    'rating': fields.Float(required=True,
                           description='Rating of the place (1-5)'),
    })


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.response(200, 'List of reviews retrieved successfully')
    @api.response(401, 'Unauthorized')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews_list = facade.get_all_reviews()
        if not reviews_list:
            return {"message": "No review yet"}, 200
        return [
            ReviewPublic.model_validate(review).model_dump()
            for review in reviews_list
            ], 200


@api.route('/from_booking/<booking_id>')
class CreateReview(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Permission error')
    @api.response(404, 'Place not found')
    def post(self, booking_id):
        """Register a new review"""
        current_user_id = get_jwt_identity()

        try:
            UUID(booking_id)
        except ValueError:
            return {"error": "Invalid booking UUID format"}, 400

        try:
            review_data = ReviewCreate(**request.json)
        except ValidationError as e:
            return {"error": json.loads(e.json())}, 400

        booking = facade.get_booking(booking_id)
        if booking is None:
            return {"error": "Booking not found"}, 404

        place_id = booking.place
        place = facade.place_repo.get(place_id)
        if place.owner_id == current_user_id:
            return {
                "error": "The owner of a place can't review its own place"
                }, 403

        try:
            new_review = facade.create_review(
                review_data, booking_id, place_id, current_user_id
                )
        except PermissionError as e:
            return {"error": str(e)}, 403
        except ValueError as e:
            return {"error": str(e)}, 400

        place.update_average_rating()
        facade.place_repo.update(place.id, {"rating": place.rating})
        return ReviewPublic.model_validate(new_review).model_dump(), 201


@api.route('/<review_id>')
class ReviewResource(Resource):
    @jwt_required()
    @api.response(200, 'Review details retrieved successfully')
    @api.response(400, 'Invalide UUID format')
    @api.response(401, 'Unauthorized')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            UUID(review_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        return ReviewPublic.model_validate(review).model_dump(), 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data or UUID format')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Permission error')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review's information"""
        current_user_id = get_jwt_identity()

        try:
            UUID(review_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if current_user_id != str(review.user_ide):
            return {'error': "Only the account owner can update "
                    "this review"}, 403

        try:
            update_data = (ReviewUpdate.model_validate(request.json)
                           .model_dump(exclude_unset=True))
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400
        place_id = review.place

        try:
            updated_review = facade.update_review(review_id, update_data)
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400

        place = facade.place_repo.get(place_id)
        place.update_average_rating()
        facade.place_repo.update(place.id, {"rating": place.rating})
        return ReviewPublic.model_validate(updated_review).model_dump(), 200

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(400, 'Invalide UUID format')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Permission error')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)
        try:
            UUID(review_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400

        review_to_delete = facade.get_review(review_id)
        if not review_to_delete:
            return {'error': 'Review not found'}, 404

        if (current_user_id != str(review_to_delete.user_ide)
           and current_user.is_admin is False):
            return {'error': "You must be the review's"
                    " creator or admin to delete it"}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.doc(security=[])
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(400, 'Invalid UUID format')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        try:
            UUID(place_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400
        review_list = facade.get_reviews_by_place(place_id)
        if not review_list:
            return {'message': 'No review for this place yet'}, 200

        return [
            ReviewPublic.model_validate(review).model_dump()
            for review in review_list
        ], 200
