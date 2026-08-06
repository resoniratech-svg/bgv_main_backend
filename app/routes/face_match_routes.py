from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.face_match_service import FaceMatchService

face_match_bp = Blueprint("face_match", __name__)


@face_match_bp.route("/", methods=["GET"])
def health():
    return jsonify({"status": "success", "message": "FaceMatch module health"}), 200


@face_match_bp.route("/face-match/verify", methods=["POST"])
@jwt_required()
def verify_face_match():

    try:
        data = request.get_json()

        token = request.headers.get("Authorization")

        result = FaceMatchService.verify_face(
            data=data,
            token=token,
        )

        if result.get("status") == "error":
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as error:
        return jsonify(
            {
                "status": "error",
                "message": str(error),
            }
        ), 500


@face_match_bp.route("/face-match/result/<int:candidate_id>", methods=["GET"])
@jwt_required()
def get_face_match_result(candidate_id):

    try:
        token = request.headers.get("Authorization")

        result = FaceMatchService.get_result(
            candidate_id,
            token,
        )

        return jsonify(
            {
                "status": "success",
                "data": result,
            }
        ), 200

    except Exception as error:
        return jsonify(
            {
                "status": "error",
                "message": str(error),
            }
        ), 500


@face_match_bp.route("/face-match/decision", methods=["POST"])
@jwt_required()
def save_face_match_decision():

    try:
        data = request.get_json()

        result = FaceMatchService.save_decision(data)

        return jsonify(result), 200

    except Exception as error:
        return jsonify(
            {
                "status": "error",
                "message": str(error),
            }
        ), 500
