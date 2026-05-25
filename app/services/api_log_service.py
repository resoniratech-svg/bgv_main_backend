from app.repositories.api_log_repository import (
    APILogRepository
)


class APILogService:

    @staticmethod
    def log_api_call(

        provider_name,

        api_endpoint,

        request_payload,

        response_payload,

        status,

        status_code=None,

        error_message=None
    ):

        data = {

            "provider_name": provider_name,

            "api_endpoint": api_endpoint,

            "request_payload": str(
                request_payload
            ),

            "response_payload": str(
                response_payload
            ),

            "status": status,

            "status_code": status_code,

            "error_message": error_message
        }

        return APILogRepository.create_log(data)