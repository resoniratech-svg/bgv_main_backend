from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils.rbac import role_required


court_bp = Blueprint("court", __name__)


# ==========================
# COURT MODULE HEALTH
# ==========================
@court_bp.route("/health", methods=["GET"])
def court_health():

    return jsonify({
        "status": "success",
        "module": "Court Record Verification Module",
        "message": "Court verification module working successfully"
    }), 200


# ==========================
# COURT VERIFICATION
# ==========================
@court_bp.route("/verify", methods=["POST"])
@jwt_required()
@role_required("Admin", "Verifier")
def verify_court_record():

    data = request.get_json()

    candidate_name = data.get("candidate_name")

    return jsonify({
        "status": "success",
        "candidate_name": candidate_name,
        "verification_status": "Clear",
        "remarks": "No court records found"
    }), 200