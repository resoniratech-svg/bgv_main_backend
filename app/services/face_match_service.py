from unittest import result

from app.services.ai_service_connector import AIServiceConnector
from app.services.notification_service import NotificationService


class FaceMatchService:
    @staticmethod
    def verify_face(data, token):

        required_fields = [
            "candidate_id",
            "bgv_id",
            "document_id",
        ]

        for field in required_fields:
            if not data.get(field):
                return {
                    "status": "error",
                    "message": f"{field} is required",
                }

        result = AIServiceConnector.verify_face_match(
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
            candidate_id=data.get("candidate_id"),
            module_name="Face Match",
            status=status,
        )

        from app.services.audit_service import AuditService

        verification_data = result.get("data", {})

        AuditService.log_action(
            action="FACE_MATCH_VERIFICATION",
            module_name="Face Match",
            entity_type="candidate",
            entity_id=data.get("candidate_id"),
            status="SUCCESS" if result.get("success") else "CRITICAL",
            remarks="Face Match verification completed",
            new_values={
                "verification_status": status,
                "provider_name": "GRIDLINES",
                "confidence_score": verification_data.get("confidence_score"),
                "verification_result": verification_data.get("verification_status"),
            },
        )
        NotificationService.create_notification(
            candidate_id=data.get("candidate_id"),
            bgv_id=data.get("bgv_id"),
            title="Face Match Verification Completed",
            description=(
                "Face Match verification completed successfully."
                if result.get("success")
                else "Face Match verification failed."
            ),
            notification_type="Success" if result.get("success") else "Critical",
        )
        return {
            "status": "success",
            "message": "Face Match verification completed",
            "data": result,
        }

    @staticmethod
    def get_result(candidate_id, token):

        return AIServiceConnector.get_face_match_result(
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

        candidate_id = data.get("candidate_id")

        decision = data.get("decision")
        print("\n========== FACE MATCH DECISION ==========")
        print("Candidate ID:", candidate_id)
        print("Decision:", decision)
        print("=========================================\n")
        summary = CandidateVerificationSummaryRepository.get_by_candidate_id(
            candidate_id
        )

        old_decision = None

        if summary:
            old_decision = summary.get("face_match_status")

        CandidateVerificationSummaryService.update_module_status(
            candidate_id=candidate_id,
            module_name="Face Match",
            status=decision,
        )
        print("update_module_status() completed")
        AuditService.log_action(
            action="FACE_MATCH_DECISION",
            module_name="Face Match",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks=f"Face Match decision updated to {decision}",
            old_values={
                "decision": old_decision,
            },
            new_values={
                "decision": decision,
            },
        )
        NotificationService.create_notification(
            candidate_id=candidate_id,
            title="Face Match Decision Updated",
            description=f"Face Match verification marked as '{decision}'.",
            notification_type="Success",
        )
        return {
            "status": "success",
            "message": "Face Match decision saved",
        }
