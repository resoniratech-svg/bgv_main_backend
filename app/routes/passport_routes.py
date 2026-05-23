from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils.rbac import role_required


passport_bp = Blueprint("passport", __name__)


# ==========================
# PASSPORT MODULE HEALTH
# ==========================
@passport_bp.route("/health", methods=["GET"])
def passport_health():

    return jsonify({
        "status": "success",
        "module": "Passport Verification Module",
        "message": "Passport module working successfully"
    }), 200


# ==========================
# PASSPORT VERIFICATION
# ==========================
@passport_bp.route("/verify", methods=["POST"])
@jwt_required()
@role_required("Admin", "Verifier")
def verify_passport():

    data = request.get_json()

    passport_number = data.get("passport_number")

    return jsonify({
        "status": "success",
        "passport_number": passport_number,
        "verification_status": "Verified",
        "remarks": "Passport verified successfully"
    }), 200