from app.repositories.candidate_link_repository import (
    CandidateLinkRepository
)
from app.repositories.candidate_repository import (
    CandidateRepository
)

from app.services.email_service import (
    EmailService
)

class CandidateLinkService:

    @staticmethod
    def generate_secure_link(data):

        required_fields = [
            "candidate_id",
            "bgv_id"
        ]

        for field in required_fields:

            if not data.get(field):

                return {
                    "status": "error",
                    "message": f"{field} is required"
                }

        result = (
        CandidateLinkRepository.create_secure_link(data)
    )

        candidate = (
            CandidateRepository.get_candidate_by_id(
                data["candidate_id"]
            )
        )

        EmailService.send_verification_email(
            candidate_email=candidate["email"],
            candidate_name=candidate["full_name"],
            upload_url=result["upload_url"]
        )

        CandidateRepository.update_candidate_status(
            data["candidate_id"],
            {
                "status": "REQUEST_SENT"
            }
        )

        return {
            "status": "success",
            "message": "Secure upload link generated successfully",
            "data": result
        }

    @staticmethod
    def validate_secure_link(secure_token):

        if not secure_token:

            return {
                "status": "error",
                "message": "Secure token is required"
            }

        result = (
            CandidateLinkRepository.validate_secure_token(
                secure_token
            )
        )

        if result["status"] == "error":

            return result

        candidate = (
    CandidateRepository.get_candidate_by_id(
        result["data"]["candidate_id"]
            )
        )

        print(
            "CANDIDATE STATUS:",
            candidate["status"]
        )

        if candidate["status"] in [
            "DOCUMENTS_UPLOADED",
            "DOCUMENTS_SUBMITTED"
        ]:

            return {
                "status": "already_uploaded",
                "message":
                "You have already uploaded your documents"
            }

        return result