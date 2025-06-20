"""
This module contains all the API endpoints for the places.
It calls the basic business logic from the facade (/app/services/facade).
It defines the CRUD methods for the places.
"""
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from pydantic import ValidationError
from app.models.place import PlaceCreate, Place
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
    @api.response(403, 'User must be connected to create a place')
    @api.response(400, 'Invalid input')
    @api.response(401, 'Unauthorized')
    def post(self):
        """Create a new place"""
        user_id = get_jwt_identity()
        data = request.json
        data['owner_id'] = user_id
        try:
            new_place = facade.create_place(data)
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400
        except Exception as e:
            return {'error': str(e)}, 500
        amenities = []
        for amenity in new_place.amenities:
            amenities.append({
                'id': str(amenity.id),
                'name': amenity.name,
                'description': amenity.description
            })
        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner_id,
            'amenities': amenities
        }, 201

    @api.response(200, 'Places found')
    @api.response(404, 'No places found')
    def get(self):
        """Get a list of all places"""
        places = facade.place_repo.get_all()
        places_list = []
        for place in places:
            amenities = []
            for amenity in place.amenities:
                amenities.append({
                    'id': str(amenity.id),
                    'name': amenity.name,
                    'description': amenity.description
                })
            places_list.append({
                'id': str(place.id),
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'amenities': amenities
            })
        return places_list, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place(s) found')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get a place by ID"""
        if place_id:
            try:
                place_uuid = UUID(place_id)
            except ValueError:
                return {'error': 'invalid UUID format'}

            place = facade.get_place(place_uuid)
            if not place:
                return {'error': 'Place not found'}, 404

            amenities = []
            for amenity in place.amenities:
                amenities.append({
                    'id': str(amenity.id),
                    'name': amenity.name,
                    'description': amenity.description
                })

            return {
                'place_id': str(place.id),
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'amenities': amenities
            }, 200

    @jwt_required()
    @api.expect(place_model_update)
    @api.response(200, 'Place successfully updated')
    @api.response(400, 'Invalid input or UUID')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Method to update a place"""
        user_id = get_jwt_identity()
        try:
            place_uuid = UUID(place_id)
        except ValueError:
            return {'error': 'Invalid input or UUID'}, 400

        existing_place = facade.get_place(place_uuid)
        if not existing_place:
            return {'error': 'Place not found'}, 404

        if existing_place.owner_id != user_id:
            return {'error': 'You must own this place to modify it'}, 403

        update_data = request.json
        try:
            updated_place = facade.update_place(place_uuid, update_data)
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400

        amenities = []
        for amenity in updated_place.amenities:
            amenities.append({
                'id': str(amenity.id),
                'name': amenity.name,
                'description': amenity.description
            })

        return {
            'id': updated_place.id,
            'title': updated_place.title,
            'description': updated_place.description,
            'price': updated_place.price,
            'latitude': updated_place.latitude,
            'longitude': updated_place.longitude,
            'owner_id': updated_place.owner_id,
            'amenities': amenities
        }

    @jwt_required()
    @api.response(200, 'Place successfully deleted')
    @api.response(400, 'Invalid ID')
    @api.response(401, 'Invalid credentials')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Method to delete a place"""
        user_id = get_jwt_identity()
        try:
            place_uuid = UUID(place_id)
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400

        existing_place = facade.get_place(place_uuid)
        if not existing_place:
            return {'error': 'Place not found'}, 404

        if existing_place.owner_id != user_id:
            return {'error': 'You must own the place to delete it'}, 403

        facade.delete_place(place_uuid)
        return {'message': 'Place deleted successfully'}, 200
