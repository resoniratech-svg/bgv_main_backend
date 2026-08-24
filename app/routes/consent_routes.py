# from flask import Blueprint
# from flask import request
# from flask import jsonify

# # from flask_jwt_extended import jwt_required

# from app.services.consent_service import ConsentService

# from app.repositories.candidate_link_repository import CandidateLinkRepository

# consent_bp = Blueprint("consent_bp", __name__)


# ########################################################
# # SAVE CANDIDATE CONSENT
# ########################################################


# @consent_bp.route("/candidate-consent", methods=["POST"])
# def save_candidate_consent():

#     try:
#         data = request.get_json()

#         candidate_id = data.get("candidate_id")

#         bgv_id = data.get("bgv_id")

#         verification_type = data.get("verification_type")

#         consent_status = data.get("consent_status")

#         consent_text = data.get("consent_text")

#         consent_version = data.get("consent_version")

#         consent_source = data.get("consent_source", "PORTAL")

#         ####################################################
#         # VALIDATIONS
#         ####################################################

#         if not candidate_id:
#             return jsonify(
#                 {"status": "error", "message": "candidate_id is required."}
#             ), 400

#         if not bgv_id:
#             return jsonify({"status": "error", "message": "bgv_id is required."}), 400

#         if not verification_type:
#             return jsonify(
#                 {"status": "error", "message": "verification_type is required."}
#             ), 400

#         if not consent_status:
#             return jsonify(
#                 {"status": "error", "message": "consent_status is required."}
#             ), 400

#         if not consent_text:
#             return jsonify(
#                 {"status": "error", "message": "consent_text is required."}
#             ), 400

#         ####################################################
#         # JWT TOKEN
#         ####################################################

#         token = request.headers.get("Authorization")

#         ####################################################
#         # CALL AI SERVICE
#         ####################################################

#         result = ConsentService.save_candidate_consent(
#             candidate_id=candidate_id,
#             bgv_id=bgv_id,
#             verification_type=verification_type,
#             consent_status=consent_status,
#             consent_text=consent_text,
#             consent_version=consent_version,
#             consent_source=consent_source,
#             token=token,
#         )

#         return jsonify(result), 200

#     except Exception as error:
#         return jsonify({"status": "error", "message": str(error)}), 500


# ########################################################
# # GET CANDIDATE CONSENT
# ########################################################


# @consent_bp.route("/candidate-consent/<int:candidate_id>", methods=["GET"])
# @jwt_required()
# def get_candidate_consent(candidate_id):

#     try:
#         bgv_id = request.args.get("bgv_id")

#         verification_type = request.args.get("verification_type")

#         if not verification_type:
#             return jsonify(
#                 {"status": "error", "message": "verification_type is required."}
#             ), 400

#         token = request.headers.get("Authorization")

#         result = ConsentService.get_candidate_consent(
#             candidate_id=candidate_id,
#             bgv_id=bgv_id,
#             verification_type=verification_type,
#             token=token,
#         )

#         return jsonify(result), 200

#     except Exception as error:
#         return jsonify({"status": "error", "message": str(error)}), 500
from flask import Blueprint
from flask import request
from flask import jsonify

from app.services.consent_service import ConsentService
from app.repositories.candidate_link_repository import CandidateLinkRepository

consent_bp = Blueprint("consent_bp", __name__)


########################################################
# SAVE CANDIDATE CONSENT
# Candidate Portal -> secure_token authentication
########################################################


@consent_bp.route("/candidate-consent", methods=["POST"])
def save_candidate_consent():

    try:
        data = request.get_json() or {}

        secure_token = data.get("secure_token")

        candidate_id = data.get("candidate_id")
        bgv_id = data.get("bgv_id")
        verification_type = data.get("verification_type")
        consent_status = data.get("consent_status")
        consent_text = data.get("consent_text")
        consent_version = data.get("consent_version")
        consent_source = data.get("consent_source", "PORTAL")

        ####################################################
        # VALIDATIONS
        ####################################################

        if not secure_token:
            return jsonify(
                {"status": "error", "message": "secure_token is required"}
            ), 400

        if not candidate_id:
            return jsonify(
                {"status": "error", "message": "candidate_id is required."}
            ), 400

        if not bgv_id:
            return jsonify({"status": "error", "message": "bgv_id is required."}), 400

        if not verification_type:
            return jsonify(
                {"status": "error", "message": "verification_type is required."}
            ), 400

        if not consent_status:
            return jsonify(
                {"status": "error", "message": "consent_status is required."}
            ), 400

        if not consent_text:
            return jsonify(
                {"status": "error", "message": "consent_text is required."}
            ), 400

        ####################################################
        # VALIDATE SECURE TOKEN
        ####################################################

        link_result = CandidateLinkRepository.validate_secure_token(secure_token)

        if link_result.get("status") != "success":
            return jsonify(link_result), 401

        link_data = link_result.get("data", {})

        ####################################################
        # VERIFY CANDIDATE
        ####################################################

        if int(link_data["candidate_id"]) != int(candidate_id):
            return jsonify(
                {
                    "status": "error",
                    "message": "Secure token does not belong to this candidate.",
                }
            ), 403

        ####################################################
        # VERIFY BGV
        ####################################################

        if str(link_data["bgv_id"]) != str(bgv_id):
            return jsonify(
                {
                    "status": "error",
                    "message": "Secure token does not belong to this BGV request.",
                }
            ), 403

        ####################################################
        # CALL CONSENT SERVICE
        ####################################################

        result = ConsentService.save_candidate_consent(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            verification_type=verification_type,
            consent_status=consent_status,
            consent_text=consent_text,
            consent_version=consent_version,
            consent_source=consent_source,
        )

        return jsonify(result), 200

    except Exception as error:
        print("SAVE CANDIDATE CONSENT ERROR:", error)

        return jsonify({"status": "error", "message": str(error)}), 500
