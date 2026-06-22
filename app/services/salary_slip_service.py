from app.repositories.document_repository import (
    DocumentRepository
)

from app.services.ai_service_connector import (
    AIServiceConnector
)

from app.services.candidate_verification_summary_service import (
    CandidateVerificationSummaryService
)


class SalarySlipService:

    @staticmethod
    def verify_candidate_salary_slip(
        candidate_id
    ):

        documents = (
            DocumentRepository
            .get_candidate_documents(
                candidate_id
            )
        )
        salary_slip = None

        for document in documents:

            if (
                document.get(
                    "document_type"
                ) == "Salary Slip"
            ):

                salary_slip = document

                break

        if not salary_slip:

            return {

                "success": False,

                "message":
                "Salary Slip document not found"
            }

        print(
            "SALARY SLIP DOCUMENT:",
            salary_slip
        )

        result = (
            AIServiceConnector
            .verify_salary_slip(

                file_path=
                salary_slip[
                    "file_path"
                ],

                candidate_id=
                candidate_id
            )
        )

        print(
            "SALARY SLIP RESULT:",
            result
        )

        # ====================================
        # UPDATE VERIFICATION SUMMARY
        # ====================================

        if result.get("success"):
            print(
                "RESULT TYPE:",
                type(result)
            )

            print(
                "RESULT DATA:",
                result
            )
            salary_data = result.get(
                "data",
                {}
            )

            fraud_score = float(
                salary_data.get(
                    "fraud_score",
                    0
                )
            )

            if fraud_score >= 0.70:

                risk_level = "HIGH"

            elif fraud_score >= 0.40:

                risk_level = "MEDIUM"

            else:

                risk_level = "LOW"

            try:

                print(
                    "UPDATING SALARY SLIP SUMMARY"
                )

                CandidateVerificationSummaryService.update_module_status(
                    candidate_id=candidate_id,
                    module_name="Salary Slip",
                    status="PENDING_REVIEW",
                    risk_level=risk_level
                )

                print(
                    "SUMMARY UPDATED SUCCESSFULLY"
                )

            except Exception as e:

                print(
                    "SUMMARY UPDATE ERROR:",
                    str(e)
                )

                raise

        return result