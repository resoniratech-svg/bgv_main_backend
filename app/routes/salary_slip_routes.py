from flask import Blueprint, jsonify
import traceback
from app.services.salary_slip_service import SalarySlipService
from app.services.candidate_verification_summary_service import (
    CandidateVerificationSummaryService,
)
from app.services.notification_service import NotificationService
from flask import request

salary_slip_bp = Blueprint("salary_slip_bp", __name__)


@salary_slip_bp.route("/salary-slip/<int:candidate_id>/verify", methods=["POST"])
def verify_salary_slip(candidate_id):

    try:
        result = SalarySlipService.verify_candidate_salary_slip(candidate_id)

        if not result.get("success"):
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as e:
        print("\n========== SALARY SLIP ERROR ==========")
        traceback.print_exc()
        print("=======================================\n")

        return jsonify(
            {
                "success": False,
                "message": "Salary slip verification failed",
                "error": str(e),
            }
        ), 500


@salary_slip_bp.route("/salary-slip/decision", methods=["POST"])
def update_salary_slip_decision():

    from app.repositories.candidate_verification_summary_repository import (
        CandidateVerificationSummaryRepository,
    )

    from app.services.audit_service import AuditService

    data = request.json

    candidate_id = data.get("candidate_id")
    decision = data.get("decision")

    summary = CandidateVerificationSummaryRepository.get_by_candidate_id(candidate_id)

    old_decision = None

    if summary:
        old_decision = summary.get("salary_slip_status")

    result = CandidateVerificationSummaryService.update_module_status(
        candidate_id=candidate_id,
        module_name="Salary Slip",
        status=decision,
    )

    AuditService.log_action(
        action="SALARY_SLIP_DECISION",
        module_name="SALARY_SLIP",
        entity_type="candidate",
        entity_id=candidate_id,
        status="SUCCESS",
        remarks=f"Salary Slip decision updated to {decision}",
        old_values={
            "decision": old_decision,
        },
        new_values={
            "decision": decision,
        },
    )
    NotificationService.create_notification(
        candidate_id=candidate_id,
        title="Salary Slip Decision Updated",
        description=f"Salary Slip verification marked as '{decision}'.",
        notification_type="Success",
    )
    return jsonify(result)


@salary_slip_bp.route("/salary-slip/<int:candidate_id>/result", methods=["GET"])
def get_salary_slip_result(candidate_id):

    try:
        result = SalarySlipService.get_salary_slip_result(candidate_id)

        return jsonify(result), 200

    except Exception as e:
        traceback.print_exc()

        print()
        print("SALARY RESULT ERROR")
        print(type(e))
        print(e)
        print()

        return jsonify({"success": False, "message": str(e)}), 500
