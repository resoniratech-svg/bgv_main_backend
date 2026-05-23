from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils.rbac import role_required


reference_bp = Blueprint("reference", __name__)


# ==========================
# REFERENCE HEALTH
# ==========================
@reference_bp.route("/health", methods=["GET"])
def reference_health():

    return jsonify({
        "status": "success",
        "module": "Reference Check Module",
        "message": "Reference module working successfully"
    }), 200


# ==========================
# REFERENCE VERIFICATION
# ==========================
@reference_bp.route("/verify", methods=["POST"])
@jwt_required()
@role_required("Admin", "Verifier")
def verify_reference():

    data = request.get_json()

    candidate_name = data.get("candidate_name")
    reference_status = data.get("reference_status")

    return jsonify({
        "status": "success",
        "candidate_name": candidate_name,
        "reference_status": reference_status,
        "verification_status": "Verified"
    }), 200