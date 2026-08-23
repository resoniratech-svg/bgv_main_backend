from app.services.ai_service_connector import AIServiceConnector
from app.services.notification_service import NotificationService


class PanService:
    @staticmethod
    def verify_pan(data, token):

        required_fields = ["candidate_id", "bgv_id", "document_id"]

        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": f"{field} is required"}

        result = AIServiceConnector.verify_pan(
            candidate_id=data.get("candidate_id"),
            bgv_id=data.get("bgv_id"),
            document_id=data.get("document_id"),
            token=token,
        )
        from app.services.candidate_verification_summary_service import (
            CandidateVerificationSummaryService,
        )

        status = "Not Verified"

        if result.get("success"):
            status = "Verified"

        CandidateVerificationSummaryService.update_module_status(
            candidate_id=data.get("candidate_id"), module_name="PAN", status=status
        )

        if result.get("success"):
            NotificationService.create_notification(
                candidate_id=data.get("candidate_id"),
                bgv_id=data.get("bgv_id"),
                title="PAN Verification Successful",
                description="PAN verification completed successfully.",
                notification_type="Success",
            )

        else:
            NotificationService.create_notification(
                candidate_id=data.get("candidate_id"),
                bgv_id=data.get("bgv_id"),
                title="PAN Verification Failed",
                description="PAN verification failed. Manual review required.",
                notification_type="Critical",
            )
        from app.services.audit_service import AuditService

        verification_data = result.get("data", {})

        AuditService.log_action(
            action="PAN_VERIFICATION",
            module_name="PAN",
            entity_type="candidate",
            entity_id=data.get("candidate_id"),
            status="SUCCESS" if result.get("success") else "CRITICAL",
            remarks="PAN verification completed",
            new_values={
                "verification_status": status,
                "provider_name": "GRIDLINES",
                "pan_number": verification_data.get("pan_number"),
                "name": verification_data.get("name"),
                "father_name": verification_data.get("father_name"),
                "date_of_birth": verification_data.get("date_of_birth"),
                "name_match_status": verification_data.get("name_match_status"),
                "dob_match_status": verification_data.get("dob_match_status"),
                "verification_result": verification_data.get("verification_status"),
            },
        )
        return {
            "status": "success",
            "message": "PAN verification completed",
            "data": result,
        }

    @staticmethod
    def get_result(candidate_id, token):

        return AIServiceConnector.get_pan_result(candidate_id, token)

    @staticmethod
    def save_decision(data):

        from app.repositories.candidate_verification_summary_repository import (
            CandidateVerificationSummaryRepository,
        )

        from app.services.candidate_verification_summary_service import (
            CandidateVerificationSummaryService,
        )

        from app.services.audit_service import AuditService

        candidate_id = data.get("candidate_id")
        decision = data.get("decision")

        summary = CandidateVerificationSummaryRepository.get_by_candidate_id(
            candidate_id
        )

        old_decision = None

        if summary:
            old_decision = summary.get("pan_status")

        CandidateVerificationSummaryService.update_module_status(
            candidate_id=candidate_id,
            module_name="PAN",
            status=decision,
        )

        if decision == "Approved":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="PAN Approved",
                description="PAN verification has been approved by the reviewer.",
                notification_type="Success",
            )

        elif decision == "Rejected":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="PAN Rejected",
                description="PAN verification has been rejected by the reviewer.",
                notification_type="Warning",
            )

        elif decision == "Reverification Requested":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="PAN Reverification Requested",
                description="PAN verification requires reverification.",
                notification_type="Info",
            )
        AuditService.log_action(
            action="PAN_DECISION",
            module_name="PAN",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks=f"PAN decision updated to {decision}",
            old_values={
                "decision": old_decision,
            },
            new_values={
                "decision": decision,
            },
        )

        return {"status": "success", "message": "PAN decision saved"}
