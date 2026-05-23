from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.face_match_service import FaceMatchService

face_match_bp = Blueprint("face_match", __name__)

@face_match_bp.route("/", methods=["GET"])
def health():
    return jsonify({"status":"success","message":"FaceMatch module health"}),200

@face_match_bp.route("/verify", methods=["POST"])
@jwt_required(optional=True)
def verify():
    data=request.get_json() or {}
    return jsonify(FaceMatchService.verify(data)),200
