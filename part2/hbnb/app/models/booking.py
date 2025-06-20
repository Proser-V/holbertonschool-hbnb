"""
This module defines data models related to bookings using Pydantic.
It supports creation, validation, and management of Booking objects,
enforcing constraints such as valid date ranges and status values.
"""

import uuid
from datetime import datetime, timezone
from pydantic import BaseModel, Field, model_validator
from typing import Optional
from enum import Enum


class BookingStatus(str, Enum):
    """
    Enumeration of possible booking statuses.
    """
    DONE = "DONE"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"


class Booking(BaseModel):
    """
    Represents a booking record linking a user to a place over a date range.

    Attributes:
        id: Unique identifier for the booking (UUID).
        status: Current status of the booking, restricted to
        BookingStatus enum.
        place: UUID of the booked place.
        user: UUID of the user who made the booking.
        start_date: Start datetime of the booking.
        end_date: End datetime of the booking.
        created_at: Timestamp when the booking was created.
        updated_at: Timestamp for the last update, optional.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    status: BookingStatus = Field(default=BookingStatus.PENDING, strict=True)
    place: uuid.UUID
    user: uuid.UUID
    start_date: datetime = Field(...)
    end_date: datetime = Field(...)
    created_at: datetime = Field(default_factory=lambda:
                                 datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    def set_status(self, status: BookingStatus):
        """
        Update the booking status and the updated_at timestamp.

        Args:
            status (BookingStatus): New status value.
        """
        self.status = status
        self.updated_at = datetime.now(timezone.utc)

    def set_start_date(self, start_date: datetime):
        """
        Update the start date and timestamp the update.

        Args:
            start_date (datetime): New start date.
        """
        self.start_date = start_date
        self.updated_at = datetime.now(timezone.utc)

    def set_end_date(self, end_date: datetime):
        """
        Update the end date and timestamp the update.

        Args:
            end_date (datetime): New end date.
        """
        self.end_date = end_date
        self.updated_at = datetime.now(timezone.utc)


class CreateBooking(BaseModel):
    """
    Schema used for booking creation, enforcing that start_date
    must be strictly before end_date.

    Attributes:
        start_date: Desired start datetime of the booking.
        end_date: Desired end datetime of the booking.
    """

    start_date: datetime = Field(...)
    end_date: datetime = Field(...)

    @model_validator(mode='before')
    def check_dates(cls, values):
        """
        Validator to ensure start_date is before end_date.

        Args:
            values (dict): Input values dictionary.

        Raises:
            ValueError: If start_date is not before end_date.

        Returns:
            dict: Validated values.
        """
        start = values.get("start_date")
        end = values.get("end_date")
        if start and end and start >= end:
            raise ValueError("Start date must be before end date")
        return values
