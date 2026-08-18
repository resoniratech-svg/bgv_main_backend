from app.repositories.candidate_repository import CandidateRepository

from app.repositories.bgv_repository import BGVRepository

from app.services.audit_service import AuditService
import json

from app.services.notification_service import NotificationService


class CandidateService:
    @staticmethod
    def create_candidate(data):

        required_fields = ["first_name", "email", "phone", "country", "company_name"]

        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": f"{field} is required"}

        candidate_result = CandidateRepository.create_candidate(data)
        from app.services.candidate_verification_summary_service import (
            CandidateVerificationSummaryService,
        )

        summary_result = (
            CandidateVerificationSummaryService.initialize_candidate_summary(
                candidate_result["candidate_id"]
            )
        )

        if not summary_result.get("success"):
            return {
                "status": "error",
                "message": "Candidate created but verification summary could not be initialized",
            }
        AuditService.log_action(
            action="CREATE_CANDIDATE",
            module_name="CANDIDATES",
            entity_type="candidate",
            entity_id=(candidate_result["candidate_id"]),
            status="SUCCESS",
            remarks="Candidate created successfully",
        )
        bgv_result = BGVRepository.create_bgv_request(
            {
                "candidate_id": candidate_result["candidate_id"],
                "company_name": data.get("company_name"),
            }
        )

        NotificationService.create_notification(
            candidate_id=candidate_result["candidate_id"],
            bgv_id=bgv_result["bgv_id"],  # VARCHAR is perfectly okay
            title="New Candidate Created",
            description=f"{data.get('first_name')} {data.get('last_name')} has been added successfully.",
            notification_type="Info",
        )

        return {
            "status": "success",
            "message": "Candidate created successfully",
            "data": {"candidate": candidate_result, "bgv": bgv_result},
        }

    @staticmethod
    def get_all_candidates():

        return CandidateRepository.get_all_candidates()

    @staticmethod
    def get_candidate_by_id(candidate_id):

        return CandidateRepository.get_candidate_by_id(candidate_id)

    @staticmethod
    def update_candidate_status(candidate_id, data):

        return CandidateRepository.update_candidate_status(candidate_id, data)

    @staticmethod
    def update_candidate(candidate_id, data):

        old_candidate = CandidateRepository.get_candidate_by_id(candidate_id)

        result = CandidateRepository.update_candidate(candidate_id, data)

        updated_candidate = CandidateRepository.get_candidate_by_id(candidate_id)

        old_candidate = json.loads(json.dumps(old_candidate, default=str))

        updated_candidate = json.loads(json.dumps(updated_candidate, default=str))

        changes = {}

        for key in updated_candidate:
            old = old_candidate.get(key)

            new = updated_candidate.get(key)

            if str(old) != str(new):
                changes[key] = {"old": old, "new": new}
        AuditService.log_action(
            action="UPDATE_CANDIDATE",
            module_name="CANDIDATES",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks="Candidate updated successfully",
            old_values=old_candidate,
            new_values=updated_candidate,
        )
        NotificationService.create_notification(
            candidate_id=candidate_id,
            title="Candidate Updated",
            description="Candidate profile has been updated.",
            notification_type="Info",
        )
        return {
            "status": "success",
            "message": "Candidate updated successfully",
            "data": result,
        }

    @staticmethod
    def delete_candidate(candidate_id):

        deleted_candidate = CandidateRepository.get_candidate_by_id(candidate_id)

        try:
            result = CandidateRepository.delete_candidate(candidate_id)

            AuditService.log_action(
                action="DELETE_CANDIDATE",
                module_name="CANDIDATES",
                entity_type="candidate",
                entity_id=candidate_id,
                status="SUCCESS",
                remarks="Candidate deleted successfully",
                old_values=deleted_candidate,
            )
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Candidate Deleted",
                description="Candidate has been deleted.",
                notification_type="Warning",
            )
            return result

        except Exception as e:
            AuditService.log_action(
                action="DELETE_CANDIDATE",
                module_name="CANDIDATES",
                entity_type="candidate",
                entity_id=candidate_id,
                status="CRITICAL",
                remarks=str(e),
            )

            raise
