from app.services.ai_service_connector import AIServiceConnector


class CCRVService:
    # ==========================================
    # VERIFY CCRV
    # ==========================================

    @staticmethod
    def verify_ccrv(candidate_id, bgv_id, token):

        return AIServiceConnector.verify_ccrv(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            token=token,
        )

    # ==========================================
    # GET CCRV RESULT
    # ==========================================

    @staticmethod
    def get_result(candidate_id, token):

        return AIServiceConnector.get_ccrv_result(
            candidate_id=candidate_id,
            token=token,
        )

    # ==========================================
    # SAVE CCRV DECISION
    # ==========================================

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

        # =====================================
        # GET DATA
        # =====================================

        candidate_id = data.get("candidate_id")
        decision = data.get("decision")

        # =====================================
        # VALIDATE CANDIDATE ID
        # =====================================

        if not candidate_id:
            return {
                "status": "error",
                "message": "candidate_id is required",
            }

        # =====================================
        # VALIDATE DECISION
        # =====================================

        if not decision:
            return {
                "status": "error",
                "message": "decision is required",
            }

        # =====================================
        # ALLOWED DECISIONS
        # =====================================

        allowed_decisions = [
            "Verified",
            "Not Verified",
            "Fraud",
            "Rejected",
        ]

        if decision not in allowed_decisions:
            return {
                "status": "error",
                "message": "Invalid Court Record decision",
            }

        # =====================================
        # GET EXISTING SUMMARY
        # =====================================

        summary = CandidateVerificationSummaryRepository.get_by_candidate_id(
            candidate_id
        )

        old_decision = None

        if summary:
            old_decision = summary.get("court_status")

        # =====================================
        # UPDATE COURT RECORD STATUS
        # =====================================

        result = CandidateVerificationSummaryService.update_module_status(
            candidate_id=candidate_id,
            module_name="Court Record",
            status=decision,
        )

        if not result.get("success", True):
            return result

        # =====================================
        # NOTIFICATION
        # =====================================

        if decision == "Verified":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Court Record Verified",
                description=(
                    "Court and criminal record verification has been "
                    "verified by the reviewer."
                ),
                notification_type="Success",
            )

        elif decision == "Not Verified":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Court Record Not Verified",
                description=(
                    "Court and criminal record verification has been "
                    "marked as not verified by the reviewer."
                ),
                notification_type="Warning",
            )

        elif decision == "Fraud":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Court Record Fraud Detected",
                description=(
                    "Court and criminal record verification has been "
                    "marked as fraudulent by the reviewer."
                ),
                notification_type="Critical",
            )

        elif decision == "Rejected":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Court Record Rejected",
                description=(
                    "Court and criminal record verification has been "
                    "rejected by the reviewer."
                ),
                notification_type="Warning",
            )

        # =====================================
        # AUDIT LOG
        # =====================================

        AuditService.log_action(
            action="COURT_RECORD_DECISION",
            module_name="Court Record",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks=f"Court Record decision updated to {decision}",
            old_values={
                "decision": old_decision,
            },
            new_values={
                "decision": decision,
            },
        )

        # =====================================
        # RETURN
        # =====================================

        return {
            "status": "success",
            "message": "Court Record decision saved",
        }
