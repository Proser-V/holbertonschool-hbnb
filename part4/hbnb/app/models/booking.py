"""
This module defines data models related to bookings using Pydantic.
It supports creation, validation, and management of Booking objects,
enforcing constraints such as valid date ranges and status values.
"""

from extensions import db  # db = SQLAlchemy()
from datetime import datetime, timezone
from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Optional
from enum import Enum


class BookingStatus(Enum):
    """
    Enumeration of possible booking statuses.
    """
    DONE = "DONE"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"


class Booking(db.Model):
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
        updated_at: Timestamp for the last update.
    """

    __tablename__ = 'bookings'

    id = db.Column(db.String, primary_key=True)
    status = db.Column(
        db.String(20),
        default=BookingStatus.PENDING.value,
        nullable=False
        )
    place = db.Column(db.String, db.ForeignKey('place.id'), nullable=False)
    user = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
        )
    updated_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
        )
    place_rel = db.relationship(
        "Place",
        back_populates='bookings',
        foreign_keys=[place]
        )
    user_rel = db.relationship("User", back_populates='bookings')
    reviews = db.relationship('Review', back_populates='booking_rel')

    __table_args__ = (
        db.CheckConstraint(
            "status IN ('DONE', 'PENDING', 'CANCELLED')",
            name="check_booking_status"
        ),
    )

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


class UpdateBooking(BaseModel):
    """
    Schema used for booking update, enforcing that start_date
    must be strictly before end_date.
    Attributes:
        start_date: Desired start datetime of the booking.
        end_date: Desired end datetime of the booking.
    """

    start_date: Optional[datetime] = Field(None)
    end_date: Optional[datetime] = Field(None)
    status: Optional[str] = None

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


class BookingPublic(BaseModel):
    """
    This class is used to display public informations when a booking is
    returned to the client.
    """
    id: str
    start_date: datetime = Field(...)
    end_date: datetime = Field(...)
    user: str
    place: str
    status: str

    model_config = ConfigDict(
                json_encoders={datetime: lambda v: v.isoformat()},
                from_attributes=True
    )
