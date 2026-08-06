from app.repositories.document_repository import DocumentRepository
from app.services.ai_service_connector import AIServiceConnector
from app.services.notification_service import NotificationService


class DeepfakeService:
    @staticmethod
    def verify(candidate_id, bgv_id, token):

        docs = DocumentRepository.get_candidate_documents(candidate_id)

        selfie = None

        for doc in docs:
            if doc.get("document_type") == "Selfie":
                selfie = doc

                break

        if not selfie:
            return {"success": False, "message": "Selfie not found"}

        result = AIServiceConnector.verify_deepfake(
            candidate_id, bgv_id, selfie["id"], token
        )

        from app.services.candidate_verification_summary_service import (
            CandidateVerificationSummaryService,
        )

        status = "Not Verified"

        if result.get("success"):
            status = "Verified"

        CandidateVerificationSummaryService.update_module_status(
            candidate_id=candidate_id,
            module_name="Deepfake Detection",
            status=status,
        )

        if result.get("success"):
            NotificationService.create_notification(
                candidate_id=candidate_id,
                bgv_id=bgv_id,
                title="Deepfake Verification Successful",
                description="Selfie passed the deepfake detection successfully.",
                notification_type="Success",
            )

        else:
            NotificationService.create_notification(
                candidate_id=candidate_id,
                bgv_id=bgv_id,
                title="Deepfake Verification Failed",
                description="Deepfake detection failed. Manual investigation required.",
                notification_type="Critical",
            )
        from app.services.audit_service import AuditService

        AuditService.log_action(
            action="DEEPFAKE_VERIFICATION",
            module_name="DEEPFAKE",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS" if result.get("success") else "CRITICAL",
            remarks="Deepfake verification completed",
            new_values={
                "verification_status": result.get("verification_status"),
                "provider_name": result.get("provider_name"),
                "confidence_score": result.get("confidence_score"),
                "fake_probability": result.get("fake_probability"),
            },
        )

        return result

    @staticmethod
    def get_result(candidate_id, token):

        return AIServiceConnector.get_deepfake_result(candidate_id, token)

    @staticmethod
    def save_decision(data):

        from app.repositories.candidate_verification_summary_repository import (
            CandidateVerificationSummaryRepository,
        )

        from app.services.candidate_verification_summary_service import (
            CandidateVerificationSummaryService,
        )

        from app.services.audit_service import AuditService

        candidate_id = data["candidate_id"]
        decision = data["decision"]

        summary = CandidateVerificationSummaryRepository.get_by_candidate_id(
            candidate_id
        )

        old_decision = None

        if summary:
            old_decision = summary.get("deepfake_status")

        CandidateVerificationSummaryService.update_module_status(
            candidate_id=candidate_id,
            module_name="Deepfake Detection",
            status=decision,
        )

        if decision == "Approved":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Deepfake Approved",
                description="Deepfake verification has been approved.",
                notification_type="Success",
            )

        elif decision == "Rejected":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Deepfake Rejected",
                description="Deepfake verification has been rejected.",
                notification_type="Warning",
            )

        elif decision == "Reverification Requested":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Deepfake Reverification Requested",
                description="Deepfake verification requires reverification.",
                notification_type="Info",
            )
        AuditService.log_action(
            action="DEEPFAKE_DECISION",
            module_name="DEEPFAKE DETECTION",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks=f"Deepfake decision updated to {decision}",
            old_values={
                "decision": old_decision,
            },
            new_values={
                "decision": decision,
            },
        )

        return {"success": True}
