from app.services.ai_service_connector import AIServiceConnector
from app.repositories.candidate_repository import CandidateRepository


class EmploymentService:
    @staticmethod
    def verify_employment(candidate_id, bgv_id, token):
        candidate = CandidateRepository.get_candidate_by_id(candidate_id)

        if not candidate:
            raise Exception("Candidate not found.")

        mobile_number = CandidateRepository.get_candidate_mobile(candidate_id)

        if not mobile_number:
            raise Exception("Candidate mobile number not found.")

        return AIServiceConnector.verify_employment(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            mobile_number=mobile_number,
            token=token,
        )

    @staticmethod
    def get_result(candidate_id, token):
        return AIServiceConnector.get_employment_result(
            candidate_id=candidate_id, token=token
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
                "message": "Invalid Employment decision",
            }

        # =====================================
        # GET EXISTING SUMMARY
        # =====================================

        summary = CandidateVerificationSummaryRepository.get_by_candidate_id(
            candidate_id
        )

        old_decision = None

        if summary:
            old_decision = summary.get("employment_status")

        # =====================================
        # UPDATE EMPLOYMENT DECISION
        # =====================================

        result = CandidateVerificationSummaryService.update_module_status(
            candidate_id=candidate_id,
            module_name="Employment",
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
                title="Employment Verified",
                description=(
                    "Employment verification has been verified by the reviewer."
                ),
                notification_type="Success",
            )

        elif decision == "Not Verified":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Employment Not Verified",
                description=(
                    "Employment verification has been marked as not verified by the reviewer."
                ),
                notification_type="Warning",
            )

        elif decision == "Fraud":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Employment Fraud Detected",
                description=(
                    "Employment verification has been marked as fraudulent by the reviewer."
                ),
                notification_type="Critical",
            )

        elif decision == "Rejected":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Employment Rejected",
                description=(
                    "Employment verification has been rejected by the reviewer."
                ),
                notification_type="Warning",
            )

        # =====================================
        # AUDIT LOG
        # =====================================

        AuditService.log_action(
            action="EMPLOYMENT_DECISION",
            module_name="Employment",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks=f"Employment decision updated to {decision}",
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
            "message": "Employment decision saved",
        }
