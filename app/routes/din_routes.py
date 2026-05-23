from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils.rbac import role_required


din_bp = Blueprint("din", __name__)


# ==========================
# DIN HEALTH
# ==========================
@din_bp.route("/health", methods=["GET"])
def din_health():

    return jsonify({
        "status": "success",
        "module": "DIN Verification Module",
        "message": "DIN module working successfully"
    }), 200


# ==========================
# DIN VERIFICATION
# ==========================
@din_bp.route("/verify", methods=["POST"])
@jwt_required()
@role_required("Admin", "Verifier")
def verify_din():

    data = request.get_json()

    candidate_name = data.get("candidate_name")
    din_number = data.get("din_number")

    return jsonify({
        "status": "success",
        "candidate_name": candidate_name,
        "din_number": din_number,
        "verification_status": "Verified"
    }), 200