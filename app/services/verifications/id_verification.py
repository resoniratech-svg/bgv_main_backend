from app.repositories.bgv_repository import BGVRepository


class BGVService:

    @staticmethod
    def create_bgv_request(data):
        return BGVRepository.create_bgv(data)

    @staticmethod
    def get_all_requests():
        return BGVRepository.get_all()

    @staticmethod
    def get_request_by_id(bgv_id):
        return BGVRepository.get_by_id(bgv_id)