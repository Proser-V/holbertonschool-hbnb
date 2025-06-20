import pytest
from app import create_app
from flask_jwt_extended import create_access_token
import uuid


@pytest.fixture(scope="session")
def app():
    """
    Create and configure a Flask application instance for testing.

    - Enables TESTING mode for better error handling during tests.
    - Sets a JWT secret key for token generation.
    - 'session' scope means this app instance is created once per test session.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'a-string-secret-at-least-256-bits-long'
    return app


@pytest.fixture
def client(app):
    """
    Provide a Flask test client linked to the application.

    This client allows sending simulated HTTP requests
    without running a real server.
    """
    return app.test_client()


@pytest.fixture
def user_id():
    """
    Generate a random UUID simulating a user ID.

    Useful for creating mock users in tests.
    """
    return uuid.uuid4()


@pytest.fixture
def user_token(app):
    """
    Create a JWT access token for a mock user.

    - Generates a UUID for the user identity.
    - Uses flask_jwt_extended's create_access_token.
    - The token can be used to authenticate requests in tests.
    """
    with app.app_context():
        user_id = str(uuid.uuid4())
        access_token = create_access_token(identity=user_id)
    return access_token, user_id


@pytest.fixture
def admin_token(app):
    """
    Create a JWT access token for a mock admin user.

    - Generates a UUID for the admin identity.
    - Useful for testing routes or actions restricted to admins.
    - Returns both the access token and the admin user ID.
    """
    with app.app_context():
        admin_id = str(uuid.uuid4())
        access_token = create_access_token(identity=admin_id)
    return access_token, admin_id
