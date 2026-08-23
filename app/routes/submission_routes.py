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

    print("################################")
    print("SUBMIT DOCUMENTS API HIT")
    print("################################")

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "status": "error",
                "message": "Request body is missing"
            }), 400

        secure_token = data.get(
            "secure_token"
        )

        remarks = data.get(
            "remarks"
        )

        print(
            "SECURE TOKEN:",
            secure_token
        )

        result = (
            SubmissionService.submit_documents(
                secure_token,
                remarks
            )
        )

        print(
            "SERVICE RESULT:",
            result
        )

        if result["status"] == "error":

            return jsonify(result), 400

        print(
            "RETURNING SUCCESS"
        )

        return jsonify(result), 200

    except Exception as e:

        import traceback
        traceback.print_exc()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500