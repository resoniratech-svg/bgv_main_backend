from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils.rbac import role_required
from app.services.watchlist_service import WatchlistService
from app.services.candidate_verification_summary_service import (
    CandidateVerificationSummaryService,
)
from app.repositories.watchlist_repository import WatchlistRepository

global_database_bp = Blueprint("global_database", __name__)


# ==========================
# GLOBAL DATABASE HEALTH
# ==========================
@global_database_bp.route("/health", methods=["GET"])
def global_database_health():

    return jsonify(
        {
            "status": "success",
            "module": "Global Database Verification Module",
            "message": "Global database module working successfully",
        }
    ), 200


# ==========================
# GLOBAL WATCHLIST + AML SCREENING
# ==========================
@global_database_bp.route("/screen/<int:candidate_id>", methods=["POST"])
@jwt_required(optional=True)
def screen_watchlist(candidate_id):

    try:
        result = WatchlistService.screen_candidate(candidate_id)

        if result.get("success"):
            risk_level = result.get("risk_level", "LOW")

            CandidateVerificationSummaryService.update_module_status(
                candidate_id=candidate_id,
                module_name="Watchlist",
                status="PENDING_REVIEW",
                risk_level=risk_level,
            )

        return jsonify(result), 200

    except Exception as e:
        import traceback

        traceback.print_exc()

        print("GLOBAL DATABASE ERROR:")
        print(str(e))

        return jsonify({"success": False, "message": str(e)}), 500


@global_database_bp.route("/decision", methods=["POST"])
@jwt_required(optional=True)
def save_watchlist_decision():

    data = request.get_json()

    candidate_id = data.get("candidate_id")
    decision = data.get("decision")

    watchlist_result = WatchlistService.get_candidate_result(candidate_id)

    risk_level = None

    if watchlist_result:
        risk_level = watchlist_result.get("risk_level")

    from app.repositories.candidate_verification_summary_repository import (
        CandidateVerificationSummaryRepository,
    )

    summary = CandidateVerificationSummaryRepository.get_by_candidate_id(candidate_id)

    old_decision = None

    if summary:
        old_decision = summary.get("watchlist_status")

    result = CandidateVerificationSummaryService.update_module_status(
        candidate_id=candidate_id,
        module_name="Watchlist",
        status=decision,
        risk_level=risk_level,
    )

    from app.services.audit_service import AuditService

    AuditService.log_action(
        action="WATCHLIST_DECISION",
        module_name="WATCHLIST",
        entity_type="candidate",
        entity_id=candidate_id,
        status="SUCCESS",
        remarks=f"Watchlist decision updated to {decision}",
        old_values={
            "decision": old_decision,
        },
        new_values={
            "decision": decision,
        },
    )

    return jsonify(result), 200


@global_database_bp.route("/result/<int:candidate_id>", methods=["GET"])
def get_watchlist_result(candidate_id):

    try:
        result = WatchlistService.get_candidate_result(candidate_id)

        print("WATCHLIST RESULT:")
        print(result)

        if not result:
            return jsonify(
                {"success": False, "message": "No watchlist result found"}
            ), 404

        return jsonify(result), 200

    except Exception as e:
        import traceback

        traceback.print_exc()

        print("WATCHLIST RESULT ERROR:")
        print(str(e))

        return jsonify({"success": False, "message": str(e)}), 500
