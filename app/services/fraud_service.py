from app.repositories.candidate_verification_summary_repository import (
    CandidateVerificationSummaryRepository,
)
from app.services.notification_service import NotificationService


class FraudService:
    @staticmethod
    def get_fraud_cases():

        return CandidateVerificationSummaryRepository.get_fraud_cases()

    @staticmethod
    def get_case(candidate_id):

        return CandidateVerificationSummaryRepository.get_case(candidate_id)

    @staticmethod
    @staticmethod
    def approve_case(candidate_id, module):

        result = CandidateVerificationSummaryRepository.approve_case(
            candidate_id,
            module,
        )

        from app.services.audit_service import AuditService

        AuditService.log_action(
            action="FRAUD_APPROVE",
            module_name="FRAUD",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks=f"Fraud case approved for {module}",
            old_values={"decision": "Pending Review"},
            new_values={"decision": "Approved"},
        )
        from app.services.notification_service import NotificationService

        NotificationService.create_notification(
            candidate_id=candidate_id,
            title="Fraud Case Approved",
            description=f"{module} fraud case approved.",
            notification_type="Success",
        )

        return result

    @staticmethod
    def reject_case(candidate_id, module):

        result = CandidateVerificationSummaryRepository.reject_case(
            candidate_id,
            module,
        )

        from app.services.audit_service import AuditService

        AuditService.log_action(
            action="FRAUD_REJECT",
            module_name="FRAUD",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks=f"Fraud case rejected for {module}",
            old_values={"decision": "Pending Review"},
            new_values={"decision": "Rejected"},
        )
        NotificationService.create_notification(
            candidate_id=candidate_id,
            title="Critical Fraud Alert",
            description=f"{module} verification rejected.",
            notification_type="Critical",
        )
        return result

    @staticmethod
    def request_reverification(candidate_id, module):

        result = CandidateVerificationSummaryRepository.request_reverification(
            candidate_id,
            module,
        )

        from app.services.audit_service import AuditService

        AuditService.log_action(
            action="FRAUD_REVERIFY",
            module_name="FRAUD",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks=f"Reverification requested for {module}",
            old_values={"decision": "Pending Review"},
            new_values={"decision": "Reverification Requested"},
        )
        NotificationService.create_notification(
            candidate_id=candidate_id,
            title="Reverification Requested",
            description=f"{module} requires reverification.",
            notification_type="Warning",
        )
        return result
