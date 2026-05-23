from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils.rbac import role_required


credit_check_bp = Blueprint("credit_check", __name__)


# ==========================
# CREDIT CHECK HEALTH
# ==========================
@credit_check_bp.route("/health", methods=["GET"])
def credit_check_health():

    return jsonify({
        "status": "success",
        "module": "Credit Check Module",
        "message": "Credit check module working successfully"
    }), 200


# ==========================
# CREDIT CHECK VERIFICATION
# ==========================
@credit_check_bp.route("/verify", methods=["POST"])
@jwt_required()
@role_required("Admin", "Verifier")
def verify_credit_check():

    data = request.get_json()

    candidate_name = data.get("candidate_name")
    credit_score = data.get("credit_score")

    return jsonify({
        "status": "success",
        "candidate_name": candidate_name,
        "credit_score": credit_score,
        "verification_status": "Verified"
    }), 200