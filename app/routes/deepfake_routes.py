from flask import Blueprint
from flask import jsonify
from flask import request

from flask_jwt_extended import jwt_required

from app.services.deepfake_service import DeepfakeService

from app.repositories.candidate_repository import CandidateRepository


deepfake_bp = Blueprint("deepfake", __name__)

print("DEEPFAKE ROUTES FILE IMPORTED")
# ==========================================
# VERIFY
# ==========================================


@deepfake_bp.route("/verify/<int:candidate_id>", methods=["POST"])
@jwt_required()
def verify_deepfake(candidate_id):

    candidate = CandidateRepository.get_candidate_by_id(candidate_id)

    if not candidate:
        return jsonify({"success": False, "message": "Candidate not found"}), 404

    token = request.headers.get("Authorization")

    result = DeepfakeService.verify(candidate_id, candidate["bgv_id"], token)

    return jsonify(result)


# ==========================================
# RESULT
# ==========================================


@deepfake_bp.route("/result/<int:candidate_id>", methods=["GET"])
@jwt_required()
def get_result(candidate_id):

    token = request.headers.get("Authorization")

    result = DeepfakeService.get_result(candidate_id, token)

    return jsonify(result)


@deepfake_bp.route("/decision", methods=["POST"])
@jwt_required()
def save_deepfake_decision():

    try:
        data = request.get_json()

        result = DeepfakeService.save_decision(data)

        return jsonify(result), 200

    except Exception as error:
        return jsonify({"success": False, "message": str(error)}), 500
