from app.repositories.candidate_repository import (
    CandidateRepository
)
from app.services.verification_orchestrator_service import (
    VerificationOrchestratorService
)
from app.repositories.candidate_link_repository import (
    CandidateLinkRepository
)
from app.services.email_service import (
    EmailService
)
from app.repositories.document_repository import (
    DocumentRepository
)


class SubmissionService:

    @staticmethod
    def submit_documents(
        secure_token,
        remarks=None
    ):

        print("XXXXXXXXXXXXXXXXXXXXXXXX")
        print("NEW SUBMISSION SERVICE EXECUTED")
        print("XXXXXXXXXXXXXXXXXXXXXXXX")

        print("########################")
        print("SUBMISSION SERVICE STARTED")
        print("########################")

        # =====================================
        # VALIDATE TOKEN
        # =====================================

        validation_result = (
            CandidateLinkRepository.validate_secure_token(
                secure_token
            )
        )

        if validation_result["status"] == "error":

            return validation_result

        candidate_data = validation_result["data"]

        # =====================================
        # CHECK DOCUMENTS EXIST
        # =====================================

        try:

            document_count = (
                DocumentRepository.count_candidate_documents(
                    candidate_data["candidate_id"]
                )
            )

            print(
                "DOCUMENT COUNT:",
                document_count
            )

            if document_count == 0:

                return {
                    "status": "error",
                    "message": "No documents uploaded"
                }

        except Exception as e:

            print(
                "DOCUMENT COUNT ERROR:",
                str(e)
            )

            return {
                "status": "error",
                "message": "Failed to validate uploaded documents"
            }

        # =====================================
        # UPDATE STATUS
        # =====================================

        try:

            CandidateRepository.update_candidate_status(

                candidate_data["candidate_id"],

                {
                    "status":
                    "DOCUMENTS_SUBMITTED"
                }
            )

            print(
                "STATUS UPDATED TO DOCUMENTS_SUBMITTED"
            )

        except Exception as e:

            print(
                "STATUS UPDATE ERROR:",
                str(e)
            )

        # =====================================
        # LOAD CANDIDATE
        # =====================================

        try:

            candidate = (
                CandidateRepository.get_candidate_by_id(
                    candidate_data["candidate_id"]
                )
            )

            if not candidate:

                candidate = {
                    "id": "N/A",
                    "full_name": "N/A"
                }

            print(
                "CANDIDATE:",
                candidate
            )

        except Exception as e:

            print(
                "CANDIDATE LOAD ERROR:",
                str(e)
            )

            candidate = {
                "id": "N/A",
                "full_name": "N/A"
            }

        # =====================================
        # SEND ADMIN EMAIL
        # =====================================

        try:

            print(
                "========== EMAIL START =========="
            )

            email_result = (
                EmailService.send_admin_alert(

                    subject=
                    "Candidate Documents Submitted",

                    message=f"""
                    Candidate Name: {candidate.get('full_name', 'N/A')}

                    Candidate ID: {candidate.get('id', 'N/A')}

                    Status: DOCUMENTS_SUBMITTED

                    Documents uploaded successfully.

                    Verification process started.
                    """
                )
            )

            print(
                "EMAIL RESULT:",
                email_result
            )

            print(
                "========== EMAIL END =========="
            )

        except Exception as e:

            print(
                "EMAIL ERROR:",
                str(e)
            )

        # =====================================
        # START VERIFICATION
        # =====================================

        try:

            print(
                "BEFORE VERIFICATION START"
            )

            VerificationOrchestratorService.start_verification_process(

                candidate_id=
                candidate_data["candidate_id"],

                bgv_id=
                candidate_data["bgv_id"]
            )

            print(
                "AFTER VERIFICATION START"
            )

        except Exception as e:

            print(
                "VERIFICATION ERROR:",
                str(e)
            )

        return {

            "status": "success",

            "message":
            "Documents submitted successfully"

        }