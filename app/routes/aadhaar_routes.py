# from flask import Blueprint, request, jsonify
# from app.services.aadhaar_service import AadhaarService
# from flask_jwt_extended import jwt_required

# aadhaar_bp = Blueprint("aadhaar", __name__)

# # ==========================================
# # GENERATE QR
# # ==========================================

# @aadhaar_bp.route("/generate-qr", methods=["POST"])
# @jwt_required()
# def generate_qr():
#     try:
#         data = request.get_json()
#         if not data:
#             return jsonify({
#                 "status": "error",
#                 "message": "Request body is required"
#             }), 400

#         candidate_id = data.get("candidate_id")
#         bgv_id = data.get("bgv_id")

#         if not candidate_id:
#             return jsonify({
#                 "status": "error",
#                 "message": "candidate_id is required"
#             }), 400

#         if not bgv_id:
#             return jsonify({
#                 "status": "error",
#                 "message": "bgv_id is required"
#             }), 400

#         token = request.headers.get("Authorization")

#         result = AadhaarService.generate_qr(
#             candidate_id=candidate_id,
#             bgv_id=bgv_id,
#             token=token
#         )

#         return jsonify(result)

#     except Exception as error:
#         return jsonify({
#             "status": "error",
#             "message": str(error)
#         }), 500


# # ==========================================
# # FETCH STATUS
# # ==========================================

# @aadhaar_bp.route("/status/<int:candidate_id>", methods=["GET"])
# @jwt_required()
# def get_status(candidate_id):
#     try:
#         token = request.headers.get("Authorization")

#         result = AadhaarService.get_status(
#             candidate_id=candidate_id,
#             token=token
#         )

#         return jsonify(result)

#     except Exception as error:
#         return jsonify({
#             "status": "error",
#             "message": str(error)
#         }), 500


# # ==========================================
# # VERIFY AADHAAR
# # ==========================================

# @aadhaar_bp.route("/verify", methods=["POST"])
# @jwt_required()
# def verify_aadhaar():
#     try:
#         data = request.get_json()
#         if not data:
#             return jsonify({
#                 "status": "error",
#                 "message": "Request body is required"
#             }), 400

#         candidate_id = data.get("candidate_id")
#         bgv_id = data.get("bgv_id")
#         document_id = data.get("document_id")

#         if not candidate_id:
#             return jsonify({
#                 "status": "error",
#                 "message": "candidate_id is required"
#             }), 400

#         if not bgv_id:
#             return jsonify({
#                 "status": "error",
#                 "message": "bgv_id is required"
#             }), 400

#         if not document_id:
#             return jsonify({
#                 "status": "error",
#                 "message": "document_id is required"
#             }), 400

#         token = request.headers.get("Authorization")

#         result = AadhaarService.verify_aadhaar(
#             candidate_id=candidate_id,
#             bgv_id=bgv_id,
#             document_id=document_id,
#             token=token
#         )

#         return jsonify(result)

#     except Exception as error:
#         return jsonify({
#             "status": "error",
#             "message": str(error)
#         }), 500


# # ==========================================
# # GET RESULT
# # ==========================================

# @aadhaar_bp.route("/result/<int:candidate_id>", methods=["GET"])
# @jwt_required()
# def get_aadhaar_result(candidate_id):
#     try:
#         token = request.headers.get("Authorization")

#         result = AadhaarService.get_result(
#             candidate_id=candidate_id,
#             token=token
#         )

#         return jsonify(result), 200

#     except Exception as e:
#         return jsonify({
#             "success": False,
#             "message": str(e)
#         }), 500
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.aadhaar_service import AadhaarService


aadhaar_bp = Blueprint("aadhaar", __name__)


# ======================================================
# VERIFY AADHAAR
# ======================================================


@aadhaar_bp.route("/verify", methods=["POST"])
@jwt_required()
def verify_aadhaar():

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
        document_id = data.get("document_id")

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
        # Validate Aadhaar document
        # --------------------------------------------------

        if not document_id:
            return jsonify(
                {
                    "status": "error",
                    "message": "document_id is required",
                }
            ), 400

        # --------------------------------------------------
        # Authorization token
        # --------------------------------------------------

        token = request.headers.get("Authorization")

        # --------------------------------------------------
        # Aadhaar Verification
        # --------------------------------------------------

        result = AadhaarService.verify_aadhaar(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            document_id=document_id,
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
# GET AADHAAR RESULT
# ======================================================


@aadhaar_bp.route(
    "/result/<int:candidate_id>",
    methods=["GET"],
)
@jwt_required()
def get_aadhaar_result(candidate_id):

    try:
        token = request.headers.get("Authorization")

        result = AadhaarService.get_result(
            candidate_id=candidate_id,
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
# SAVE AADHAAR DECISION
# ======================================================


@aadhaar_bp.route("/decision", methods=["POST"])
@jwt_required()
def save_aadhaar_decision():

    try:
        data = request.get_json()

        if not data:
            return jsonify(
                {
                    "status": "error",
                    "message": "Request body is required",
                }
            ), 400

        result = AadhaarService.save_decision(data)

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
