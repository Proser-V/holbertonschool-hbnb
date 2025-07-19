from flask import Blueprint, abort, render_template, jsonify
from flask import request, flash, url_for, session, redirect
from uuid import UUID
from app.services import facade
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import datetime, timezone


bp_web = Blueprint('web', __name__)


@bp_web.route('/')
def index():
    places = facade.place_repo.get_all()
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    return render_template('index.html', places_list=places, now=now)


@bp_web.route('/place/<place_id>')
def show_place(place_id):
    try:
        UUID(place_id)
    except ValueError:
        abort(400, description="Invalid UUID")

    place = facade.get_place(place_id)
    if not place:
        abort(404, description="Place not found")

    return render_template("place.html", place=place, photos_url=place.photos_url or [], reviews_list=place.reviews or [])


@bp_web.route('/login')
def login():
    return render_template("login.html")

@bp_web.route('/logout')
def logout():
    return render_template("logout.html")

@bp_web.route('/new_user')
def new_user():
    return render_template("registration.html")