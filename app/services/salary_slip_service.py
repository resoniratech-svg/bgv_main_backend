from app.services.ai_service_connector import AIServiceConnector


class SalarySlipService:
    ####################################################
    # SALARY SLIP OCR
    ####################################################

    @staticmethod
    def verify_salary_slip(candidate_id, bgv_id, document_id, token):

        ####################################################
        # VALIDATIONS
        ####################################################

        if not candidate_id:
            raise Exception("Candidate ID is required.")

        if not bgv_id:
            raise Exception("BGV ID is required.")

        if not document_id:
            raise Exception("Document ID is required.")

        ####################################################
        # AI SERVICE
        ####################################################

        print("=" * 80)
        print("SALARY SLIP OCR")
        print("Candidate ID :", candidate_id)
        print("BGV ID       :", bgv_id)
        print("Document ID  :", document_id)
        print("=" * 80)

        result = AIServiceConnector.verify_salary_slip(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            document_id=document_id,
            token=token,
        )

        ####################################################
        # UPDATE VERIFICATION STATUS
        ####################################################

        if result.get("success"):
            from app.services.candidate_verification_summary_service import (
                CandidateVerificationSummaryService,
            )

            CandidateVerificationSummaryService.update_module_status(
                candidate_id=candidate_id,
                module_name="Salary Slip",
                status="Not Verified",
            )

        return result

    ####################################################
    # GET OCR RESULT
    ####################################################

    @staticmethod
    def get_result(candidate_id, token):

        if not candidate_id:
            raise Exception("Candidate ID is required.")

        return AIServiceConnector.get_salary_slip_result(candidate_id, token)

    ####################################################
    # SAVE SALARY SLIP DECISION
    ####################################################

    @staticmethod
    def save_decision(data):

        from app.repositories.candidate_verification_summary_repository import (
            CandidateVerificationSummaryRepository,
        )

        from app.services.candidate_verification_summary_service import (
            CandidateVerificationSummaryService,
        )

        from app.services.audit_service import AuditService

        ####################################################
        # INPUTS
        ####################################################

        candidate_id = data.get("candidate_id")
        decision = data.get("decision")

        ####################################################
        # VALIDATION
        ####################################################

        if not candidate_id:
            raise Exception("Candidate ID is required.")

        if not decision:
            raise Exception("Decision is required.")

        allowed_decisions = [
            "Verified",
            "Not Verified",
            "Fraud",
            "Rejected",
        ]

        if decision not in allowed_decisions:
            raise Exception(
                "Invalid Salary Slip decision. "
                "Allowed values: Verified, Not Verified, Fraud, Rejected."
            )

        ####################################################
        # GET CURRENT SUMMARY
        ####################################################

        summary = CandidateVerificationSummaryRepository.get_by_candidate_id(
            candidate_id
        )

        old_decision = None

        if summary:
            old_decision = summary.get("salary_slip_status")

        ####################################################
        # UPDATE VERIFICATION SUMMARY
        ####################################################

        result = CandidateVerificationSummaryService.update_module_status(
            candidate_id=candidate_id,
            module_name="Salary Slip",
            status=decision,
        )

        if not result.get("success"):
            raise Exception(
                result.get(
                    "message",
                    "Failed to update Salary Slip status.",
                )
            )

        ####################################################
        # AUDIT LOG
        ####################################################

        AuditService.log_action(
            action="SALARY_SLIP_DECISION",
            module_name="SALARY SLIP",
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

        ####################################################
        # RESPONSE
        ####################################################

        return {
            "success": True,
            "message": "Salary Slip decision updated successfully.",
            "candidate_id": candidate_id,
            "decision": decision,
        }
