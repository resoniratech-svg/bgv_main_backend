from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.resume_service import ResumeService

resume_bp = Blueprint("resume", __name__)


@resume_bp.route("/", methods=["GET"])
def health():

    return jsonify({"status": "success", "message": "Resume module health"}), 200


@resume_bp.route("/parse", methods=["POST"])
@jwt_required(optional=True)
def parse_resume():

    try:
        data = request.get_json() or {}

        candidate_id = data.get("candidate_id")

        if not candidate_id:
            return jsonify(
                {"status": "error", "message": "candidate_id is required"}
            ), 400

        result = ResumeService.parse_resume(candidate_id)

        return jsonify(result), 200

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify({"status": "error", "message": str(e)}), 500


@resume_bp.route("/<int:candidate_id>", methods=["GET"])
@jwt_required(optional=True)
def get_parsed_resume(candidate_id):

    try:
        result = ResumeService.get_parsed_resume(candidate_id)

        return jsonify(result), 200

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify({"status": "error", "message": str(e)}), 500


@resume_bp.route("/<int:candidate_id>/decision", methods=["PUT"])
@jwt_required(optional=True)
def update_resume_decision(candidate_id):

    try:
        data = request.get_json() or {}

        decision = data.get("decision")

        result = ResumeService.update_decision(candidate_id, decision)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
