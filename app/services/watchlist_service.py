from unittest import result

from app.repositories.candidate_repository import CandidateRepository
from app.services.ai_service_connector import AIServiceConnector
from app.services.notification_service import NotificationService


class WatchlistService:
    @staticmethod
    def screen_candidate(candidate_id):

        candidate = CandidateRepository.get_candidate_by_id(candidate_id)

        if not candidate:
            return {"success": False, "message": "Candidate not found"}
        print("CANDIDATE OBJECT")
        print(candidate)

        print("FULL NAME TYPE")
        print(type(candidate["full_name"]))
        dob = None

        if candidate.get("dob"):
            dob = candidate["dob"].strftime("%d/%m/%Y")

        result = AIServiceConnector.screen_watchlist(
            candidate_id=candidate["id"],
            full_name=candidate["full_name"],
            dob=dob,
            gender=candidate.get("gender"),
        )

        if result.get("match_found"):
            NotificationService.create_notification(
                candidate_id=candidate["id"],
                title="Watchlist Match Found",
                description="Candidate matched one or more watchlists.",
                notification_type="Critical",
            )

        else:
            NotificationService.create_notification(
                candidate_id=candidate["id"],
                title="Watchlist Screening Completed",
                description="Candidate cleared Watchlist screening.",
                notification_type="Success",
            )

        return result

    @staticmethod
    def get_candidate_result(candidate_id):

        from app.repositories.watchlist_repository import WatchlistRepository

        return WatchlistRepository.get_by_candidate_id(candidate_id)
