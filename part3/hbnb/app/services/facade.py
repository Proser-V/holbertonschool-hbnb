"""
HBnBFacade Module

This module defines the HBnBFacade class, which acts as a facade layer
for the application. It centralizes operations on users, places, amenities,
reviews, and bookings, using repositories to handle data persistence.
"""

from app.persistence.repository import SQLAlchemyRepository
from app.models.amenity import Amenity, AmenityCreate
from app.models.place import Place, PlaceCreate
from app.models.review import Review
from app.models.user import User, UserCreate, AdminCreate
from app.models.booking import Booking, BookingStatus
from uuid import UUID, uuid4
from datetime import datetime, timezone
from argon2 import PasswordHasher
import uuid
from app import db


def ensure_aware(dt):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


class HBnBFacade:
    """
    HBnBFacade centralizes all business logic for managing:
    - Users
    - Places
    - Amenities
    - Reviews
    - Bookings

    It uses in-memory repositories to store data and provides
    methods for creating, retrieving, updating, and deleting records.
    """
    def __init__(self):
        """Initialize repositories for each entity."""
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.booking_repo = SQLAlchemyRepository(Booking)
        self.ph = PasswordHasher(
            time_cost=2,  # Base recommended (number of hash iterations)
            memory_cost=62500,  # Memory allowed (64Mb)
            parallelism=2,  # Number of threads used
            hash_len=24,
            salt_len=16
        )

    @property
    def passwd_hasher(self):
        return self.ph

    # ------------------ User management ------------------

    def create_user(self, user_data):
        """
        Create a new user with hashed password.
        """
        user_in = UserCreate(**user_data)
        hashed_pw = self.ph.hash(user_in.password)

        user = User(
            id=str(uuid.uuid4()),
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            email=user_in.email,
            hashed_password=hashed_pw,
            photo_url=str(user_in.photo_url)
        )
        self.user_repo.add(user)
        return user

    def create_user_admin(self, user_data):
        """
        Create a new user with hashed password.
        """
        user_in = AdminCreate(**user_data)
        hashed_pw = self.ph.hash(user_in.password)

        user = User(
            id=str(uuid.uuid4()),
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            email=user_in.email,
            hashed_password=hashed_pw,
            is_admin=user_in.is_admin,
            photo_url=str(user_in.photo_url)
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve user by email address."""
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id: UUID, update_data: dict):
        """
        Update user data. If password is provided, hash it.
        """
        user = self.user_repo.get(user_id)
        if not user:
            return None

        if "password" in update_data:
            update_data["hashed_password"] = self.ph.hash(
                update_data.pop("password")
            )

        self.user_repo.update(str(user_id), update_data)
        return self.user_repo.get(str(user_id))

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def delete_user(self, user_id):
        """Delete an user by ID."""
        user = self.user_repo.get(user_id)
        if not user:
            print(f"User not found for id={user_id}")
            return None

        self.user_repo.delete(user_id)
        return ''

    # ------------------ Place management ------------------

    def create_place(self, place_data):
        """
        Create a new place and validate amenities existence.
        """
        place_in = PlaceCreate(**place_data)

        amenities = []
        for amenity_id in place_in.amenity_ids or []:
            amenity = self.get_amenity(str(amenity_id))
            if not amenity:
                raise ValueError(f'Amenity {amenity_id} not found')
            amenities.append(amenity)

        photos = []
        for url in place_in.photos_url or []:
            photos.append(url)

        place = Place(
            id=str(uuid4()),
            title=place_in.title,
            description=place_in.description,
            price=place_in.price,
            latitude=place_in.latitude,
            longitude=place_in.longitude,
            owner_id=place_in.owner_id,
            amenities=amenities,
            photos_url=photos
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve place by ID."""
        return self.place_repo.get(place_id)

    def update_place(self, place_id: str, update_data: dict) -> Place:
        """
        Update place data, handle amenity association update.
        """
        place = self.place_repo.get(place_id)
        if not place:
            raise Exception("Place not found")

        if "amenity_ids" in update_data:
            current_amenity_ids = {str(a.id) for a in place.amenities}
            new_amenity_ids = set(update_data["amenity_ids"])

            # Determine amenities to add and remove
            to_add = new_amenity_ids - current_amenity_ids
            to_remove = current_amenity_ids - new_amenity_ids

            updated_amenities = [a for a in place.amenities if
                                 str(a.id) not in to_remove]

            for amenity_id in to_add:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity {amenity_id} not found")
                updated_amenities.append(amenity)

            place.amenities = updated_amenities

            update_data.pop('amenity_ids')
        
        if "photos_url" in update_data:
            current_photos = {str(url) for url in place.photos_url}
            new_photos = set(update_data["photos_url"])

            photos_to_add = new_photos - current_photos
            photos_to_remove = current_photos - new_photos

            updated_photos = [url for url in place.photos_url if
                              str(url) not in photos_to_remove]

            for photo in photos_to_add:
                updated_photos.append(photo)

        self.place_repo.update(place_id, update_data)
        return self.place_repo.get(place_id)

    def delete_place(self, place_id):
        """
        Delete a place by ID.
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None
        self.place_repo.delete(place_id)
        return ''

    # ------------------ Amenity management ------------------

    def create_amenity(self, amenity_data):
        """
        Create a new amenity.
        """
        amenity_in = AmenityCreate(**amenity_data)

        amenity = Amenity(
            id=str(uuid.uuid4()),
            name=amenity_in.name,
            description=amenity_in.description
        )

        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def get_amenity_by_name(self, amenity_name):
        """Retrieve an amenity by its name"""
        return self.amenity_repo.get_by_attribute("name", amenity_name)

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity.
        """
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    def delete_amenity(self, amenity_id):
        """Delete an amenity by ID."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        self.amenity_repo.delete(amenity_id)
        return ''

    # ------------------ Review management ------------------

    def create_review(self, review_data, booking_id, place_id, user_id):
        """
        Create a review only if booking is done and user visited the place.
        One review per booking.
        """
        booking = self.get_booking(booking_id)
        reviews = self.review_repo.get_all()
        user = self.get_user(user_id)
        for review in reviews:
            if review.booking == booking_id:
                raise PermissionError(
                    "User can review a place once per booking."
                    )

        if not self.user_repo.get(user_id):
            raise ValueError("User not found")
        if not self.place_repo.get(place_id):
            raise ValueError("Place not found")
        if not booking:
            raise ValueError("Booking not found")

        end_date_aware = ensure_aware(booking.end_date)

        if (booking.status != BookingStatus.DONE.value or
                end_date_aware >= datetime.now(timezone.utc)):
            raise PermissionError("User must visit the place to post review.")

        new_review = Review(
            id=str(uuid.uuid4()),
            comment=review_data.comment,
            rating=review_data.rating,
            booking=str(booking_id),
            place=str(place_id),
            user_ide=str(user_id),
            user_last_name=user.last_name,
            user_first_name=user.first_name
        )
        self.review_repo.add(new_review)
        return new_review

    def get_review(self, review_id):
        """Retrieve review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place."""
        return Review.query.filter(Review.place == str(place_id)).all()

    def update_review(self, review_id, review_data):
        """
        Update an existing review.
        """
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        """Delete a review by ID."""
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        return ''

    # ------------------ Booking management ------------------

    def create_booking(self, user_id, place_id, booking_data):
        """
        Create a new booking for a place by a user.
        """
        if not self.user_repo.get(user_id):
            raise ValueError("User not found")
        if not self.place_repo.get(place_id):
            raise ValueError("Place not found")
        new_booking = Booking(
            id=str(uuid.uuid4()),
            place=place_id,
            user=user_id,
            start_date=booking_data.start_date,
            end_date=booking_data.end_date,
            status=BookingStatus.PENDING.value
        )
        self.booking_repo.add(new_booking)
        return new_booking

    def get_booking(self, booking_id):
        """Retrieve booking by ID."""
        return self.booking_repo.get(booking_id)

    def get_all_bookings(self):
        """Retrieve all bookings."""
        return self.booking_repo.get_all()

    def get_booking_list_by_place(self, place_id):
        """Retrieve all bookings for a specific place."""
        return (
            db.session.query(Booking)
            .filter(Booking.place == str(place_id))
            .all()
        )

    def get_pending_booking_list_by_place(self, place_id):
        """Retrieve all pending bookings for a specific place."""
        return (
            db.session.query(Booking)
            .filter(Booking.place == str(place_id),
                    Booking.status == BookingStatus.PENDING.value)
            .all()
        )

    def get_booking_list_by_user(self, user_id):
        """Retrieve all bookings for a specific user."""
        return (
            db.session.query(Booking)
            .filter_by(user=user_id)
            .all()
        )

    def cancel_booking(self, booking_id):
        """
        Cancel a booking.
        Only the owner of the place or an admin can update booking status.
        """
        booking = self.get_booking(booking_id)
        if booking.status == BookingStatus.PENDING.value:
            booking.set_status(BookingStatus.CANCELLED.value)
        return booking

    def update_booking(self, booking_id, booking_data):
        """
        Update a booking.
        Only the owner of the place can update booking status.
        """
        booking = self.booking_repo.get(booking_id)
        if not booking:
            return None
        place_id = booking.place
        place = self.place_repo.get(place_id)
        user_id = booking.user
        user = self.get_user(user_id)

        if 'status' in booking_data:
            if (str(place.owner_id) != str(user_id)
               and not user.is_admin):
                raise PermissionError("Only the owner of a place or an admin"
                                      " can update the status")
            if booking_data['status'] not in ("DONE", "PENDING", "CANCELLED"):
                raise ValueError("Status must be DONE, PENDING, or CANCELLED")

        self.booking_repo.update(booking_id, booking_data)
        return self.booking_repo.get(booking_id)
    
    def manage_bookingstatus(self, booking_id):

        booking = self.get_booking(booking_id)
        now = datetime.now(timezone.utc)
        booking_end_aware = ensure_aware(booking.end_date)

        if (booking.status == BookingStatus.PENDING.value
           and now > booking_end_aware):
            booking.set_status(BookingStatus.DONE.value)
            self.booking_repo.update(booking_id, booking.__dict__)
        return booking.status
