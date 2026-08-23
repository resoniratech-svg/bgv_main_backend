from flask import Blueprint
from flask import request
from flask import jsonify
import traceback
from flask_jwt_extended import jwt_required

from app.services.employment_service import EmploymentService


employment_bp = Blueprint("employment", __name__)


# ======================================================
# VERIFY EMPLOYMENT
# ======================================================


@employment_bp.route("/verify", methods=["POST"])
@jwt_required()
def verify_employment():

    try:
        data = request.get_json()

        if not data:
            return jsonify(
                {"status": "error", "message": "Request body is required."}
            ), 400

        candidate_id = data.get("candidate_id")

        bgv_id = data.get("bgv_id")

        token = request.headers.get("Authorization")

        result = EmploymentService.verify_employment(
            candidate_id=candidate_id, bgv_id=bgv_id, token=token
        )

        return jsonify(result)

    except Exception as error:
        print("=" * 80)
        print("EMPLOYMENT VERIFICATION ERROR")
        traceback.print_exc()
        print("=" * 80)

        return jsonify({"status": "error", "message": str(error)}), 500


# ======================================================
# GET EMPLOYMENT RESULT
# ======================================================


@employment_bp.route("/result/<int:candidate_id>", methods=["GET"])
@jwt_required()
def get_employment_result(candidate_id):

    try:
        token = request.headers.get("Authorization")

        result = EmploymentService.get_result(candidate_id=candidate_id, token=token)

        return jsonify(result)

    except Exception as error:
        print("=" * 80)
        print("EMPLOYMENT RESULT ERROR")
        traceback.print_exc()
        print("=" * 80)

        return jsonify({"status": "error", "message": str(error)}), 500


# ======================================================
# SAVE EMPLOYMENT DECISION
# ======================================================


@employment_bp.route("/decision", methods=["POST"])
@jwt_required()
def save_employment_decision():

    try:
        data = request.get_json()

        if not data:
            return jsonify(
                {
                    "status": "error",
                    "message": "Request body is required",
                }
            ), 400

        result = EmploymentService.save_decision(data)

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
