"""
This module contains all the API endpoints for the bookings.
It calls the basic business logic from the facade (/app/services/facade).
It defines the CRUD methods for the bookings.
"""
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from app.models.booking import CreateBooking
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
from datetime import datetime, timezone
from dateutil.parser import isoparse
import json

api = Namespace('bookings', description='Booking operations')

# Swagger model for booking
booking_model = api.model('Booking', {
    'place_id': fields.String(required=True, description='ID of the place'),
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


@api.route('/')
class BookingList(Resource):
    @jwt_required()
    @api.expect(booking_model, validate=True)
    @api.response(201, 'Booking succesfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new booking"""
        user_id = get_jwt_identity()
        data = request.json

        try:
            place_id = uuid.UUID(data.get("place_id"))
            booking_data = CreateBooking(**data)
        except ValidationError as e:
            return {'errors': json.loads(e.json())}, 400
        except ValueError as e:
            return {'error': str(e)}, 400

        booking_list = facade.get_booking_list_by_place(place_id)
        for booking in booking_list:
            if (
                booking.start_date < booking_data.end_date
                and booking_data.start_date < booking.end_date
               ):
                return {"error": "Already booked"}, 400
        new_booking = facade.create_booking(user_id, place_id, booking_data)

        return new_booking.model_dump(mode="json"), 201

    @api.response(200, 'List of bookings retrieved successfully')
    def get(self):
        """Retrieve a list of all bookings"""
        bookings = facade.get_all_bookings()
        if not bookings:
            return {"message": "No booking yet"}, 200

        booking_list = []
        now = datetime.now(timezone.utc)
        for booking in bookings:
            if booking.status == "PENDING" and now > booking.end_date:
                booking.set_status("DONE")
            booking_list.append({
                'id': str(booking.id),
                'place_id': str(booking.place),
                'user_id': str(booking.user),
                'start_date': booking.start_date.isoformat(),
                'end_date': booking.end_date.isoformat(),
                'status': booking.status,
            })
        return booking_list, 200


@api.route('/<booking_id>')
class BookingResource(Resource):
    @api.response(200, 'Booking details retrieved successfully')
    @api.response(400, 'Invalide UUID format')
    @api.response(404, 'Booking not found')
    def get(self, booking_id):
        """Get booking details by ID"""
        try:
            booking_uuid = uuid.UUID(booking_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400

        booking = facade.get_booking(booking_uuid)
        if not booking:
            return {'error': 'Booking not found'}, 404

        if (
            booking.status == "PENDING"
            and datetime.now(timezone.utc) > booking.end_date
        ):
            booking.set_status("DONE")
        return {
                'id': str(booking.id),  # UUID -> str pour le JSON
                'user_id': str(booking.user),
                'place_id': str(booking.place),
                'start_date': booking.start_date.isoformat(),
                'end_date': booking.end_date.isoformat(),
                'status': booking.status,
        }, 200

    @api.expect(booking_update_model)
    @api.response(200, 'Booking updated successfully')
    @api.response(404, 'Booking not found')
    @api.response(400, 'Invalid input data or UUID format')
    @jwt_required()
    def put(self, booking_id):
        """Update a booking's information"""
        try:
            booking_uuid = uuid.UUID(booking_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400

        booking = facade.get_booking(booking_uuid)
        if not booking:
            return {'error': 'Booking not found'}, 404

        current_user = get_jwt_identity()
        update_data = request.json

        try:
            if update_data.get('start_date'):
                update_data['start_date'] = isoparse(update_data['start_date'])
            if update_data.get('end_date'):
                update_data['end_date'] = isoparse(update_data['end_date'])
        except ValueError as e:
            return {'error': 'Invalid date format'}, 400

        if "status" in update_data:
            place = facade.get_place(booking.place)
            if not place or str(place.owner_id) != str(current_user):
                return {
                    'error': 'Only the owner of a place can update the status'
                    }, 403
            if update_data['status'] not in ("DONE", "PENDING", "CANCELED"):
                return {
                    'error': "Status must be DONE, PENDING, or CANCELED"
                    }, 400

        try:
            updated_booking = facade.update_booking(booking_uuid, update_data)
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400
        except PermissionError as e:
            return {'error': str(e)}, 403

        return [
            {
                'id': str(updated_booking.id),  # UUID -> str pour le JSON
                'start_date': updated_booking.start_date.isoformat(),
                'end_date': updated_booking.end_date.isoformat(),
                'status': updated_booking.status,
            }
        ], 200


@api.route('/places/<place_id>/booking')
class PlaceBookingList(Resource):
    @api.response(200, 'List of booking for the place retrieved successfully')
    @api.response(400, 'Invalide UUID format')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all bookings for a specific place"""
        try:
            place_uuid = uuid.UUID(place_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400
        bookings = facade.get_booking_list_by_place(place_uuid)
        if not bookings:
            return {'message': 'No booking for this place yet'}, 200

        booking_list = []
        now = datetime.now(timezone.utc)
        for booking in bookings:
            if booking.status == "PENDING" and now > booking.end_date:
                booking.set_status("DONE")
            booking_list.append({
                'id': str(booking.id),
                'place_id': str(booking.place),
                'user_id': str(booking.user),
                'start_date': booking.start_date.isoformat(),
                'end_date': booking.end_date.isoformat(),
                'status': booking.status,
            })
        return booking_list, 200


@api.route('/users/<user_id>/booking')
class UserBookingList(Resource):
    @api.response(200, 'List of booking of the user retrieved successfully')
    @api.response(400, 'Invalide UUID format')
    def get(self, user_id):
        """Get all bookings of a user"""
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400
        bookings = facade.get_booking_list_by_user(user_uuid)
        if not bookings:
            return {'message': 'No booking for this place yet'}, 200

        booking_list = []
        now = datetime.now(timezone.utc)
        for booking in bookings:
            if booking.status == "PENDING" and now > booking.end_date:
                booking.set_status("DONE")
            booking_list.append({
                'id': str(booking.id),
                'place_id': str(booking.place),
                'user_id': str(booking.user),
                'start_date': booking.start_date.isoformat(),
                'end_date': booking.end_date.isoformat(),
                'status': booking.status,
            })
        return booking_list, 200
