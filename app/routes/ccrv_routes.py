# from flask import Blueprint
# from flask import request
# from flask import jsonify

# from flask_jwt_extended import jwt_required

# from app.services.ccrv_service import CCRVService


# ccrv_bp = Blueprint("ccrv", __name__)


# # ======================================================
# # VERIFY CCRV
# # ======================================================


# @ccrv_bp.route("/verify", methods=["POST"])
# @jwt_required()
# def verify_ccrv():

#     try:
#         data = request.get_json()

#         candidate_id = data.get("candidate_id")

#         bgv_id = data.get("bgv_id")

#         token = request.headers.get("Authorization")

#         result = CCRVService.verify_ccrv(candidate_id, bgv_id, token)

#         return jsonify(result)

#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500


# # ======================================================
# # GET CCRV RESULT
# # ======================================================


# @ccrv_bp.route("/result/<int:candidate_id>", methods=["GET"])
# @jwt_required()
# def get_ccrv_result(candidate_id):

#     try:
#         token = request.headers.get("Authorization")

#         result = CCRVService.get_result(candidate_id, token)

#         return jsonify(result)

#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500
from flask import Blueprint
from flask import request
from flask import jsonify

from flask_jwt_extended import jwt_required

from app.services.ccrv_service import CCRVService


ccrv_bp = Blueprint("ccrv", __name__)


# ======================================================
# VERIFY CCRV
# ======================================================


@ccrv_bp.route("/verify", methods=["POST"])
@jwt_required()
def verify_ccrv():

    try:
        data = request.get_json()

        candidate_id = data.get("candidate_id")

        bgv_id = data.get("bgv_id")

        token = request.headers.get("Authorization")

        result = CCRVService.verify_ccrv(
            candidate_id,
            bgv_id,
            token,
        )

        return jsonify(result)

    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": str(e),
            }
        ), 500


# ======================================================
# GET CCRV RESULT
# ======================================================


@ccrv_bp.route("/result/<int:candidate_id>", methods=["GET"])
@jwt_required()
def get_ccrv_result(candidate_id):

    try:
        token = request.headers.get("Authorization")

        result = CCRVService.get_result(
            candidate_id,
            token,
        )

        return jsonify(result)

    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": str(e),
            }
        ), 500


# ======================================================
# SAVE CCRV DECISION
# ======================================================


@ccrv_bp.route("/decision", methods=["POST"])
@jwt_required()
def save_ccrv_decision():

    try:
        data = request.get_json()

        # =================================================
        # REQUEST BODY VALIDATION
        # =================================================

        if not data:
            return jsonify(
                {
                    "status": "error",
                    "message": "Request body is required",
                }
            ), 400

        # =================================================
        # SAVE DECISION
        # =================================================

        result = CCRVService.save_decision(data)

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
