from app.repositories.candidate_repository import (
    CandidateRepository
)
from app.services.verification_orchestrator_service import (
    VerificationOrchestratorService
)
from app.repositories.candidate_link_repository import (
    CandidateLinkRepository
)

from app.repositories.submission_repository import (
    SubmissionRepository
)


class SubmissionService:

    @staticmethod
    def submit_documents(
        secure_token,
        remarks=None
    ):

        validation_result = (
            CandidateLinkRepository.validate_secure_token(
                secure_token
            )
        )

        if validation_result["status"] == "error":

            return validation_result

        candidate_data = validation_result["data"]

        data = {

            "candidate_id": candidate_data["candidate_id"],

            "bgv_id": candidate_data["bgv_id"],

            "access_link_id": candidate_data["id"],

            "remarks": remarks
        }

        result = (
            SubmissionRepository.create_submission(
                data
            )
        )
        CandidateRepository.update_candidate_status(

            candidate_data["candidate_id"],

            {
                "status": "DOCUMENTS_UPLOADED"
            }
        )
        VerificationOrchestratorService.start_verification_process(

            candidate_id=validation_result["data"]["candidate_id"],

            bgv_id=validation_result["data"]["bgv_id"]
        )
        return {

            "status": "success",

            "message": (
                "Documents submitted successfully"
            ),

            "data": {
                "submission_id": (
                    result["submission_id"]
                )
            }
        }