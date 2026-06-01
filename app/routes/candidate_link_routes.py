from flask import Blueprint, request, jsonify

from app.services.candidate_link_service import (
    CandidateLinkService
)


candidate_link_bp = Blueprint(
    "candidate_link_bp",
    __name__
)


@candidate_link_bp.route(
    "/candidate/generate-link",
    methods=["POST"]
)
def generate_secure_link():

    try:

        data = request.get_json()

        result = (
            CandidateLinkService.generate_secure_link(data)
        )

        if result["status"] == "error":

            return jsonify(result), 400

        return jsonify(result), 201

    except Exception as e:

        import traceback
        traceback.print_exc()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
    
@candidate_link_bp.route(
    "/candidate/validate-link/<secure_token>",
    methods=["GET"]
)
def validate_secure_link(secure_token):

    try:

        result = (
            CandidateLinkService.validate_secure_link(
                secure_token
            )
        )

        if result["status"] == "error":

            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500