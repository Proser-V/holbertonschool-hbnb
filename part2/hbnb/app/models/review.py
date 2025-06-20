"""
This module defines Pydantic data models related to reviews.
It manages the creation, validation, and updating of Review objects,
enforcing constraints like rating boundaries and non-empty comments.
"""

import uuid
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class Review(BaseModel):
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
        updated_at: Optional timestamp of last update (UTC).
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    comment: str = Field(..., min_length=1, max_length=1000)
    rating: float = Field(..., ge=0, le=5)  # Rating must be between 0 and 5
    place: uuid.UUID
    user: uuid.UUID
    booking: str
    created_at: datetime = Field(default_factory=lambda:
                                 datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

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
    booking: str

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
        if value is None or not value.strip():
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
