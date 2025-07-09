"""
This module defines Pydantic data models related to reviews.
It manages the creation, validation, and updating of Review objects,
enforcing constraints like rating boundaries and non-empty comments.
"""

from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from extensions import db  # db = SQLAlchemy()
import re


class Review(db.Model):
    """
    Represents a user review for a place, linked to a booking.

    Attributes:
        id: Unique identifier for the review (UUID as string).
        comment: Textual comment, 1 to 1000 characters.
        rating: Numeric rating between 0 and 5 inclusive.
        place: UUID of the place being reviewed.
        user: UUID of the user who wrote the review.
        booking: Identifier of the related booking.
        created_at: Timestamp when review was created (UTC).
        updated_at: Timestamp of last update (UTC).
    """
    __tablename__ = 'reviews'

    id = db.Column(db.String, primary_key=True)
    comment = db.Column(db.String(2000), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    place = db.Column(db.String, db.ForeignKey('place.id'), nullable=False)
    user_ide = db.Column(db.String, db.ForeignKey('user.id'),nullable=False)
    user_first_name = db.Column(db.String, nullable=False)
    user_last_name = db.Column(db.String, nullable=False)
    booking = db.Column(db.String,
                        db.ForeignKey('bookings.id'), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc), nullable=False
        )
    updated_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
        )
    place_rel = db.relationship(
        'Place',
        back_populates='reviews',
        foreign_keys=[place]
        )
    user = db.relationship('User', back_populates='reviews')
    booking_rel = db.relationship('Booking', back_populates='reviews')

    __table_args__ = (
        db.CheckConstraint('rating >= 0 AND rating <= 5',
                           name='check_rating_range'),
    )

    def set_comment(self, comment: str) -> None:
        """
        Update the comment and refresh the updated_at timestamp.
        Args:
            comment (str): New comment text.
        """
        self.comment = comment
        self.updated_at = datetime.now(timezone.utc)

    def set_rating(self, rating: float) -> None:
        """
        Update the rating and refresh the updated_at timestamp.
        Args:
            rating (float): New rating value between 0 and 5.
        """
        self.rating = rating
        self.updated_at = datetime.now(timezone.utc)


class ReviewCreate(BaseModel):
    """
    Schema for creating a new review.
    Attributes:
        comment: Text comment, required, trimmed and non-empty.
        rating: Rating value, required, between 0 and 5.
        booking: Booking identifier related to the review.
    """

    comment: str = Field(..., min_length=1, max_length=1000)
    rating: float = Field(..., ge=0, le=5)

    @field_validator('comment')
    @classmethod
    def check_for_blanks(cls, value: str) -> str:
        """
        Ensure the comment is not empty or whitespace only.
        Args:
            value (str): Comment string to validate.
        Raises:
            ValueError: If comment is blank or only whitespace.
        Returns:
            str: Trimmed comment string.
        """
        value = re.sub(r'\s+', ' ', value).strip()
        if not value:
            raise ValueError("Comment cannot be empty or just whitespace")
        return value.strip()

    @field_validator('rating')
    def round_one_decimal(cls, value: float) -> float:
        """
        Round the rating value to one decimal place for consistency.
        Args:
            value (float): Original rating value.
        Returns:
            float: Rounded rating value.
        """
        return round(value, 1)


class ReviewUpdate(BaseModel):
    """
    Schema for updating a new review.
    Attributes:
        comment: Text comment, required, trimmed and non-empty.
        rating: Rating value, required, between 0 and 5.
        booking: Booking identifier related to the review.
    """

    comment: Optional[str] = Field(None, min_length=1, max_length=1000)
    rating: Optional[float] = Field(None, ge=0, le=5)

    @field_validator('comment')
    @classmethod
    def check_for_blanks(cls, value: str) -> str:
        """
        Ensure the comment is not empty or whitespace only.
        Args:
            value (str): Comment string to validate.
        Raises:
            ValueError: If comment is blank or only whitespace.
        Returns:
            str: Trimmed comment string.
        """
        value = re.sub(r'\s+', ' ', value).strip()
        if not value:
            raise ValueError("Comment cannot be empty or just whitespace")
        return value.strip()

    @field_validator('rating')
    def round_one_decimal(cls, value: float) -> float:
        """
        Round the rating value to one decimal place for consistency.
        Args:
            value (float): Original rating value.
        Returns:
            float: Rounded rating value.
        """
        return round(value, 1)

class ReviewPublic(BaseModel):
    """
    This class is used to display public informations when a review is
    returned to the client.
    """
    id: str
    comment: str = Field(..., min_length=1, max_length=1000)
    rating: float = Field(..., ge=0, le=5)
    booking: str
    user_first_name: str
    user_last_name: str

    # Pydantic config to serialize datetime as ISO format strings
    model_config = ConfigDict(
                json_encoders={datetime: lambda v: v.isoformat()},
                from_attributes=True
    )
