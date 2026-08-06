from app.repositories.document_repository import DocumentRepository

from app.services.ai_service_connector import AIServiceConnector

from app.services.candidate_verification_summary_service import (
    CandidateVerificationSummaryService,
)
from app.services.notification_service import NotificationService


class SalarySlipService:
    @staticmethod
    def verify_candidate_salary_slip(candidate_id):

        documents = DocumentRepository.get_candidate_documents(candidate_id)
        salary_slip = None

        for document in documents:
            if document.get("document_type") == "Salary Slip":
                salary_slip = document

                break

        if not salary_slip:
            return {"success": False, "message": "Salary Slip document not found"}

        print("SALARY SLIP DOCUMENT:", salary_slip)

        result = AIServiceConnector.verify_salary_slip(
            file_path=salary_slip["file_path"], candidate_id=candidate_id
        )

        print("SALARY SLIP RESULT:", result)

        # ====================================
        # UPDATE VERIFICATION SUMMARY
        # ====================================

        if result.get("success"):
            print("RESULT TYPE:", type(result))

            print("RESULT DATA:", result)
            fraud_score = float(result.get("fraud_score", 0))
            if fraud_score >= 0.70:
                risk_level = "HIGH"

            elif fraud_score >= 0.40:
                risk_level = "MEDIUM"

            else:
                risk_level = "LOW"

            try:
                print("UPDATING SALARY SLIP SUMMARY")

                CandidateVerificationSummaryService.update_module_status(
                    candidate_id=candidate_id,
                    module_name="Salary Slip",
                    status="PENDING_REVIEW",
                    risk_level=risk_level,
                )
                from app.services.audit_service import AuditService

                AuditService.log_action(
                    action="SALARY_SLIP_VERIFICATION",
                    module_name="SALARY_SLIP",
                    entity_type="candidate",
                    entity_id=candidate_id,
                    status="SUCCESS" if result.get("success") else "CRITICAL",
                    remarks="Salary Slip verification completed",
                    new_values={
                        "verification_status": "PENDING_REVIEW",
                        "fraud_score": result.get("fraud_score"),
                        "risk_level": risk_level,
                    },
                )
                NotificationService.create_notification(
                    candidate_id=candidate_id,
                    title="Salary Slip Verification Completed",
                    description=f"Salary Slip verification completed. Risk Level: {risk_level}.",
                    notification_type=(
                        "Critical"
                        if risk_level == "HIGH"
                        else "Warning"
                        if risk_level == "MEDIUM"
                        else "Success"
                    ),
                )
                print("SUMMARY UPDATED SUCCESSFULLY")

            except Exception as e:
                print("SUMMARY UPDATE ERROR:", str(e))

                raise

        return result

    @staticmethod
    def get_salary_slip_result(candidate_id):

        return AIServiceConnector.get_salary_slip_result(candidate_id)
