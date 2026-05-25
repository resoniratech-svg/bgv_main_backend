from flask import Blueprint, request, jsonify

from app.services.submission_service import (
    SubmissionService
)

submission_bp = Blueprint(
    "submission_bp",
    __name__
)


@submission_bp.route(
    "/candidate/submit-documents",
    methods=["POST"]
)
def submit_documents():

    try:

        data = request.get_json()

        secure_token = data.get(
            "secure_token"
        )

        remarks = data.get(
            "remarks"
        )

        result = (
            SubmissionService.submit_documents(
                secure_token,
                remarks
            )
        )

        if result["status"] == "error":

            return jsonify(result), 400

        return jsonify(result), 201

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500