from app.services.ai_service_connector import AIServiceConnector


class DrivingLicenseService:
    # ======================================================
    # VERIFY DRIVING LICENSE
    # ======================================================

    @staticmethod
    def verify_driving_license(
        candidate_id,
        bgv_id,
        front_document_id,
        back_document_id,
        token,
    ):

        return AIServiceConnector.verify_driving_license(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            front_document_id=front_document_id,
            back_document_id=back_document_id,
            token=token,
        )

    # ======================================================
    # GET DRIVING LICENSE RESULT
    # ======================================================

    @staticmethod
    def get_result(candidate_id, token):

        return AIServiceConnector.get_driving_license_result(
            candidate_id,
            token,
        )

    # ======================================================
    # SAVE DRIVING LICENSE DECISION
    # ======================================================

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

        # ==================================================
        # REQUEST DATA
        # ==================================================

        if not data:
            return {
                "status": "error",
                "message": "Request body is required",
            }

        candidate_id = data.get("candidate_id")
        decision = data.get("decision")

        # ==================================================
        # VALIDATE CANDIDATE
        # ==================================================

        if not candidate_id:
            return {
                "status": "error",
                "message": "candidate_id is required",
            }

        # ==================================================
        # VALIDATE DECISION
        # ==================================================

        if not decision:
            return {
                "status": "error",
                "message": "decision is required",
            }

        # ==================================================
        # ALLOWED DECISIONS
        # ==================================================

        allowed_decisions = [
            "Verified",
            "Not Verified",
            "Fraud",
            "Rejected",
        ]

        if decision not in allowed_decisions:
            return {
                "status": "error",
                "message": "Invalid Driving License decision",
            }

        # ==================================================
        # GET CURRENT SUMMARY
        # ==================================================

        summary = CandidateVerificationSummaryRepository.get_by_candidate_id(
            candidate_id
        )

        old_decision = None

        if summary:
            old_decision = summary.get("dl_status")

        # ==================================================
        # UPDATE DRIVING LICENSE DECISION
        # ==================================================

        result = CandidateVerificationSummaryService.update_module_status(
            candidate_id=candidate_id,
            module_name="Driving License",
            status=decision,
        )

        if not result.get("success", True):
            return result

        # ==================================================
        # NOTIFICATION
        # ==================================================

        if decision == "Verified":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Driving License Verified",
                description=(
                    "Driving License verification has been verified by the reviewer."
                ),
                notification_type="Success",
            )

        elif decision == "Not Verified":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Driving License Not Verified",
                description=(
                    "Driving License verification has been marked "
                    "as not verified by the reviewer."
                ),
                notification_type="Warning",
            )

        elif decision == "Fraud":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Driving License Fraud Detected",
                description=(
                    "Driving License verification has been marked "
                    "as fraudulent by the reviewer."
                ),
                notification_type="Critical",
            )

        elif decision == "Rejected":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Driving License Rejected",
                description=(
                    "Driving License verification has been rejected by the reviewer."
                ),
                notification_type="Warning",
            )

        # ==================================================
        # AUDIT LOG
        # ==================================================

        AuditService.log_action(
            action="DRIVING_LICENSE_DECISION",
            module_name="Driving License",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks=(f"Driving License decision updated to {decision}"),
            old_values={
                "decision": old_decision,
            },
            new_values={
                "decision": decision,
            },
        )

        # ==================================================
        # RESPONSE
        # ==================================================

        return {
            "status": "success",
            "message": "Driving License decision saved",
        }
