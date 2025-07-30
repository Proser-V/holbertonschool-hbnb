from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app.models.place import PlaceCreate
import requests

# Define the API blueprint for backend utility endpoints
bp_api = Blueprint('api', __name__)  # Front-end helper routes

@bp_api.route('/validate-photo', methods=['POST'])
@jwt_required()
def validate_photo():
    """Endpoint to validate a single photo URL before form submission"""

    # Parse the JSON request body and extract the image URL
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"valid": False, "reason": "URL manquante"}), 400

    try:
        # Use pydantic model's validator to check image validity
        PlaceCreate.validate_image([url])
        return jsonify({"valid": True})
    except ValueError as e:
        return jsonify({"valid": False, "reason": str(e)}), 400
    
@bp_api.route('/geocode-address', methods=['POST'])
def geocode_address():
    """
    Endpoint to geocode a postal address into latitude/longitude coordinates using LocationIQ API.
    """

    # Get the address field from the request JSON body
    address = request.json.get("address")
    if not address:
        return jsonify({"error": "Adresse manquante"}), 400

    try:
        # Retrieve the LocationIQ API key from the Flask config
        api_key = current_app.config['LOCATIONIQ_KEY']
        # Send a GET request to LocationIQ search endpoint
        response = requests.get(
            "https://us1.locationiq.com/v1/search.php",
            params={
                "key": api_key,
                "q": address,
                "format": "json"
            }
        )

        # Raise exception if response status is not OK
        response.raise_for_status()

        # Parse the JSON response (should be a list of results)
        results = response.json()
        if len(results) > 1:
            # If multiple results found, return all as selectable choices
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
            # Only one result: return its coordinates directly
            result = results[0]
            return jsonify({
                "multiple_results": False,
                "lat": result["lat"],
                "lon": result["lon"],
                "display_name": result["display_name"]
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
