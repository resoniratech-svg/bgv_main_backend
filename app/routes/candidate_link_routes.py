from flask import Blueprint, request, jsonify

from app.services.candidate_link_service import CandidateLinkService

from app.services.aadhaar_service import AadhaarService
from app.repositories.candidate_link_repository import CandidateLinkRepository

candidate_link_bp = Blueprint("candidate_link_bp", __name__)


@candidate_link_bp.route("/candidate/generate-link", methods=["POST"])
def generate_secure_link():

    try:
        data = request.get_json()

        result = CandidateLinkService.generate_secure_link(data)

        if result["status"] == "error":
            return jsonify(result), 400

        return jsonify(result), 201

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify({"status": "error", "message": str(e)}), 500


@candidate_link_bp.route("/candidate/validate-link/<secure_token>", methods=["GET"])
def validate_secure_link(secure_token):

    try:
        result = CandidateLinkService.validate_secure_link(secure_token)

        if result["status"] == "error":
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@candidate_link_bp.route("/candidate/aadhaar-consent/<secure_token>", methods=["POST"])
def aadhaar_consent(secure_token):

    try:
        result = CandidateLinkRepository.validate_secure_token(secure_token)

        if result["status"] == "error":
            return jsonify(result), 400

        candidate_id = result["data"]["candidate_id"]

        bgv_id = result["data"]["bgv_id"]

        response = AadhaarService.generate_qr(candidate_id, bgv_id, None)

        return jsonify(response)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@candidate_link_bp.route("/candidate/aadhaar-status/<secure_token>", methods=["GET"])
def aadhaar_status(secure_token):

    try:
        result = CandidateLinkRepository.validate_secure_token(secure_token)

        if result["status"] == "error":
            return jsonify(result), 400

        candidate_id = result["data"]["candidate_id"]

        response = AadhaarService.get_status(candidate_id, None)

        return jsonify(response)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
