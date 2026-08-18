from flask import Blueprint, request, jsonify

from app.services.candidate_link_service import CandidateLinkService
from app.services.aadhaar_service import AadhaarService
from app.repositories.candidate_link_repository import CandidateLinkRepository

from app.services.candidate_verification_summary_service import (
    CandidateVerificationSummaryService,
)
from app.repositories.candidate_repository import CandidateRepository
from app.services.audit_service import AuditService


candidate_link_bp = Blueprint("candidate_link_bp", __name__)


# ==========================================================
# GENERATE SECURE LINK
# ==========================================================


@candidate_link_bp.route("/candidate/generate-link", methods=["POST"])
def generate_secure_link():

    try:
        data = request.get_json()

        result = CandidateLinkService.generate_secure_link(data)

        if result["status"] == "error":
            return jsonify(result), 400

        return jsonify(result), 201

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify(
            {
                "status": "error",
                "message": str(e),
            }
        ), 500


# ==========================================================
# VALIDATE SECURE LINK
# ==========================================================


@candidate_link_bp.route(
    "/candidate/validate-link/<secure_token>",
    methods=["GET"],
)
def validate_secure_link(secure_token):

    try:
        result = CandidateLinkService.validate_secure_link(secure_token)

        if result["status"] == "error":
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify(
            {
                "status": "error",
                "message": str(e),
            }
        ), 500


# ==========================================================
# SAVE AADHAAR RESULT
#
# Gridlines SDK
#      ↓
# CandidatePortal
#      ↓
# This endpoint
#      ↓
# AI Service
#      ↓
# aadhaar_verification_results
#      ↓
# candidate_verification_summary
#      ↓
# audit_logs
# ==========================================================


@candidate_link_bp.route(
    "/candidate/aadhaar/result",
    methods=["POST"],
)
def save_aadhaar_result():

    try:
        data = request.get_json()

        if not data:
            return jsonify(
                {
                    "success": False,
                    "message": "Request body is required",
                }
            ), 400

        secure_token = data.get("secure_token")
        aadhaar_data = data.get("aadhaar_data")

        # ==================================================
        # VALIDATE INPUT
        # ==================================================

        if not secure_token:
            return jsonify(
                {
                    "success": False,
                    "message": "secure_token is required",
                }
            ), 400

        if not aadhaar_data:
            return jsonify(
                {
                    "success": False,
                    "message": "aadhaar_data is required",
                }
            ), 400

        # ==================================================
        # VALIDATE SECURE TOKEN
        # ==================================================

        link_result = CandidateLinkRepository.validate_secure_token(secure_token)

        if link_result["status"] == "error":
            return jsonify(link_result), 400

        # ==================================================
        # GET CANDIDATE + BGV
        # ==================================================

        candidate_id = link_result["data"]["candidate_id"]
        bgv_id = link_result["data"]["bgv_id"]

        print("=" * 80)
        print("AADHAAR RESULT SAVE REQUEST")
        print("CANDIDATE ID:", candidate_id)
        print("BGV ID:", bgv_id)
        print("=" * 80)

        # ==================================================
        # STEP 1
        # SAVE AADHAAR RESULT IN AI SERVICE
        # ==================================================

        result = AadhaarService.save_result(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            aadhaar_data=aadhaar_data,
        )

        print("=" * 80)
        print("AI SERVICE AADHAAR SAVE RESPONSE")
        print(result)
        print("=" * 80)

        # ==================================================
        # CHECK AI SERVICE RESULT
        # ==================================================

        if not result or not result.get("success"):
            print("=" * 80)
            print("AADHAAR RESULT SAVE FAILED")
            print(result)
            print("=" * 80)

            return jsonify(
                {
                    "success": False,
                    "message": (
                        result.get(
                            "message",
                            "Failed to save Aadhaar result",
                        )
                        if result
                        else "Failed to save Aadhaar result"
                    ),
                }
            ), 500

        # ==================================================
        # STEP 3
        # AUDIT LOG
        # ==================================================

        try:
            AuditService.log_action(
                action="AADHAAR_VERIFICATION",
                module_name="Aadhaar",
                entity_type="candidate",
                entity_id=candidate_id,
                status="SUCCESS",
                remarks=(
                    "Aadhaar verification completed successfully through Gridlines."
                ),
                old_values={
                    "verification_status": None,
                },
                new_values={
                    "verification_status": "Verified",
                    "provider": "GRIDLINES",
                    "bgv_id": bgv_id,
                },
            )

            print("=" * 80)
            print("AADHAAR AUDIT LOG CREATED")
            print("=" * 80)

        except Exception as audit_error:
            # Do not fail Aadhaar verification just because
            # audit logging failed.

            print("=" * 80)
            print("AADHAAR AUDIT LOG ERROR")
            print(str(audit_error))
            print("=" * 80)

            import traceback

            traceback.print_exc()

        # ==================================================
        # FINAL RESPONSE
        # ==================================================

        return jsonify(
            {
                "success": True,
                "message": ("Aadhaar verification completed successfully"),
                "candidate_id": candidate_id,
                "bgv_id": bgv_id,
                "verification_status": "Verified",
                "aadhaar_result": result,
                "summary": summary_result,
            }
        ), 200

    except Exception as e:
        import traceback

        traceback.print_exc()

        print("=" * 80)
        print("AADHAAR RESULT SAVE ROUTE FAILED")
        print(str(e))
        print("=" * 80)

        return jsonify(
            {
                "success": False,
                "message": str(e),
            }
        ), 500


# ==========================================================
# GET AADHAAR RESULT THROUGH SECURE TOKEN
#
# Used by candidate portal if required.
# ==========================================================


@candidate_link_bp.route(
    "/candidate/aadhaar/result/<secure_token>",
    methods=["GET"],
)
def aadhaar_result(secure_token):

    try:
        # ==================================================
        # VALIDATE SECURE TOKEN
        # ==================================================

        result = CandidateLinkRepository.validate_secure_token(secure_token)

        if result["status"] == "error":
            return jsonify(result), 400

        # ==================================================
        # GET CANDIDATE ID
        # ==================================================

        candidate_id = result["data"]["candidate_id"]

        # ==================================================
        # FETCH SAVED AADHAAR RESULT
        # ==================================================

        response = AadhaarService.get_result(
            candidate_id=candidate_id,
            token=None,
        )

        return jsonify(response), 200

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify(
            {
                "status": "error",
                "message": str(e),
            }
        ), 500


# ==========================================================
# SAVE BANK STATEMENT DETAILS
# ==========================================================


@candidate_link_bp.route(
    "/candidate/bank-statement/details",
    methods=["POST"],
)
def save_bank_statement_details():

    try:
        data = request.get_json()

        if not data:
            return jsonify(
                {
                    "success": False,
                    "message": "Request body is required",
                }
            ), 400

        secure_token = data.get("secure_token")
        bank_name = data.get("bank_name")
        bank_statement_password = data.get("bank_statement_password")

        if not secure_token:
            return jsonify(
                {
                    "success": False,
                    "message": "secure_token is required",
                }
            ), 400

        if not bank_name or not bank_name.strip():
            return jsonify(
                {
                    "success": False,
                    "message": "bank_name is required",
                }
            ), 400

        if not bank_statement_password or not bank_statement_password.strip():
            return jsonify(
                {
                    "success": False,
                    "message": "bank_statement_password is required",
                }
            ), 400

        # ==================================================
        # VALIDATE SECURE TOKEN
        # ==================================================

        link_result = CandidateLinkRepository.validate_secure_token(secure_token)

        if link_result["status"] == "error":
            return jsonify(link_result), 400

        candidate_id = link_result["data"]["candidate_id"]

        # ==================================================
        # SAVE BANK DETAILS
        # ==================================================

        saved = CandidateRepository.save_bank_statement_details(
            candidate_id=candidate_id,
            bank_name=bank_name.strip(),
            bank_statement_password=bank_statement_password,
        )

        if not saved:
            return jsonify(
                {
                    "success": False,
                    "message": "Candidate not found.",
                }
            ), 404

        return jsonify(
            {
                "success": True,
                "message": "Bank Statement details saved successfully.",
                "candidate_id": candidate_id,
            }
        ), 200

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify(
            {
                "success": False,
                "message": str(e),
            }
        ), 500


# @candidate_link_bp.route("/candidate/aadhaar-consent/<secure_token>", methods=["POST"])
# def aadhaar_consent(secure_token):

#     try:
#         result = CandidateLinkRepository.validate_secure_token(secure_token)

#         if result["status"] == "error":
#             return jsonify(result), 400

#         candidate_id = result["data"]["candidate_id"]

#         bgv_id = result["data"]["bgv_id"]

#         response = AadhaarService.generate_qr(candidate_id, bgv_id, None)

#         return jsonify(response)

#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500


# @candidate_link_bp.route("/candidate/aadhaar-status/<secure_token>", methods=["GET"])
# def aadhaar_status(secure_token):

#     try:
#         result = CandidateLinkRepository.validate_secure_token(secure_token)

#         if result["status"] == "error":
#             return jsonify(result), 400

#         candidate_id = result["data"]["candidate_id"]

#         response = AadhaarService.get_status(candidate_id, None)

#         return jsonify(response)

#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500
