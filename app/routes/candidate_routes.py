from flask import Blueprint, request, jsonify

from app.services.candidate_service import CandidateService


candidate_bp = Blueprint(
    "candidate_bp",
    __name__
)


@candidate_bp.route(
    "/candidates/create",
    methods=["POST"]
)
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