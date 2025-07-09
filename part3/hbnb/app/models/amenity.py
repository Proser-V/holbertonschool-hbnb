"""
This module defines data models for amenities using Pydantic.
It handles creation, validation, and management of Amenity objects,
enforcing constraints on fields like name and description.
"""

from pydantic import BaseModel, Field, model_validator, ConfigDict
from datetime import datetime, timezone
from app.models.place import place_amenities
from extensions import db  # db = SQLAlchemy()


class Amenity(db.Model):
    """
    Represents an amenity with unique ID, name, description, and timestamps.

    Attributes:
        id: Unique identifier for the amenity (UUID as a string).
        name: Name of the amenity, must be between 1 and 100 characters.
        description: Description of the amenity, between 1 and 500 characters.
        created_at: Timestamp of creation in UTC.
        updated_at: Optional timestamp for last update in UTC.
    """
    __tablename__ = 'amenity'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
        )
    places = db.relationship('Place', secondary=place_amenities,
                             back_populates='amenities')

    def set_name(self, name: str):
        """
        Update the amenity's name and refresh the updated_at timestamp.
        Args:
            name (str): New name for the amenity.
        """
        self.name = name
        self.updated_at = datetime.now(timezone.utc)

    def set_description(self, description: str):
        """
        Update the amenity's description and refresh the updated_at timestamp.
        Args:
            description (str): New description for the amenity.
        """
        self.description = description
        self.updated_at = datetime.now(timezone.utc)


class AmenityCreate(BaseModel):
    """
    Schema for creating an amenity with validation that
    'name' and 'description' are non-empty and non-whitespace strings.
    Attributes:
        name: Name of the amenity.
        description: Description of the amenity.
    """

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)

    @model_validator(mode='before')
    @classmethod
    def check_for_blanks(cls, values):
        """
        Validate that 'name' and 'description'
        fields are not empty or whitespace only.
        Args:
            values (dict): The input values to validate.
        Raises:
            ValueError: If either field is empty or whitespace only.
        Returns:
            dict: The validated and stripped values.
        """
        for field_name in ['name', 'description']:
            value = values.get(field_name)
            if value is None or not value.strip():
                raise ValueError(
                    f"{field_name} cannot be empty or just whitespace")
            values[field_name] = value.strip()
        return values


class AmenityPublic(BaseModel):
    """
    This class is used to display public informations when an amenity is
    returned to the client.
    """
    id: str
    name: str
    description: str

    model_config = ConfigDict(
                json_encoders={datetime: lambda v: v.isoformat()},
                from_attributes=True
    )
