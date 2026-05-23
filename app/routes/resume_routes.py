from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.resume_service import ResumeService

resume_bp = Blueprint("resume", __name__)

@resume_bp.route("/", methods=["GET"])
def health():
    return jsonify({"status":"success","message":"Resume module health"}),200

@resume_bp.route("/verify", methods=["POST"])
@jwt_required(optional=True)
def verify():
    data=request.get_json() or {}
    return jsonify(ResumeService.verify(data)),200
