from flask import Blueprint
from flask import request
from flask import jsonify

from app.repositories.candidate_verification_summary_repository import (
    CandidateVerificationSummaryRepository,
)
from app.services.candidate_verification_summary_service import (
    CandidateVerificationSummaryService,
)
from app.services.audit_service import AuditService

verification_summary_bp = Blueprint("verification_summary", __name__)


# =====================================
# UPDATE MODULE STATUS
# =====================================


@verification_summary_bp.route("/update", methods=["POST"])
def update_verification_summary():

    try:
        data = request.get_json()

        result = CandidateVerificationSummaryService.update_module_status(
            candidate_id=data.get("candidate_id"),
            module_name=data.get("module_name"),
            status=data.get("status"),
            risk_level=data.get("risk_level"),
        )
        # =====================================
        # AUDIT LOG FOR MODULE DECISION
        # =====================================

        AuditService.log_action(
            action=f"{data.get('module_name').upper().replace(' ', '_')}_DECISION",
            module_name=data.get("module_name"),
            entity_type="candidate",
            entity_id=data.get("candidate_id"),
            status="SUCCESS",
            remarks=f"{data.get('module_name')} decision updated to {data.get('status')}",
            new_values={
                "decision": data.get("status"),
                "risk_level": data.get("risk_level"),
            },
        )
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# =====================================
# GET CANDIDATE SUMMARY
# =====================================


@verification_summary_bp.route("/<int:candidate_id>", methods=["GET"])
def get_candidate_summary(candidate_id):

    try:
        result = CandidateVerificationSummaryService.get_candidate_summary(candidate_id)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# =====================================
# GET PENDING CANDIDATES FOR MODULE
# =====================================
@verification_summary_bp.route("/<module_name>/pending", methods=["GET"])
def get_pending_candidates(module_name):

    try:
        result = CandidateVerificationSummaryService.get_pending_candidates(module_name)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# =====================================
# GET MODULE STATISTICS
# =====================================


@verification_summary_bp.route("/<module_name>/stats", methods=["GET"])
def get_module_statistics(module_name):

    try:
        result = CandidateVerificationSummaryService.get_module_statistics(module_name)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

    # =====================================


# GET CANDIDATES BY STATUS
# =====================================


@verification_summary_bp.route("/<module_name>/status/<status>", methods=["GET"])
def get_candidates_by_status(module_name, status):

    try:
        result = CandidateVerificationSummaryService.get_candidates_by_status(
            module_name, status
        )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
