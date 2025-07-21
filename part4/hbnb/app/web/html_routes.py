from flask import Blueprint, abort, render_template
from flask import make_response
from uuid import UUID
from app.services import facade
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from datetime import datetime, timezone, timedelta


bp_web = Blueprint('web', __name__)


@bp_web.route('/')
def index():
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except:
        user_id = None

    places = facade.place_repo.get_all()
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    tomorrow = now + timedelta(days=1)

    current_user = None
    if user_id:
        current_user = facade.get_user(user_id)
    return render_template('index.html',
                           places_list=places,
                           now=now,
                           tomorrow=tomorrow,
                           current_user=current_user)


@bp_web.route('/place/<place_id>')
def show_place(place_id):
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
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    tomorrow = now + timedelta(days=1)
    if not place:
        abort(404, description="Place not found")

    current_user = None
    if user_id:
        current_user = facade.get_user(user_id)

    return render_template("place.html",
                           place=place,
                           photos_url=place.photos_url or [],
                           reviews_list=place.reviews or [],
                           now=now,
                           tomorrow=tomorrow,
                           current_user=current_user)


@bp_web.route('/login')
def login():
    return render_template("login.html")

@bp_web.route('/logout')
def logout():
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
    return render_template("registration.html")

@bp_web.route('/booking/<place_id>')
def new_booking(place_id):
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except:
        user_id = None

    place = facade.get_place(place_id)
    current_user = None
    if user_id:
        current_user = facade.get_user(user_id)

    ranges = [{"start_date": booking.start_date.strftime("%Y-%m-%d"), "end_date": booking.end_date.strftime("%Y-%m-%d")} for booking in place.bookings if booking.status != 'CANCELLED']

    return render_template("booking.html", place=place, photos_url=place.photos_url or [], reviews_list=place.reviews or [], current_user=current_user, bookings=ranges)

@bp_web.route('/review')
def add_review():
    return render_template("review.html")