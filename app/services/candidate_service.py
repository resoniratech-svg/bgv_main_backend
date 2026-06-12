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

        return CandidateRepository.get_all_candidates()

    @staticmethod
    def get_candidate_by_id(candidate_id):

        return CandidateRepository.get_candidate_by_id(
            candidate_id
        )

    @staticmethod
    def update_candidate_status(candidate_id, data):

        return CandidateRepository.update_candidate_status(
            candidate_id,
            data
        )

    @staticmethod
    def update_candidate(candidate_id, data):

        result = CandidateRepository.update_candidate(
            candidate_id,
            data
        )

        return {
            "status": "success",
            "message": "Candidate updated successfully",
            "data": result
        }

    @staticmethod
    def delete_candidate(candidate_id):

        return CandidateRepository.delete_candidate(
            candidate_id
        )