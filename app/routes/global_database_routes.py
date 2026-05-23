from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils.rbac import role_required


global_database_bp = Blueprint("global_database", __name__)


# ==========================
# GLOBAL DATABASE HEALTH
# ==========================
@global_database_bp.route("/health", methods=["GET"])
def global_database_health():

    return jsonify({
        "status": "success",
        "module": "Global Database Verification Module",
        "message": "Global database module working successfully"
    }), 200


# ==========================
# GLOBAL DATABASE VERIFICATION
# ==========================
@global_database_bp.route("/verify", methods=["POST"])
@jwt_required()
@role_required("Admin", "Verifier")
def verify_global_database():

    data = request.get_json()

    candidate_name = data.get("candidate_name")
    database_status = data.get("database_status")

    return jsonify({
        "status": "success",
        "candidate_name": candidate_name,
        "database_status": database_status,
        "verification_status": "Verified"
    }), 200