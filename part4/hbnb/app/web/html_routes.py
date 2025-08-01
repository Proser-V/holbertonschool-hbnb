from flask import Blueprint, abort, render_template
from flask import make_response
from uuid import UUID
from app.services import facade
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from datetime import datetime, timezone, timedelta

# Define the main web blueprint for route declarations
bp_web = Blueprint('web', __name__)

def get_first_available_date(bookings, now):
    """
    Calculate the earliest available date after all PENDING bookings.
    
    Args:
        bookings (list): List of booking objects.
        now (datetime): Reference date to start checking availability.
    
    Returns:
        datetime: First available date not covered by a pending booking.
    """

    # Filter only pending bookings and sort them by start date
    pending_bookings = sorted((b for b in bookings if b.status == "PENDING"),
                              key=lambda b: b.start_date)

    current = now
    # Loop through sorted bookings and find the next free slot
    for booking in pending_bookings:
        if booking.start_date > current:
            return current
        # Move current pointer to after the booking ends
        current = max(current, booking.end_date + timedelta(days=1))

    return current

@bp_web.route('/')
def index():
    """
    Home page route. Displays all available places and their next available booking date.
    """
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except:
        user_id = None

    places = facade.place_repo.get_all()
    # Get current date (naive UTC format) and compute tomorrow's date
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    tomorrow = now + timedelta(days=1)

    current_user = None
    if user_id:
        current_user = facade.get_user(user_id)

    # For each place, calculate the next available booking date
    for place in places:
        place.available_date = get_first_available_date(place.bookings, tomorrow)

    return render_template('index.html',
                           places_list=places,
                           now=now,
                           tomorrow=tomorrow,
                           current_user=current_user)

@bp_web.route('/under_construction')
def under_construction():
    """
    Route for an under-construction page.
    """
    return render_template("under_construction.html")

@bp_web.route('/login')
def login():
    """
    Login page route.
    """
    return render_template("login.html")

@bp_web.route('/admin_panel')
def admin_panel():
    """
    Admin panel route. Only accessible to authenticated admins.
    """
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        if not get_jwt().get("is_admin", False):
            return {"msg": "Accès refusé"}, 403
    except:
        user_id = None

    # Get all the informations for the admin panel
    users = facade.get_all_users()
    places = facade.place_repo.get_all()
    reviews = facade.get_all_reviews()
    bookings = facade.get_all_bookings()
    amenities = facade.get_all_amenities()

    current_user = None
    if user_id:
        current_user = facade.get_user(user_id)

    return render_template("admin_panel.html",
                           users=users,
                           places=places,
                           reviews=reviews,
                           bookings=bookings,
                           amenities=amenities,
                           current_user=current_user)

@bp_web.route('/logout')
def logout():
    """
    Logout route. Clears JWT cookies and redirects to home page.
    """
    response = make_response("""
        <script>
            alert("A bientôt sur HBnB");
            window.location.href = "/";
        </script>
    """)
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response

@bp_web.route('/new_user')
def new_user():
    """
    Route to register a new user.
    """
    return render_template("registration.html")

@bp_web.route('/user/<user_id>/profile')
def user_profile(user_id):
    """
    Display a user's profile, including their places and availability.
    """
    try:
        UUID(user_id)
    except ValueError:
        abort(400, description="Invalid UUID")

    # Get current date (naive UTC format) and compute tomorrow's date
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    tomorrow = now + timedelta(days=1)
    user = facade.get_user(user_id)

    # For each place, calculate the next available booking date
    for place in user.places:
        place.available_date = get_first_available_date(place.bookings, tomorrow)

    return render_template("user_profile.html", user=user, now=now, tomorrow=tomorrow)


@bp_web.route('/booking/<place_id>')
def new_booking(place_id):
    """
    Booking form page for a given place.
    """
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except:
        user_id = None

    place = facade.get_place(place_id)
    current_user = None
    if user_id:
        current_user = facade.get_user(user_id)


    # Get current date (naive UTC format) and compute tomorrow's date
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    tomorrow = now + timedelta(days=1)

    # Extract non-cancelled booking date ranges for use in templates
    ranges = [
        {
            "start_date": booking.start_date.strftime("%Y-%m-%d"),
            "end_date": booking.end_date.strftime("%Y-%m-%d")
        }
        for booking in place.bookings if booking.status != 'CANCELLED'
    ]

    # For the place, calculate the next available booking date
    place.available_date = get_first_available_date(place.bookings, tomorrow)

    return render_template("booking.html",
                           place=place,
                           now=now,
                           tomorrow=tomorrow,
                           photos_url=place.photos_url or [],
                           reviews_list=place.reviews or [],
                           current_user=current_user,
                           bookings=ranges)

@bp_web.route('/reviews/from_booking/<booking_id>')
def add_review(booking_id):
    """
    Route to add a review for a specific booking.
    """
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except:
        user_id = None
    booking = facade.get_booking(booking_id)
    place = facade.get_place(booking.place)
    current_user = None
    if user_id:
        current_user = facade.get_user(user_id)

    return render_template("add_review.html",
                           booking=booking,
                           place=place,
                           photos_url=place.photos_url or [],
                           current_user=current_user)

@bp_web.route('/new_place')
def add_place():
    """
    Route to render the form to add a new place.
    """
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except:
        user_id = None

    current_user = None
    if user_id:
        current_user = facade.get_user(user_id)

    return render_template("add_place.html",
                           current_user=current_user)

@bp_web.route('/place/<place_id>/update')
def update_place(place_id):
    """
    Route to render the form to update an existing place.
    """
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except:
        user_id = None

    current_user = None
    if user_id:
        current_user = facade.get_user(user_id)

    place = facade.get_place(place_id)

    return render_template("update_place.html",
                           current_user=current_user,
                           place=place)

@bp_web.route('/place/<place_id>/show_photos')
def show_photos(place_id):
    """
    Route to display all photos for a given place.
    """
    try:
        UUID(place_id)
    except ValueError:
        abort(400, description="Invalid UUID")
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except:
        user_id = None

    place = facade.get_place(place_id)
    if not place:
        abort(404, description="Place not found")

    current_user = None
    if user_id:
        current_user = facade.get_user(user_id)

    return render_template("place-all-photos.html",
                           place=place,
                           photos_url=place.photos_url or [],
                           current_user=current_user)

@bp_web.route('/place/<place_id>/show_reviews')
def show_reviews(place_id):
    """
    Route to display all reviews for a given place.
    """
    try:
        UUID(place_id)
    except ValueError:
        abort(400, description="Invalid UUID")
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except:
        user_id = None

    place = facade.get_place(place_id)
    if not place:
        abort(404, description="Place not found")

    current_user = None
    if user_id:
        current_user = facade.get_user(user_id)

    return render_template("place-all-reviews.html",
                           place=place,
                           current_user=current_user)

@bp_web.route('/place/<place_id>')
def show_place(place_id):
    """
    Route to display a single place's details, photos, and reviews.
    """
    try:
        UUID(place_id)
    except ValueError:
        abort(400, description="Invalid UUID")
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except:
        user_id = None

    place = facade.get_place(place_id)

    # Get current date (naive UTC format) and compute tomorrow's date
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    tomorrow = now + timedelta(days=1)

    if not place:
        abort(404, description="Place not found")

    current_user = None
    if user_id:
        current_user = facade.get_user(user_id)

    # For the place, calculate the next available booking date
    place.available_date = get_first_available_date(place.bookings, tomorrow)

    return render_template("place.html",
                           place=place,
                           photos_url=place.photos_url or [],
                           reviews_list=place.reviews or [],
                           now=now,
                           tomorrow=tomorrow,
                           current_user=current_user)

@bp_web.route('/place/<place_id>/bookings')
def place_bookings(place_id):
    """
    Route to show all bookings for a given place.
    """
    try:
        UUID(place_id)
    except ValueError:
        abort(400, description="Invalid UUID")
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except:
        user_id = None

    place = facade.get_place(place_id)
    if not place:
        abort(404, description="Place not found")

    current_user = None
    if user_id:
        current_user = facade.get_user(user_id)

    return render_template("place-all-bookings.html",
                           place=place,
                           bookings=place.bookings,
                           current_user=current_user)
