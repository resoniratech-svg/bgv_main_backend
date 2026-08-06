from app.repositories.candidate_verification_summary_repository import (
    CandidateVerificationSummaryRepository,
)


class DashboardService:
    @staticmethod
    def get_summary():

        summary = CandidateVerificationSummaryRepository.get_dashboard_summary()

        return {
            "total_candidates": summary["total_candidates"] or 0,
            "verified": summary["verified"] or 0,
            "pending": summary["pending"] or 0,
            "high_risk": summary["high_risk"] or 0,
            "medium_risk": summary["medium_risk"] or 0,
            "low_risk": summary["low_risk"] or 0,
            "completed_today": summary["completed_today"] or 0,
        }

    @staticmethod
    def get_candidate_history(candidate_id):

        return []
