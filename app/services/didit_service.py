from app.providers.didit_client import (
    DiditClient
)

from app.services.api_log_service import (
    APILogService
)


class DiditService:

    @staticmethod
    def create_verification_session(

        workflow_id,

        candidate_id,

        callback_url
    ):

        payload = {

            "workflow_id": workflow_id,

            "vendor_data": str(candidate_id),

            "callback": callback_url
        }

        response = (
            DiditClient.create_session(
                payload
            )
        )

        APILogService.log_api_call(

            provider_name="DIDIT",

            api_endpoint="/v3/session/",

            request_payload=payload,

            response_payload=response,

            status=(
                "SUCCESS"
                if response.get("success")
                else "FAILED"
            ),

            status_code=response.get(
                "status_code"
            ),

            error_message=response.get(
                "message"
            )
        )

        return response