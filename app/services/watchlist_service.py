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
        print("CANDIDATE OBJECT")
        print(candidate)

        print("FULL NAME TYPE")
        print(type(candidate["full_name"]))
        dob = None

        if candidate.get("dob"):
            dob = candidate["dob"].strftime("%d/%m/%Y")

        return AIServiceConnector.screen_watchlist(
            candidate_id=candidate["id"],
            full_name=candidate["full_name"],
            dob=dob,
            gender=candidate.get("gender")
        )

    
    @staticmethod
    def get_candidate_result(candidate_id):

        from app.repositories.watchlist_repository import (
            WatchlistRepository
        )

        return WatchlistRepository.get_by_candidate_id(
            candidate_id
        )