from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.aadhaar_service import AadhaarService

aadhaar_bp = Blueprint("aadhaar", __name__)

@aadhaar_bp.route("/", methods=["GET"])
def health():
    return jsonify({"status":"success","message":"Aadhaar module health"}),200

@aadhaar_bp.route("/verify", methods=["POST"])
@jwt_required(optional=True)
def verify():
    data=request.get_json() or {}
    return jsonify(AadhaarService.verify(data)),200
