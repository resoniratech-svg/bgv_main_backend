from app.services.ai_service_connector import AIServiceConnector
from app.repositories.candidate_repository import CandidateRepository


class EmploymentService:

    @staticmethod
    def verify_employment(candidate_id, bgv_id, token):
        candidate = CandidateRepository.get_candidate_by_id(candidate_id)

        if not candidate:
            raise Exception("Candidate not found.")

        mobile_number = CandidateRepository.get_candidate_mobile(
        candidate_id
        )

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
            candidate_id=candidate_id, 
            token=token
        )