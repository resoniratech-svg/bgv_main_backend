from app.repositories.candidate_repository import CandidateRepository
from app.services.ai_service_connector import AIServiceConnector


class CreditBureauService:
    @staticmethod
    def verify_credit_bureau(candidate_id, bgv_id, token):
        print("=" * 80)
        print("INSIDE CreditBureauService")
        print("candidate_id =", candidate_id)
        print("bgv_id =", bgv_id)
        print("=" * 80)

        ####################################################
        # GET CANDIDATE
        ####################################################
        candidate = CandidateRepository.get_candidate_by_id(candidate_id)
        print("Candidate Object:", candidate)

        if not candidate:
            raise Exception("Candidate not found.")

        ####################################################
        # REQUIRED FIELDS
        ####################################################
        first_name = candidate.get("first_name")
        last_name = candidate.get("last_name") or ""
        phone = candidate.get("phone")

        # Moved print statements down so variables are defined before printing
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Phone: {phone}")

        ####################################################
        # VALIDATIONS
        ####################################################
        if not first_name:
            raise Exception("Candidate first name not found.")

        if not phone:
            raise Exception("Candidate phone number not found.")

        ####################################################
        # AI SERVICE
        ####################################################
        print("CALLING AI CONNECTOR")
        return AIServiceConnector.verify_credit_bureau(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            token=token,
        )

    ####################################################
    # RESULT
    ####################################################
    @staticmethod
    def get_result(candidate_id, token):
        return AIServiceConnector.get_credit_bureau_result(candidate_id, token)
        ####################################################

    # SAVE CREDIT BUREAU DECISION
    ####################################################

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
                "message": "Invalid Credit Bureau decision",
            }

        # =====================================
        # GET EXISTING SUMMARY
        # =====================================

        summary = CandidateVerificationSummaryRepository.get_by_candidate_id(
            candidate_id
        )

        old_decision = None

        if summary:
            old_decision = summary.get("credit_status")

        # =====================================
        # UPDATE CREDIT BUREAU DECISION
        # =====================================

        result = CandidateVerificationSummaryService.update_module_status(
            candidate_id=candidate_id,
            module_name="Credit Bureau",
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
                title="Credit Bureau Verified",
                description=(
                    "Credit Bureau verification has been verified by the reviewer."
                ),
                notification_type="Success",
            )

        elif decision == "Not Verified":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Credit Bureau Not Verified",
                description=(
                    "Credit Bureau verification has been marked as not verified "
                    "by the reviewer."
                ),
                notification_type="Warning",
            )

        elif decision == "Fraud":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Credit Bureau Fraud Detected",
                description=(
                    "Credit Bureau verification has been marked as fraudulent "
                    "by the reviewer."
                ),
                notification_type="Critical",
            )

        elif decision == "Rejected":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Credit Bureau Rejected",
                description=(
                    "Credit Bureau verification has been rejected by the reviewer."
                ),
                notification_type="Warning",
            )

        # =====================================
        # AUDIT LOG
        # =====================================

        AuditService.log_action(
            action="CREDIT_BUREAU_DECISION",
            module_name="Credit Bureau",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks=f"Credit Bureau decision updated to {decision}",
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
            "message": "Credit Bureau decision saved",
        }
