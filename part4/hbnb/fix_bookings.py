from app import create_app, db
from app.models import Booking
from datetime import timezone

app = create_app()  # adapte si tu as une factory ou change selon ton projet

with app.app_context():
    bookings = Booking.query.all()
    for booking in bookings:
        if booking.start_date.tzinfo is None:
            booking.start_date = booking.start_date.replace(tzinfo=timezone.utc)
        if booking.end_date.tzinfo is None:
            booking.end_date = booking.end_date.replace(tzinfo=timezone.utc)

    db.session.commit()
    print(f"{len(bookings)} bookings fixed.")
