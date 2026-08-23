import os
from app.repositories.document_repository import DocumentRepository
from app.repositories.resume_repository import ResumeRepository
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.candidate_verification_summary_repository import (
    CandidateVerificationSummaryRepository,
)
from app.services.ai_service_connector import AIServiceConnector
from app.services.notification_service import NotificationService


class ResumeService:
    @staticmethod
    def parse_resume(candidate_id):
        resume_document = DocumentRepository.get_resume_document(candidate_id)

        if not resume_document:
            return {"status": "error", "message": "Resume not uploaded"}

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        full_path = os.path.join(project_root, resume_document["file_path"])

        if not os.path.exists(full_path):
            return {"status": "error", "message": "Resume file not found"}

        result = AIServiceConnector.parse_resume(full_path, candidate_id)
        print("\nAI RESPONSE")
        print(result)

        if result.get("success"):
            candidate = CandidateRepository.get_candidate_by_id(candidate_id)
            candidate_name = (
                f"{candidate['first_name']} {candidate.get('last_name', '')}"
            )
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Resume Parsed Successfully",
                description="Resume has been parsed and extracted successfully.",
                notification_type="Success",
            )
            CandidateVerificationSummaryRepository.create_or_update_module_status(
                candidate_id=candidate_id,
                candidate_name=candidate_name,
                email=candidate["email"],
                phone=candidate["phone"],
                column_name="resume_status",
                status="Verified",
                risk_level="LOW",
            )

        return {
            "status": "success",
            "candidate_id": candidate_id,
            "resume_data": result,
        }

    @staticmethod
    def get_parsed_resume(candidate_id):
        result = ResumeRepository.get_parsed_resume(candidate_id)

        if not result:
            return {"status": "error", "message": "No parsed resume found"}

        return {"status": "success", "data": result}

    @staticmethod
    def update_decision(candidate_id, decision):

        candidate = CandidateRepository.get_candidate_by_id(candidate_id)

        candidate_name = f"{candidate['first_name']} {candidate.get('last_name', '')}"

        # Get existing decision before updating
        old_summary = CandidateVerificationSummaryRepository.get_by_candidate_id(
            candidate_id
        )

        old_decision = None

        if old_summary:
            old_decision = old_summary.get("resume_status")

        # Update decision
        CandidateVerificationSummaryRepository.create_or_update_module_status(
            candidate_id=candidate_id,
            candidate_name=candidate_name,
            email=candidate["email"],
            phone=candidate["phone"],
            column_name="resume_status",
            status=decision,
            risk_level="LOW",
        )

        from app.services.audit_service import AuditService

        AuditService.log_action(
            action="RESUME_DECISION",
            module_name="RESUME",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks="Resume decision updated",
            old_values={"decision": old_decision},
            new_values={"decision": decision},
        )
        NotificationService.create_notification(
            candidate_id=candidate_id,
            title="Resume Decision Updated",
            description=f"Resume verification marked as '{decision}'.",
            notification_type="Success",
        )
        return {"status": "success"}
