from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.employment_service import EmploymentService

employment_bp = Blueprint("employment", __name__)

@employment_bp.route("/", methods=["GET"])
def health():
    return jsonify({"status":"success","message":"Employment module health"}),200

@employment_bp.route("/verify", methods=["POST"])
@jwt_required(optional=True)
def verify():
    data=request.get_json() or {}
    return jsonify(EmploymentService.verify(data)),200
