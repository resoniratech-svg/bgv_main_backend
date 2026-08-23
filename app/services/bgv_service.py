from app.repositories.bgv_repository import BGVRepository


class BGVService:
    @staticmethod
    def create_bgv_request(data):

        required_fields = ["candidate_id", "company_name"]

        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": f"{field} is required"}

        result = BGVRepository.create_bgv_request(data)

        return {
            "status": "success",
            "message": "BGV request created successfully",
            "data": result,
        }
