"""
This module defines Pydantic data models related to user management.
It includes models for User data, user creation requests, and login requests,
with validation rules and sensible defaults applied.
"""

import uuid
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic import field_validator
from datetime import datetime, timezone
from typing import Optional, List


# Default profile picture URL used when no photo_url is provided by the user
DEFAULT_USER_PHOTO_URL = (
    "https://cdn0.iconfinder.com/data/icons"
    "/mobile-basic-vol-1/32/Profile-256.png"
)


class User(BaseModel):
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

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(...)
    hashed_password: str
    is_active: bool = True  # Allows disabling user without deletion
    is_admin: bool = False
    created_at: datetime = Field(default_factory=lambda:
                                 datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    photo_url: Optional[str] = None
    places: List[uuid.UUID] = Field(default_factory=list)
    reviews: List[uuid.UUID] = Field(default_factory=list)

    # Pydantic config to serialize datetime as ISO format strings
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()}
    )

    @field_validator("photo_url")
    @classmethod
    def set_default_photo(cls, photo_url):
        """
        Ensures that the photo_url field defaults to a
        generic image if not provided.

        Args:
            photo_url (str | None): URL of the user's profile photo.

        Returns:
            str: The original URL or a default URL if none was given.
        """
        if not photo_url:
            return DEFAULT_USER_PHOTO_URL
        return photo_url

    def set_first_name(self, first_name: str) -> None:
        """
        Updates the user's first name and refreshes the updated_at timestamp.

        Args:
            first_name (str): New first name to set.
        """
        self.first_name = first_name
        self.updated_at = datetime.now(timezone.utc)

    def set_last_name(self, last_name: str) -> None:
        """
        Updates the user's last name and refreshes the updated_at timestamp.

        Args:
            last_name (str): New last name to set.
        """
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
    """

    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=50)

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
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty or just whitespace")
        return value


class LoginRequest(BaseModel):
    """
    Model representing a login request payload.

    Fields:
        email: User's email address (validated).
        password: User's password (raw).
    """

    email: EmailStr
    password: str
