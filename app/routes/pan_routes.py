from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.pan_service import PanService

pan_bp = Blueprint("pan", __name__)

@pan_bp.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "Pan module health"
    }), 200


@pan_bp.route("/verify", methods=["POST"])
@jwt_required(optional=True)
def verify():

    data = request.get_json() or {}

    return jsonify(
        PanService.verify(data)
    ), 200