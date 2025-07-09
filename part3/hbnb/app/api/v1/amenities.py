"""
This module contains all the API endpoints for the amenities.
It calls the basic business logic from the facade (/app/services/facade).
It defines the CRUD methods for the amenities.
"""
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from pydantic import ValidationError
from uuid import UUID
from app.models.amenity import AmenityCreate, AmenityPublic
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=True,
                                 description='Description of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Amenity already exists or invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    def post(self):
        """Register a new amenity"""
        user_id = get_jwt_identity()
        user = facade.get_user(user_id)
        if not user or not user.is_admin:
            return {"error": "Admin privileges required"}, 403

        try:
            amenity_data = AmenityCreate(**request.json)
        except ValidationError as e:
            return {"error": json.loads(e.json())}, 400

        if facade.get_amenity_by_name(amenity_data.name):
            return {"error": "This amenity already exists"}, 400

        new_amenity = facade.create_amenity(amenity_data.model_dump())
        return AmenityPublic.model_validate(new_amenity).model_dump(), 200

    @api.doc(security=[])
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Get a list of amenities"""
        amenity_list = facade.get_all_amenities()
        return [
            AmenityPublic.model_validate(amenity).model_dump()
            for amenity in amenity_list
        ], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.doc(security=[])
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            UUID(amenity_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return AmenityPublic.model_validate(amenity).model_dump(), 200

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update an amenity's information"""
        user_id = get_jwt_identity()
        user = facade.get_user(user_id)
        if not user or not user.is_admin:
            return {'error': 'Admin privileges required'}, 403
        try:
            UUID(amenity_id)
        except TypeError:
            return {'error': 'Invalid UUID format'}, 400

        existing_amenity = facade.get_amenity(amenity_id)
        if not existing_amenity:
            return {'error': 'Amenity not found'}, 404

        update_data = request.json

        try:
            updated_amenity = facade.update_amenity(amenity_id, update_data)
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400

        return AmenityPublic.model_validate(updated_amenity).model_dump(), 200

    @jwt_required()
    @api.response(200, 'Amenity deleted successfully')
    @api.response(400, 'Invalide UUID format')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete an amenity"""
        user_id = get_jwt_identity()
        user = facade.get_user(user_id)
        try:
            UUID(amenity_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400

        amenity_to_delete = facade.get_amenity(amenity_id)
        if not amenity_to_delete:
            return {'error': 'Amenity not found'}, 404

        if user.is_admin is False:
            return {'error': "You must be an admin to delete an amenity"}, 403

        facade.delete_amenity(amenity_id)
        return {'message': 'Amenity deleted successfully'}, 200
