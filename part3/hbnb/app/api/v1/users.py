"""
This module contains all the API endpoints for the users.
It calls the basic business logic from the facade (/app/services/facade).
It defines the CRUD methods for the users.
"""
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from datetime import datetime
from blacklist import blacklist
from pydantic import ValidationError, EmailStr, TypeAdapter
from uuid import UUID
from app.models.user import UserCreate, LoginRequest, UserUpdate
from app.models.user import UserPublic, RevokedToken, AdminCreate
from app.models.user import UserModeration
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from argon2.exceptions import VerifyMismatchError
from app import db
import json

api = Namespace('users', description='User operations')
api = Namespace('auth', description='Authentication operations')

# Doc only, no validation here
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of user'),
    'last_name': fields.String(required=True, description='Last name of user'),
    'email': fields.String(required=True, description='Email of user'),
    'password': fields.String(required=True, description='Password of user'),
    'photo_url': fields.String(required=False, description='Avatar of user')
})

# User update
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False,
                                description='First name of user'),
    'last_name': fields.String(required=False,
                               description='Last name of user'),
    'email': fields.String(required=False, description='Email of user'),
    'password': fields.String(required=False, description='Password of user'),
    'photo_url': fields.String(required=False, description='Avatar of user')
})

# User login
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# User moderation
user_moderation_model = api.model('UserModeration', {
    'is_active': fields.Boolean(required=True,
                                description='Desactive or active an account')
})


@api.route('/')
class UserList(Resource):
    @api.doc(security=[])
    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input')
    def post(self):
        """Register new user"""
        try:
            user_data = UserCreate(**request.json)
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400

        if facade.get_user_by_email(user_data.email):
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data.model_dump())

        return UserPublic.model_validate(new_user).model_dump(), 201

    @jwt_required()
    @api.doc(params={'email': 'Filter user by email (optional)'})
    @api.response(200, 'User(s) found')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'User not found')
    def get(self):
        """Get all users or by email query"""
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)
        if (current_user.is_admin is False):
            return {'error': "Only an admin can view these informations"}, 403
        email = request.args.get('email')
        if email:
            user = facade.get_user_by_email(email)
            if not user:
                return {'error': 'User not found'}, 404

            return UserPublic.model_validate(user).model_dump(), 200

        users = facade.get_all_users()
        return [
            UserPublic.model_validate(user).model_dump()
            for user in users
            ], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.response(200, 'user details retrieved successfully')
    @api.response(400, 'Invalid UUID format')
    @api.response(401, 'Unauthorized')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        try:
            UUID(user_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return UserPublic.model_validate(user).model_dump(), 200

    @jwt_required()
    @api.expect(user_update_model)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid input or UUID format')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update an existing user"""
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)
        try:
            UUID(user_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400

        if (current_user_id != str(user_id)
           and current_user.is_admin is False):
            return {'error': "Only an admin or the account owner can modify "
                    "this account"}, 403

        existing_user = facade.get_user(user_id)
        if not existing_user:
            return {'error': 'User not found'}, 404

        try:
            update_user = UserUpdate.model_validate(request.json)
            if update_user.photo_url is not None:
                if not UserUpdate.validate_image(update_user.photo_url):
                    return {'message': 'L\'URL ne pointe pas'
                            ' vers une image valide'}, 400
            update_data = update_user.model_dump(exclude_unset=True,
                                                 mode="json")
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400
        if "email" in update_data:
            try:
                TypeAdapter(EmailStr).validate_python(update_data["email"])
            except ValidationError:
                return {"error": "Invalid email format"}, 400

        if ("email" in update_data and
           facade.get_user_by_email(update_data["email"])):
            return {'error': 'Email already registered'}, 400

        try:
            updated_user = facade.update_user(user_id, update_data)
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400

        return UserPublic.model_validate(updated_user).model_dump(), 200

    @jwt_required()
    @api.response(200, 'User deleted successfully')
    @api.response(400, 'Invalide UUID format')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)
        """Delete a user"""
        try:
            UUID(user_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400

        user_to_delete = facade.get_user(user_id)
        if not user_to_delete:
            return {'error': 'User not found'}, 404

        if (current_user_id != str(user_id)
           and current_user.is_admin is False):
            return {'error': "Only an admin or the account owner can delete "
                    "this account"}, 403

        facade.delete_user(user_id)
        return {'message': 'User deleted successfully'}, 200


@api.route('/login')
class Login(Resource):
    @api.doc(security=[])
    @api.expect(login_model, validate=True)
    @api.response(200, 'Token created')
    @api.response(400, 'Invalid password or email')
    @api.response(403, 'Forbidden')
    @api.response(404, 'User not found')
    def post(self):
        """Login the user"""
        data = request.json
        try:
            login_data = LoginRequest(**data)
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400

        user = facade.get_user_by_email(login_data.email)
        if not user:
            return {'error': 'User not found'}, 404
        try:
            facade.passwd_hasher.verify(
                user.hashed_password, login_data.password)
        except VerifyMismatchError:
            return {'error': 'Invalid password or email'}, 400

        if user.is_active is False:
            return {'error': 'User account deactivated'}, 403

        access_token = create_access_token(
            identity=user.id,
            additional_claims={"is_admin": user.is_admin}
        )
        refresh_token = create_refresh_token(identity=user.id)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200


@api.route('/refresh')
class TokenRefresh(Resource):
    @jwt_required()
    @api.response(200, 'Refresh token created')
    @api.response(401, 'Unauthorized')
    def post(self):
        identity = get_jwt_identity()
        new_token = create_access_token(identity=identity)
        return {"access_token": new_token}, 200


@api.route('/logout')
class Logout(Resource):
    @api.response(200, 'Access token revoked')
    @api.response(401, 'Unauthorized')
    @jwt_required()
    def post(self):
        jwt_data = get_jwt()
        jti = jwt_data["jti"]
        exp = jwt_data["exp"]
        expires_at = datetime.utcfromtimestamp(exp)

        db.session.add(RevokedToken(jti=jti, expires_at=expires_at))
        db.session.commit()

        return {"message": "Access token revoked"}, 200


@api.route('/logout_refresh')
class LogoutRefresh(Resource):
    @api.response(200, 'Refresh token revoked')
    @api.response(401, 'Unauthorized')
    @jwt_required(refresh=True)
    def post(self):
        jwt_data = get_jwt()
        jti = jwt_data["jti"]
        exp = jwt_data["exp"]
        expires_at = datetime.utcfromtimestamp(exp)

        db.session.add(RevokedToken(jti=jti, expires_at=expires_at))
        db.session.commit()

        return {"message": "Refresh token revoked"}, 200


@api.route('/admin_creation')
class AdminCreation(Resource):
    @api.expect(user_model)
    @api.response(201, 'Admin successfully created')
    @api.response(400, 'Email already registered or invalid input')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @jwt_required()
    def post(self):
        """
        Create a new admin.
        """
        identity = get_jwt_identity()
        user = facade.get_user(identity)
        if not user.is_admin:
            return {'error': 'You are not allowed'}, 403
        try:
            admin_data = AdminCreate(**request.json)
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400

        if facade.get_user_by_email(admin_data.email):
            return {'error': 'Email already registered'}, 400

        new_admin = facade.create_user_admin(admin_data.model_dump())

        return UserPublic.model_validate(new_admin).model_dump(), 201


@api.route('/<user_id>/moderate')
class ModerateUser(Resource):
    @jwt_required()
    @api.expect(user_moderation_model)
    @api.response(201, 'User successfully updated')
    @api.response(400, 'Email already registered or invalid input')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    def patch(self, user_id):
        """
        Deactivate or activate an user account
        """
        identity = get_jwt_identity()
        user = facade.get_user(identity)
        try:
            UUID(user_id)
        except ValueError:
            return {'error': 'Invalid UUID format'}, 400
        if not user.is_admin:
            return {'error': 'You are not allowed'}, 403
        try:
            user_is_active = UserModeration(**request.json)
        except ValidationError as e:
            return {'error': json.loads(e.json())}, 400

        updated_user = facade.update_user(user_id, user_is_active.model_dump())
        return UserPublic.model_validate(updated_user).model_dump(), 201
