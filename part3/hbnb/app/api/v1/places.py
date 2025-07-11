"""
This module contains all the API endpoints for the places.
It calls the basic business logic from the facade (/app/services/facade).
It defines the CRUD methods for the places.
"""
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from pydantic import ValidationError
from app.models.place import PlacePublic, PlaceUpdate
from uuid import UUID
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

api = Namespace('places', description='Places operations')


# Model for places creation and update
place_model = api.model('Place', {
    'title': fields.String(required=True,
                           description='The title of the place'),
    'description': fields.String(required=True,
                                 description='The description of the place'),
    'price': fields.Float(required=True, description='The price of the place'),
    'latitude': fields.Float(required=True,
                             description='The latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='The longitude of the place'),
    'amenity_ids': fields.List(fields.String, required=False,
                               description='List of amenity IDs')
})

place_model_update = api.model('PlaceUpdate', {
    'title': fields.String(required=False,
                           description='The title of the place'),
    'description': fields.String(required=False,
                                 description='The description of the place'),
    'price': fields.Float(required=False,
                          description='The price of the place'),
    'latitude': fields.Float(required=False,
                             description='The latitude of the place'),
    'longitude': fields.Float(required=False,
                              description='The longitude of the place'),
    'amenity_ids': fields.List(fields.String, required=False,
                               description='List of amenity IDs')
})


@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input')
    @api.response(401, 'Unauthorized')
    @api.response(404, 'Amenity not found')
    def post(self):
        """Create a new place"""
        user_id = get_jwt_identity()
        data = request.json
        data['owner_id'] = user_id
        try:
            new_place = facade.create_place(data)
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400
        except ValueError as e:
            return {'error': str(e)}, 404
        amenities = []
        for amenity in new_place.amenities:
            amenities.append({
                'id': str(amenity.id),
                'name': amenity.name,
                'description': amenity.description
            })
        return PlacePublic.model_validate(new_place).model_dump(), 201

    @api.doc(security=[])
    @api.response(200, 'Places found')
    @api.response(404, 'No places found')
    def get(self):
        """Get a list of all places"""
        places = facade.place_repo.get_all()

        if not places:
            return {'message': 'No places found'}, 404

        return [
            PlacePublic.model_validate(place).model_dump()
            for place in places
        ], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.doc(security=[])
    @api.response(200, 'Place(s) found')
    @api.response(400, 'Invalid UUID format')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get a place by ID"""
        if place_id:
            try:
                UUID(place_id)
            except ValueError:
                return {'error': 'invalid UUID format'}, 400

            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            amenities = []
            for amenity in place.amenities:
                amenities.append({
                    'id': str(amenity.id),
                    'name': amenity.name,
                    'description': amenity.description
                })

            return PlacePublic.model_validate(place).model_dump(), 200

    @jwt_required()
    @api.expect(place_model_update)
    @api.response(200, 'Place successfully updated')
    @api.response(400, 'Invalid input or UUID')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Method to update a place"""
        user_id = get_jwt_identity()
        user = facade.get_user(user_id)
        try:
            UUID(place_id)
        except ValueError:
            return {'error': 'Invalid input or UUID'}, 400

        existing_place = facade.get_place(place_id)
        if not existing_place:
            return {'error': 'Place not found'}, 404

        if (existing_place.owner_id != user_id
           and user.is_admin is False):
            return {'error': 'You must own this place to modify it'}, 403

        try:
            update_data = (PlaceUpdate.model_validate(request.json)
                           .model_dump(exclude_unset=True))
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400
        try:
            updated_place = facade.update_place(place_id, update_data)
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400
        except ValueError as e:
            return {'error': str(e)}, 404

        amenities = []
        for amenity in updated_place.amenities:
            amenities.append({
                'id': str(amenity.id),
                'name': amenity.name,
                'description': amenity.description
            })

        return PlacePublic.model_validate(updated_place).model_dump(), 200

    @jwt_required()
    @api.response(200, 'Place successfully deleted')
    @api.response(400, 'Invalid UUID')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Method to delete a place"""
        user_id = get_jwt_identity()
        user = facade.get_user(user_id)
        try:
            UUID(place_id)
        except ValueError as e:
            return {'error': 'Invalid UUID'}, 400

        existing_place = facade.get_place(place_id)
        if not existing_place:
            return {'error': 'Place not found'}, 404

        if (existing_place.owner_id != user_id
           and user.is_admin is False):
            return {'error': 'You must own the place to delete it'}, 403

        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200
