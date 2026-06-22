from flask import (
    Blueprint,
    jsonify
)
import traceback
from app.services.salary_slip_service import (
    SalarySlipService
)
from app.services.candidate_verification_summary_service import (
    CandidateVerificationSummaryService
)

from flask import request
salary_slip_bp = Blueprint(
    "salary_slip_bp",
    __name__
)


@salary_slip_bp.route(
    "/salary-slip/<int:candidate_id>/verify",
    methods=["POST"]
)
def verify_salary_slip(
    candidate_id
):

    try:

        result = (
            SalarySlipService
            .verify_candidate_salary_slip(
                candidate_id
            )
        )

        if not result.get(
            "success"
        ):

            return jsonify(
                result
            ), 400

        return jsonify(
            result
        ), 200

    except Exception as e:

        print("\n========== SALARY SLIP ERROR ==========")
        traceback.print_exc()
        print("=======================================\n")

        return jsonify({
            "success": False,
            "message": "Salary slip verification failed",
            "error": str(e)
        }), 500
    
@salary_slip_bp.route(
    "/salary-slip/decision",
    methods=["POST"]
)
def update_salary_slip_decision():

    data = request.json

    candidate_id = data.get(
        "candidate_id"
    )

    decision = data.get(
        "decision"
    )

    result = (
        CandidateVerificationSummaryService
        .update_module_status(
            candidate_id=
            candidate_id,

            module_name=
            "Salary Slip",

            status=
            decision
        )
    )

    return jsonify(result)