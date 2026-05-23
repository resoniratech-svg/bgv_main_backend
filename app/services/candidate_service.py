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