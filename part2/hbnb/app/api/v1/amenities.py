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
from app.models.amenity import AmenityCreate
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
    @api.response(403, 'Admin privileges required')
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
        return {
            'id': str(new_amenity.id),  # UUID -> str pour le JSON
            'name': new_amenity.name,
            'description': new_amenity.description,
        }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Get a list of amenities"""
        amenity_list = facade.get_all_amenities()
        return [
            {
                'id': str(amenity.id),  # UUID -> str pour le JSON
                'name': amenity.name,
                'description': amenity.description,
            } for amenity in amenity_list
        ], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity_uuid = UUID(amenity_id)
        except TypeError:
            return {'error': 'Invalid UUID format'}, 400

        amenity = facade.get_amenity(amenity_uuid)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {
                'id': str(amenity.id),  # UUID -> str pour le JSON
                'name': amenity.name,
                'description': amenity.description,
        }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
            amenity_uuid = UUID(amenity_id)
        except TypeError:
            return {'error': 'Invalid UUID format'}, 400

        existing_amenity = facade.get_amenity(amenity_uuid)
        if not existing_amenity:
            return {'error': 'Amenity not found'}, 404

        update_data = request.json

        try:
            updated_amenity = facade.update_amenity(amenity_uuid, update_data)
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400

        return {
            'id': str(updated_amenity.id),  # UUID -> str pour le JSON
            'name': updated_amenity.name,
            'description': updated_amenity.description
        }, 200
