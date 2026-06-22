from app.repositories.candidate_verification_summary_repository import (
    CandidateVerificationSummaryRepository,
)


class FraudService:
    @staticmethod
    def get_fraud_cases():

        return CandidateVerificationSummaryRepository.get_fraud_cases()

    @staticmethod
    def get_case(candidate_id):

        return CandidateVerificationSummaryRepository.get_case(candidate_id)

    @staticmethod
    def approve_case(candidate_id, module):

        return CandidateVerificationSummaryRepository.approve_case(candidate_id, module)

    @staticmethod
    def reject_case(candidate_id, module):

        return CandidateVerificationSummaryRepository.reject_case(candidate_id, module)

    @staticmethod
    def request_reverification(candidate_id, module):

        return CandidateVerificationSummaryRepository.request_reverification(
            candidate_id, module
        )
