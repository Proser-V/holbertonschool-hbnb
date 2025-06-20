"""
This module defines data models related to places using Pydantic.
It supports creation, validation, and management of Place objects,
including associated amenities, reviews, and photo handling.
"""

import uuid
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, timezone
from app.models.amenity import Amenity
from app.models.review import Review

# Default image URL to use when no photos are provided for a place
DEFAULT_PLACE_PHOTO_URL = (
    "https://static.vecteezy.com/system/resources/previews/006/059/989/"
    "large_2x/crossed-camera-icon-avoid-taking-photos-image-is-not-"
    "available-illustration-free-vector.jpg"
)


class Place(BaseModel):
    """
    Represents a physical place listing with detailed information.

    Attributes:
        id: Unique identifier for the place (UUID as string).
        title: Short descriptive title (1 to 50 characters).
        description: Detailed text description (1 to 1000 characters).
        price: Price per unit (e.g., per night), must be non-negative.
        latitude: Geographic latitude, valid range [-90, 90].
        longitude: Geographic longitude, valid range [-180, 180].
        owner_id: Identifier of the user who owns the place.
        amenities: List of Amenity objects associated with the place.
        created_at: Timestamp when the place was created (UTC).
        updated_at: Optional timestamp for last modification (UTC).
        photos: List of photo URLs representing the place.
        reviews: List of Review objects linked to this place.
        rating: Average rating calculated from reviews, default 0.0.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1, max_length=1000)
    price: float = Field(..., ge=0)  # price must be zero or positive
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    owner_id: str
    amenities: List[Amenity] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda:
                                 datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    photos: List[str] = Field(default_factory=list)
    reviews: List[Review] = Field(default_factory=list)
    rating: float = 0.0

    @field_validator("photos")
    @classmethod
    def set_default_photo(cls, photos_list):
        """
        Ensure that if no photos are provided, a default
        placeholder image is used.

        Args:
            photos_list (list): List of photo URLs.

        Returns:
            list: Original list if not empty, otherwise a
            list with default photo URL.
        """
        if not photos_list:
            return [DEFAULT_PLACE_PHOTO_URL]
        return photos_list

    def set_title(self, title: str):
        """
        Update the title and timestamp last update.

        Args:
            title (str): New title string.
        """
        self.title = title
        self.updated_at = datetime.now(timezone.utc)

    def set_description(self, description: str):
        """
        Update the description and timestamp last update.

        Args:
            description (str): New description string.
        """
        self.description = description
        self.updated_at = datetime.now(timezone.utc)

    def set_price(self, price: float):
        """
        Update the price and timestamp last update.

        Args:
            price (float): New price value (non-negative).
        """
        self.price = price
        self.updated_at = datetime.now(timezone.utc)

    def set_latitude(self, latitude: float):
        """
        Update the latitude and timestamp last update.

        Args:
            latitude (float): New latitude, must be between -90 and 90.
        """
        self.latitude = latitude
        self.updated_at = datetime.now(timezone.utc)

    def set_longitude(self, longitude: float):
        """
        Update the longitude and timestamp last update.

        Args:
            longitude (float): New longitude, must be between -180 and 180.
        """
        self.longitude = longitude
        self.updated_at = datetime.now(timezone.utc)

    def add_photo(self, url: str):
        """
        Add a new photo URL to the photos list.
        Removes the default photo if present before adding.

        Args:
            url (str): URL of the photo to add.
        """
        if DEFAULT_PLACE_PHOTO_URL in self.photos:
            self.photos.remove(DEFAULT_PLACE_PHOTO_URL)
        self.photos.append(url)
        self.updated_at = datetime.now(timezone.utc)

    def remove_photos(self, url: str):
        """
        Remove a photo URL from the photos list.
        If the list becomes empty after removal, add the default photo.

        Args:
            url (str): URL of the photo to remove.
        """
        self.photos.remove(url)
        if not self.photos:
            self.photos.append(DEFAULT_PLACE_PHOTO_URL)
        self.updated_at = datetime.now(timezone.utc)

    def update_average_rating(self):
        """
        Calculate and update the average rating based on the current reviews.
        If no reviews exist, the rating is set to 0.
        """
        if not self.reviews:
            self.rating = 0.0
        else:
            total = sum(review.rating for review in self.reviews)
            self.rating = round(total / len(self.reviews), 1)


class PlaceCreate(BaseModel):
    """
    Schema for creating a new Place object.

    Attributes:
        title: Title of the place (required, 1 to 100 characters).
        description: Description of the place (required, 1 to 1000 characters).
        price: Price for the place (required, must be non-negative).
        latitude: Latitude coordinate (required, between -90 and 90).
        longitude: Longitude coordinate (required, between -180 and 180).
        rating: Initial rating, defaults to 0.0.
        owner_id: Owner's user ID.
        amenity_ids: Optional list of UUIDs referencing amenities.
    """

    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=1000)
    price: float = Field(..., ge=0)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    rating: float = 0.0
    owner_id: str
    amenity_ids: Optional[List[uuid.UUID]] = []

    @field_validator('price')
    def round_price(cls, v: float) -> float:
        """
        Round the price to 2 decimal places for consistency.

        Args:
            v (float): Original price value.

        Returns:
            float: Rounded price value.
        """
        return round(v, 2)

    @field_validator('title', 'description')
    def no_blank_strings(cls, value: str) -> str:
        """
        Ensure that title and description fields are
        not blank or whitespace-only.

        Args:
            value (str): Field value to validate.

        Raises:
            ValueError: If the value is empty or only whitespace.

        Returns:
            str: Trimmed string value.
        """
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty or just whitespace")
        return value
