from app.repositories.candidate_link_repository import (
    CandidateLinkRepository
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

        return result