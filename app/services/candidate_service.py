from app.repositories.candidate_repository import CandidateRepository


class CandidateService:

    @staticmethod
    def create_candidate(data):

        required_fields = [
            "first_name",
            "email",
            "phone"
        ]

        for field in required_fields:

            if not data.get(field):

                return {
                    "status": "error",
                    "message": f"{field} is required"
                }

        result = CandidateRepository.create_candidate(data)

        return {
            "status": "success",
            "message": "Candidate created successfully",
            "data": result
        }

    @staticmethod
    def get_all_candidates():
        candidates = CandidateRepository.get_all_candidates()
        # Convert datetime objects to string for JSON serialization and add full_name
        for c in candidates:
            c['full_name'] = f"{c.get('first_name') or ''} {c.get('last_name') or ''}".strip()
            for key, value in c.items():
                if hasattr(value, 'isoformat'):
                    c[key] = value.isoformat()
        return candidates

    @staticmethod
    def get_candidate_by_id(candidate_id: int):
        candidate = CandidateRepository.get_candidate_by_id(candidate_id)
        if candidate:
            for key, value in candidate.items():
                if hasattr(value, 'isoformat'):
                    candidate[key] = value.isoformat()
        return candidate