from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.education_service import EducationService

education_bp = Blueprint("education", __name__)

@education_bp.route("/", methods=["GET"])
def health():
    return jsonify({"status":"success","message":"Education module health"}),200

@education_bp.route("/verify", methods=["POST"])
@jwt_required(optional=True)
def verify():
    data=request.get_json() or {}
    return jsonify(EducationService.verify(data)),200
