from app.services.ai_service_connector import AIServiceConnector


class PassportService:
    @staticmethod
    def verify_passport(
        candidate_id,
        bgv_id,
        front_document_id,
        back_document_id,
        token,
    ):

        return AIServiceConnector.verify_passport(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            front_document_id=front_document_id,
            back_document_id=back_document_id,
            token=token,
        )

    @staticmethod
    def get_result(candidate_id, token):

        return AIServiceConnector.get_passport_result(
            candidate_id,
            token,
        )

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

        candidate_id = data.get("candidate_id")
        decision = data.get("decision")

        if not candidate_id:
            return {
                "status": "error",
                "message": "candidate_id is required",
            }

        if not decision:
            return {
                "status": "error",
                "message": "decision is required",
            }

        allowed_decisions = [
            "Verified",
            "Not Verified",
            "Fraud",
            "Rejected",
        ]

        if decision not in allowed_decisions:
            return {
                "status": "error",
                "message": "Invalid Passport decision",
            }

        summary = CandidateVerificationSummaryRepository.get_by_candidate_id(
            candidate_id
        )

        old_decision = None

        if summary:
            old_decision = summary.get("passport_status")

        # =====================================
        # UPDATE PASSPORT DECISION
        # =====================================

        result = CandidateVerificationSummaryService.update_module_status(
            candidate_id=candidate_id,
            module_name="Passport",
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
                title="Passport Verified",
                description=(
                    "Passport verification has been verified by the reviewer."
                ),
                notification_type="Success",
            )

        elif decision == "Not Verified":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Passport Not Verified",
                description=(
                    "Passport verification has been marked as not verified by the reviewer."
                ),
                notification_type="Warning",
            )

        elif decision == "Fraud":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Passport Fraud Detected",
                description=(
                    "Passport verification has been marked as fraudulent by the reviewer."
                ),
                notification_type="Critical",
            )

        elif decision == "Rejected":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Passport Rejected",
                description=(
                    "Passport verification has been rejected by the reviewer."
                ),
                notification_type="Warning",
            )

        # =====================================
        # AUDIT LOG
        # =====================================

        AuditService.log_action(
            action="PASSPORT_DECISION",
            module_name="Passport",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks=f"Passport decision updated to {decision}",
            old_values={
                "decision": old_decision,
            },
            new_values={
                "decision": decision,
            },
        )

        return {
            "status": "success",
            "message": "Passport decision saved",
        }
