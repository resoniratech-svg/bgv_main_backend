from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.candidate_service import CandidateService


candidate_bp = Blueprint(
    "candidate_bp",
    __name__
)


@candidate_bp.route(
    "/candidates",
    methods=["GET"]
)
@jwt_required()
def get_all_candidates():
    try:
        candidates = CandidateService.get_all_candidates()
        return jsonify(candidates), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@candidate_bp.route(
    "/candidates/<int:candidate_id>",
    methods=["GET"]
)
@jwt_required()
def get_candidate(candidate_id):
    try:
        candidate = CandidateService.get_candidate_by_id(candidate_id)
        if not candidate:
            return jsonify({"status": "error", "message": "Candidate not found"}), 404
        return jsonify(candidate), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@candidate_bp.route(
    "/candidates/create",
    methods=["POST"]
)
@jwt_required()
def create_candidate():

    try:

        data = request.get_json()

        result = CandidateService.create_candidate(data)

        if result["status"] == "error":

            return jsonify(result), 400

        return jsonify(result), 201

    except Exception as e:
        error_message = str(e)
        if "Duplicate entry" in error_message:
            return jsonify({
                "status": "error",
                "message": "Candidate email already exists"
            }), 400
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500