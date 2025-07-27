from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app.models.place import PlaceCreate
import requests

bp_api = Blueprint('api', __name__)

@bp_api.route('/validate-photo', methods=['POST'])
@jwt_required()
def validate_photo():
    """Endpoint to validate a single photo URL before form submission"""
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"valid": False, "reason": "URL manquante"}), 400

    try:
        PlaceCreate.validate_image([url])
        return jsonify({"valid": True})
    except ValueError as e:
        return jsonify({"valid": False, "reason": str(e)}), 400
    
@bp_api.route('/geocode-address', methods=['POST'])
def geocode_address():
    address = request.json.get("address")
    if not address:
        return jsonify({"error": "Adresse manquante"}), 400

    try:
        api_key = current_app.config['LOCATIONIQ_KEY']
        response = requests.get(
            "https://us1.locationiq.com/v1/search.php",
            params={
                "key": api_key,
                "q": address,
                "format": "json"
            }
        )
        response.raise_for_status()
        results = response.json()
        if len(results) > 1:
            # Renvoie la liste des choix au front
            choices = [{
                "display_name": result["display_name"],
                "lat": result["lat"],
                "lon": result["lon"]
            } for result in results]
            return jsonify({
                "multiple_results": True,
                "choices": choices
            })
        else:
            result = results[0]
            return jsonify({
                "multiple_results": False,
                "lat": result["lat"],
                "lon": result["lon"],
                "display_name": result["display_name"]
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500