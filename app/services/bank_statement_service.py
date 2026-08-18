from app.services.ai_service_connector import AIServiceConnector

from app.repositories.candidate_repository import CandidateRepository


class BankStatementService:
    ###############################################################
    # SAVE BANK STATEMENT DETAILS
    ###############################################################
    @staticmethod
    def save_bank_statement_details(
        candidate_id,
        bank_name,
        bank_statement_password,
    ):

        if not candidate_id:
            return {
                "success": False,
                "message": "candidate_id is required",
            }

        if not bank_name or not bank_name.strip():
            return {
                "success": False,
                "message": "bank_name is required",
            }

        if not bank_statement_password or not bank_statement_password.strip():
            return {
                "success": False,
                "message": "bank_statement_password is required",
            }

        saved = CandidateRepository.save_bank_statement_details(
            candidate_id=candidate_id,
            bank_name=bank_name.strip(),
            bank_statement_password=bank_statement_password,
        )

        if not saved:
            return {
                "success": False,
                "message": "Candidate not found.",
            }

        return {
            "success": True,
            "message": "Bank Statement details saved successfully.",
        }

    ###############################################################
    # UPLOAD BANK STATEMENT
    ###############################################################

    @staticmethod
    def upload_bank_statement(candidate_id, bgv_id, document_id, token):

        candidate = CandidateRepository.get_bank_statement_details(candidate_id)

        if not candidate:
            return {
                "success": False,
                "message": "Candidate not found.",
            }

        bank_name = candidate.get("bank_name")
        bank_statement_password = candidate.get("bank_statement_password")

        print("=" * 80)
        print("BANK DETAILS FROM DATABASE")
        print(f"Candidate ID : {candidate_id}")
        print(f"Bank Name    : {bank_name}")
        print(f"Password     : {bank_statement_password}")
        print("=" * 80)

        return AIServiceConnector.upload_bank_statement(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            document_id=document_id,
            bank_name=bank_name,
            bank_statement_password=bank_statement_password,
            token=token,
        )

    ###############################################################
    # GET RESULT
    ###############################################################

    @staticmethod
    def get_result(candidate_id, bgv_id, token):

        return AIServiceConnector.get_bank_statement_result(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            token=token,
        )

    ###############################################################
    # SAVE BANK STATEMENT DECISION
    ###############################################################

    @staticmethod
    def save_decision(data):

        from app.repositories.candidate_verification_summary_repository import (
            CandidateVerificationSummaryRepository,
        )

        from app.services.candidate_verification_summary_service import (
            CandidateVerificationSummaryService,
        )

        from app.services.audit_service import AuditService

        from app.services.notification_service import NotificationService

        # =========================================================
        # GET DATA
        # =========================================================

        candidate_id = data.get("candidate_id")
        decision = data.get("decision")

        # =========================================================
        # VALIDATE CANDIDATE ID
        # =========================================================

        if not candidate_id:
            return {
                "status": "error",
                "message": "candidate_id is required",
            }

        # =========================================================
        # VALIDATE DECISION
        # =========================================================

        if not decision:
            return {
                "status": "error",
                "message": "decision is required",
            }

        # =========================================================
        # ALLOWED DECISIONS
        # =========================================================

        allowed_decisions = [
            "Verified",
            "Not Verified",
            "Fraud",
            "Rejected",
        ]

        if decision not in allowed_decisions:
            return {
                "status": "error",
                "message": "Invalid Bank Statement decision",
            }

        # =========================================================
        # GET EXISTING SUMMARY
        # =========================================================

        summary = CandidateVerificationSummaryRepository.get_by_candidate_id(
            candidate_id
        )

        old_decision = None

        if summary:
            old_decision = summary.get("bank_statement_status")

        # =========================================================
        # UPDATE BANK STATEMENT STATUS
        # =========================================================

        result = CandidateVerificationSummaryService.update_module_status(
            candidate_id=candidate_id,
            module_name="Bank Statement",
            status=decision,
        )

        if not result.get("success", True):
            return result

        # =========================================================
        # NOTIFICATION
        # =========================================================

        if decision == "Verified":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Bank Statement Verified",
                description=(
                    "Bank Statement verification has been verified by the reviewer."
                ),
                notification_type="Success",
            )

        elif decision == "Not Verified":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Bank Statement Not Verified",
                description=(
                    "Bank Statement verification has been "
                    "marked as not verified by the reviewer."
                ),
                notification_type="Warning",
            )

        elif decision == "Fraud":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Bank Statement Fraud Detected",
                description=(
                    "Bank Statement verification has been "
                    "marked as fraudulent by the reviewer."
                ),
                notification_type="Critical",
            )

        elif decision == "Rejected":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Bank Statement Rejected",
                description=(
                    "Bank Statement verification has been rejected by the reviewer."
                ),
                notification_type="Warning",
            )

        # =========================================================
        # AUDIT LOG
        # =========================================================

        AuditService.log_action(
            action="BANK_STATEMENT_DECISION",
            module_name="Bank Statement",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks=f"Bank Statement decision updated to {decision}",
            old_values={
                "decision": old_decision,
            },
            new_values={
                "decision": decision,
            },
        )

        # =========================================================
        # RETURN
        # =========================================================

        return {
            "status": "success",
            "message": "Bank Statement decision saved",
        }
