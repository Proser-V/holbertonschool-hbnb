from app.models.amenity import Amenity
from sqlalchemy import delete
from app.models.user import RevokedToken
from datetime import datetime, timezone
from extensions import db
import requests
import re


def delete_invalid_amenities():
    """
    """
    result = db.session.execute(
        delete(Amenity).where(Amenity.id.like('<function uuid4%'))
    )
    db.session.commit()
    print(f"{result.rowcount} amenities invalides supprimées")


def purge_expired_tokens():
    """
    """
    now = datetime.now(timezone.utc)
    expired = RevokedToken.query.filter(RevokedToken.expires_at < now).all()

    for token in expired:
        db.session.delete(token)

    db.session.commit()

def clean_city_name(name):
    """Retire les caractères non-latins si possible."""
    if name is None:
        return None
    return name.strip()

def geolocation(lat, lon):
    try:
        response = requests.get(
            "https://eu1.locationiq.com/v1/reverse",
            params={
                "key": "pk.84031ba5f6aff806113e746e96348592",
                "lat": lat,
                "lon": lon,
                "format": "json",
                "accept-language": "fr"
            },
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        address = data.get("address", {})
        for key in ("city", "town", "village", "municipality", "county"):
            name = address.get(key)
            if name:
                return name
        return "Localisation inconnue"

    except Exception as e:
        print("Erreur LocationIQ:", e)
        return "Localisation inconnue"
