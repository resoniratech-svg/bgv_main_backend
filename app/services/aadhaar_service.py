from app.services.ai_service_connector import AIServiceConnector
from app.repositories.candidate_repository import CandidateRepository

class AadhaarService:

    @staticmethod
    def generate_qr(candidate_id, bgv_id, token):
        return AIServiceConnector.generate_aadhaar_qr(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            token=token
        )

    @staticmethod
    def get_status(candidate_id, token):
        return AIServiceConnector.get_aadhaar_status(
            candidate_id=candidate_id,
            token=token
        )
    
    @staticmethod
    def get_result(candidate_id, token):
        return AIServiceConnector.get_aadhaar_result(
            candidate_id=candidate_id,
            token=token
        )

    @staticmethod
    def verify_aadhaar(

        candidate_id,

        bgv_id,

        document_id,

        token

    ):

        result = (

            AIServiceConnector

            .verify_aadhaar(

                candidate_id,

                bgv_id,

                document_id,

                token

            )

        )

        if result.get("success"):

            CandidateRepository.update_candidate_profile(

                candidate_id=candidate_id,

                date_of_birth=result.get("date_of_birth"),

                gender=result.get("gender")

            )

        return result
    