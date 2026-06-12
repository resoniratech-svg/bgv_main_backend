from app.repositories.candidate_repository import CandidateRepository
from app.services.ai_service_connector import AIServiceConnector


class WatchlistService:

    @staticmethod
    def screen_candidate(candidate_id):

        candidate = CandidateRepository.get_candidate_by_id(
            candidate_id
        )

        if not candidate:

            return {
                "success": False,
                "message": "Candidate not found"
            }

        return AIServiceConnector.screen_watchlist(
            candidate_id=candidate["id"],
            full_name=candidate["full_name"],
            country="India"
        )
    
    @staticmethod
    def get_candidate_result(candidate_id):

        from app.repositories.watchlist_repository import (
            WatchlistRepository
        )

        return WatchlistRepository.get_by_candidate_id(
            candidate_id
        )