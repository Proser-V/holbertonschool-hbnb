"""
This module contains all the API endpoints for the bookings.
It calls the basic business logic from the facade (/app/services/facade).
It defines the CRUD methods for the bookings.
"""
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from app.models.booking import CreateBooking, BookingPublic, BookingStatus
from app.models.booking import UpdateBooking
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
from datetime import datetime, timezone
import json

api = Namespace('bookings', description='Booking operations')

# Swagger model for booking
booking_model = api.model('Booking', {
    'start_date': fields.DateTime(required=True, description='Start date'),
    'end_date': fields.DateTime(required=True, description='End date')
})

booking_update_model = api.model('BookingUpdate', {
    'start_date': fields.DateTime(required=False, description='Start date'),
    'end_date': fields.DateTime(required=False, description='End date'),
    'status': fields.String(
        required=False,
        description='Booking status (editable only by owner)',
        enum=['PENDING', 'DONE', 'CANCELLED'],
        ),
})


def ensure_aware(dt):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


@api.route('/')
class BookingList(Resource):
    @jwt_required()
    @api.response(200, 'List of bookings retrieved successfully')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    def get(self):
        """Retrieve a list of all bookings"""
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)
        if (current_user.is_admin is False):
            return {'error': "Only an admin can view these informations"}, 403
        bookings = facade.get_all_bookings()
        if not bookings:
            return {"message": "No booking yet"}, 200

        booking_list = []
        for booking in bookings:
            facade.manage_bookingstatus(booking.id)
            booking_list.append(BookingPublic.model_validate(
                booking).model_dump(mode='json'))

        return booking_list, 200


@api.route('/<place_id>')
class BookingCreate(Resource):
    @jwt_required()
    @api.expect(booking_model, validate=True)
    @api.response(201, 'Booking succesfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    def post(self, place_id):
        """Create a new booking"""
        user_id = get_jwt_identity()
        data = request.json

        try:
            uuid.UUID(place_id)
            booking_data = CreateBooking(**data)
        except ValidationError as e:
            return {'errors': json.loads(e.json())}, 400
        except ValueError as e:
            return {'error': str(e)}, 400

        booking_list = facade.get_pending_booking_list_by_place(place_id)
        for booking in booking_list:
            booking_start = ensure_aware(booking.start_date)
            booking_end = ensure_aware(booking.end_date)
            new_start = ensure_aware(booking_data.start_date)
            new_end = ensure_aware(booking_data.end_date)

            if booking_start < new_end and new_start < booking_end:
                return {'error': 'Already booked'}, 400
        now = datetime.now(timezone.utc)
        if booking_data.start_date < now:
            return {'error': 'Cannot create a booking in the past'}, 400

        new_booking = facade.create_booking(user_id, place_id, booking_data)

        return (BookingPublic.model_validate(
            new_booking).model_dump(mode='json')), 201


@api.route('/<booking_id>')
class BookingResource(Resource):
    @jwt_required()
    @api.response(200, 'Booking details retrieved successfully')
    @api.response(400, 'Invalide UUID format')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Booking not found')
    def get(self, booking_id):
        """Get booking details by ID"""
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)

        try:
            uuid.UUID(booking_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400

        booking = facade.get_booking(booking_id)
        if not booking:
            return {'error': 'Booking not found'}, 404
        place = facade.get_place(booking.place)
        if not place:
            return {'error': 'Place not found'}, 404
        if (current_user_id != booking.user
            and current_user_id != place.owner_id
                and current_user.is_admin is False):
            return {'error': "Only an admin, the place owner or the visitor "
                    "can view these informations"}, 403

        facade.manage_bookingstatus(booking_id)

        return (BookingPublic.model_validate(
            booking).model_dump(mode='json')), 200

    @api.expect(booking_update_model)
    @api.response(200, 'Booking updated successfully')
    @api.response(400, 'Invalid input data or UUID format')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Entity not found')
    @jwt_required()
    def put(self, booking_id):
        """Update a booking's information"""
        try:
            uuid.UUID(booking_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400

        booking = facade.get_booking(booking_id)
        if not booking:
            return {'error': 'Booking not found'}, 404
        if booking.status != "PENDING":
            return {
                'error': 'Cannot modifiy an already done or cancelled booking'
                }, 400
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)
        try:
            update_data = (UpdateBooking.model_validate(request.json)
                           .model_dump(exclude_unset=True))
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400

        now = datetime.now(timezone.utc)
        if 'start_date' in update_data and update_data['start_date'] < now:
            return {'error': 'Cannot create a booking in the past'}, 400

        if "status" in update_data:
            place = facade.get_place(booking.place)
            if not place:
                return {'error': 'Associated place not found'}, 404
            if (str(place.owner_id) != str(current_user_id)
               and not current_user.is_admin):
                return {
                    "error": "Only the owner of a place or an"
                    "admin can update the status"
                    }, 403
            if update_data['status'] not in ("CANCELLED"):
                return {
                    'error': "Status must be CANCELLED"
                    }, 400

        try:
            updated_booking = facade.update_booking(booking_id, update_data)
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400
        except PermissionError as e:
            return {'error': str(e)}, 403

        return (BookingPublic.model_validate(
            updated_booking).model_dump(mode='json')), 200


@api.route('/places/<place_id>/booking')
class PlaceBookingList(Resource):
    @jwt_required()
    @api.response(200, 'List of booking for the place retrieved successfully')
    @api.response(400, 'Invalide UUID format')
    @api.response(401, 'Unauthorized')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all bookings for a specific place"""
        try:
            uuid.UUID(place_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404
        bookings = facade.get_booking_list_by_place(place_id)
        if not bookings:
            return {'message': 'No booking for this place yet'}, 200

        booking_list = []
        for booking in bookings:
            facade.manage_bookingstatus(booking.id)
            booking_list.append(BookingPublic.model_validate(
                booking).model_dump(mode='json'))

        return booking_list, 200


@api.route('/places/<place_id>/pending_booking')
class PlaceBookingList(Resource):
    @jwt_required()
    @api.response(200, 'List of booking for the place retrieved successfully')
    @api.response(400, 'Invalide UUID format')
    @api.response(401, 'Unauthorized')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all pending bookings for a specific place"""
        try:
            uuid.UUID(place_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404
        bookings = facade.get_pending_booking_list_by_place(place_id)
        if not bookings:
            return {'message': 'No pending booking for this place yet'}, 200

        booking_list = []
        for booking in bookings:
            facade.manage_bookingstatus(booking.id)
            booking_list.append(BookingPublic.model_validate(booking)
                                    .model_dump(mode='json'))
        return booking_list, 200


@api.route('/users/<user_id>/booking')
class UserBookingList(Resource):
    @jwt_required()
    @api.response(200, 'List of booking of the user retrieved successfully')
    @api.response(400, 'Invalide UUID format')
    @api.response(401, 'Unauthorized')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get all bookings of a user"""
        try:
            uuid.UUID(user_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400
        user = facade.get_user(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        bookings = facade.get_booking_list_by_user(user_id)
        if not bookings:
            return {'message': 'No booking for this place yet'}, 200

        booking_list = []
        for booking in bookings:
            facade.manage_bookingstatus(booking.id)
            booking_list.append(BookingPublic.model_validate(
                booking).model_dump(mode='json'))

        return booking_list, 200
