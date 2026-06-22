from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.services.pan_service import PanService

pan_bp = Blueprint("pan", __name__)


@pan_bp.route("/verify", methods=["POST"])
@jwt_required()
def verify_pan():
    try:
        data = request.get_json()
        token = request.headers.get("Authorization")

        result = PanService.verify_pan(data=data, token=token)

        if result.get("status") == "error":
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


@pan_bp.route("/result/<int:candidate_id>", methods=["GET"])
@jwt_required()
def get_pan_result(candidate_id):
    try:
        token = request.headers.get("Authorization")

        # Fixed: Changed PANService to PanService to match the import statement
        result = PanService.get_result(candidate_id, token)

        return jsonify({
            "status": "success",
            "data": result
        }), 200

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500