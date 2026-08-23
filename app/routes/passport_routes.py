from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.passport_service import PassportService


passport_bp = Blueprint("passport", __name__)


# ======================================================
# VERIFY PASSPORT
# ======================================================


@passport_bp.route("/verify", methods=["POST"])
@jwt_required()
def verify_passport():

    try:
        data = request.get_json()

        if not data:
            return jsonify(
                {
                    "status": "error",
                    "message": "Request body is required",
                }
            ), 400

        candidate_id = data.get("candidate_id")
        bgv_id = data.get("bgv_id")

        # Passport requires FRONT + BACK
        front_document_id = data.get("front_document_id")
        back_document_id = data.get("back_document_id")

        # --------------------------------------------------
        # Validate candidate
        # --------------------------------------------------

        if not candidate_id:
            return jsonify(
                {
                    "status": "error",
                    "message": "candidate_id is required",
                }
            ), 400

        # --------------------------------------------------
        # Validate BGV
        # --------------------------------------------------

        if not bgv_id:
            return jsonify(
                {
                    "status": "error",
                    "message": "bgv_id is required",
                }
            ), 400

        # --------------------------------------------------
        # Validate Passport Front
        # --------------------------------------------------

        if not front_document_id:
            return jsonify(
                {
                    "status": "error",
                    "message": "front_document_id is required",
                }
            ), 400

        # --------------------------------------------------
        # Validate Passport Back
        # --------------------------------------------------

        if not back_document_id:
            return jsonify(
                {
                    "status": "error",
                    "message": "back_document_id is required",
                }
            ), 400

        # --------------------------------------------------
        # Authorization token
        # --------------------------------------------------

        token = request.headers.get("Authorization")

        # --------------------------------------------------
        # Passport Verification
        # --------------------------------------------------

        result = PassportService.verify_passport(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            front_document_id=front_document_id,
            back_document_id=back_document_id,
            token=token,
        )

        return jsonify(result), 200

    except Exception as error:
        import traceback

        traceback.print_exc()

        return jsonify(
            {
                "status": "error",
                "message": str(error),
            }
        ), 500


# ======================================================
# GET PASSPORT RESULT
# ======================================================


@passport_bp.route(
    "/result/<int:candidate_id>",
    methods=["GET"],
)
@jwt_required()
def get_passport_result(candidate_id):

    try:
        token = request.headers.get("Authorization")

        result = PassportService.get_result(
            candidate_id,
            token,
        )

        return jsonify(result), 200

    except Exception as error:
        import traceback

        traceback.print_exc()

        return jsonify(
            {
                "status": "error",
                "message": str(error),
            }
        ), 500


# ======================================================
# SAVE PASSPORT DECISION
# ======================================================


@passport_bp.route("/decision", methods=["POST"])
@jwt_required()
def save_passport_decision():

    try:
        data = request.get_json()

        result = PassportService.save_decision(data)

        return jsonify(result), 200

    except Exception as error:
        import traceback

        traceback.print_exc()

        return jsonify(
            {
                "status": "error",
                "message": str(error),
            }
        ), 500
