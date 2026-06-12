from app.repositories.candidate_verification_summary_repository import (
    CandidateVerificationSummaryRepository
)

class FraudService:

    @staticmethod
    def get_fraud_cases():

        return CandidateVerificationSummaryRepository.get_fraud_cases()