"""
This module defines Pydantic data models related to user management.
It includes models for User data, user creation requests, and login requests,
with validation rules and sensible defaults applied.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic import field_validator, AnyUrl
from datetime import datetime, timezone
from app.models.place import Place
from app.models.review import Review
from app.models.booking import Booking
from typing import Optional
from extensions import db  # db = SQLAlchemy()
import re
import requests


# Default profile picture URL used when no photo_url is provided by the user
DEFAULT_USER_PHOTO_URL = (
    "https://cdn0.iconfinder.com/data/icons"
    "/mobile-basic-vol-1/32/Profile-256.png"
)


class User(db.Model):
    """
    Represents a user with detailed information stored in the system.

    Fields:
        id: Unique identifier as a string UUID, auto-generated.
        first_name: User's first name, required, 1-50 chars.
        last_name: User's last name, required, 1-50 chars.
        email: User's email address, validated as proper email format.
        hashed_password: Password hash stored securely.
        is_active: Flag to enable/disable account without deleting it.
        is_admin: Flag to indicate admin privileges.
        created_at: Timestamp of user creation, UTC timezone.
        updated_at: Optional timestamp for last update, UTC timezone.
        photo_url: URL of the user's profile picture,
        defaults to a generic image.
        places: List of UUIDs referencing places associated with user.
        reviews: List of UUIDs referencing reviews made by user.
    """
    __tablename__ = 'user'

    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)  # Allows disabling user
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc), nullable=False
        )
    updated_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
        )
    photo_url = db.Column(db.String(2048), nullable=True)
    places = db.relationship(Place, back_populates='owner',
                             cascade='all, delete-orphan')
    reviews = db.relationship(Review, back_populates='user',
                              cascade='all, delete-orphan')
    bookings = db.relationship(Booking, back_populates='user_rel',
                               cascade='all, delete-orphan')

    def set_first_name(self, first_name):
        self.first_name = first_name
        self.updated_at = datetime.now(timezone.utc)

    def set_last_name(self, last_name):
        self.last_name = last_name
        self.updated_at = datetime.now(timezone.utc)


class UserCreate(BaseModel):
    """
    Model used when creating a new user account.

    Fields:
        first_name: First name, required, 1-50 chars, cannot be blank.
        last_name: Last name, required, 1-50 chars, cannot be blank.
        email: Valid email address.
        password: Raw password, required, 1-50 chars, cannot be blank.
        photo_url: Url for an avatar.
    """

    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=50)
    photo_url: Optional[AnyUrl] = None

    @field_validator("photo_url")
    @classmethod
    def validate_image(cls, url):
        if url is None:
            return None
        try:
            # HEAD request
            response = requests.head(str(url), timeout=5, allow_redirects=True)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if content_type.startswith('image/'):
                    return url
            # GET partial content
            headers = {'Range': 'bytes=0-1023'}
            response = requests.get(str(url), headers=headers, timeout=5,
                                    stream=True, allow_redirects=True)
            if response.status_code in (200, 206):
                content_type = response.headers.get('Content-Type', '')
                if content_type.startswith('image/'):
                    return url
            raise ValueError("The URL is not a valid image")
        except requests.RequestException as e:
            raise ValueError(f"An error occured while the verification"
                             " of the image")

    @classmethod
    def set_default_photo(cls, photo_url):
        if not photo_url:
            return DEFAULT_USER_PHOTO_URL
        return photo_url

    @field_validator('first_name', 'last_name', 'password')
    @classmethod
    def no_blank_strings(cls, value: str) -> str:
        """
        Validates that the given field is not empty or only whitespace.
        Args:
            value (str): The input string value.
        Raises:
            ValueError: If the string is empty or only whitespace.
        Returns:
            str: The trimmed string value.
        """
        value = re.sub(r'\s+', ' ', value).strip()
        if not value:
            raise ValueError("Field cannot be empty or just whitespace")
        return value


class UserUpdate(BaseModel):
    """
    Model used when updating a new user account.

    Fields:
        first_name: First name, required, 1-50 chars, cannot be blank.
        last_name: Last name, required, 1-50 chars, cannot be blank.
        email: Valid email address.
        password: Raw password, required, 1-50 chars, cannot be blank.
        photo_url: Url for an avatar.
    """

    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=1, max_length=50)
    photo_url: Optional[AnyUrl] = None

    @field_validator("photo_url")
    @classmethod
    def validate_image(cls, url):
        if url is None:
            return None
        try:
            # HEAD request
            response = requests.head(str(url), timeout=5, allow_redirects=True)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if content_type.startswith('image/'):
                    return url
            # GET partial content
            headers = {'Range': 'bytes=0-1023'}
            response = requests.get(str(url), headers=headers, timeout=5,
                                    stream=True, allow_redirects=True)
            if response.status_code in (200, 206):
                content_type = response.headers.get('Content-Type', '')
                if content_type.startswith('image/'):
                    return url
            raise ValueError("The URL is not a valid image")
        except requests.RequestException as e:
            raise ValueError(f"An error occured while the verification"
                             " of the image")

    @classmethod
    def set_default_photo(cls, photo_url):
        if not photo_url:
            return DEFAULT_USER_PHOTO_URL
        return photo_url

    @field_validator('first_name', 'last_name', 'password')
    @classmethod
    def no_blank_strings(cls, value: str) -> str:
        """
        Validates that the given field is not empty or only whitespace.
        Args:
            value (str): The input string value.
        Raises:
            ValueError: If the string is empty or only whitespace.
        Returns:
            str: The trimmed string value.
        """
        value = re.sub(r'\s+', ' ', value).strip()
        if not value:
            raise ValueError("Field cannot be empty or just whitespace")
        return value


class UserPublic(BaseModel):
    """
    This class is used to display public informations when a user is
    returned to the client.
    """
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool

    # Pydantic config to serialize datetime as ISO format strings
    model_config = ConfigDict(
                json_encoders={datetime: lambda v: v.isoformat()},
                from_attributes=True
    )


class LoginRequest(BaseModel):
    """
    Model representing a login request payload.

    Fields:
        email: User's email address (validated).
        password: User's password (raw).
    """

    email: EmailStr
    password: str


class AdminCreate(UserCreate):
    """

    """
    is_admin: bool = True


class UserModeration(BaseModel):
    """

    """
    is_active: bool = Field(..., description="User active status (True/False)")


class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'

    jti = db.Column(db.String(36), primary_key=True)
    expires_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<RevokedToken {self.jti}>"
