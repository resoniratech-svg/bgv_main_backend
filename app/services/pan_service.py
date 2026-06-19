from app.services.ai_service_connector import (
    AIServiceConnector
)


class PanService:

    @staticmethod
    def verify_pan(
        data,
        token
    ):

        required_fields = [

            "candidate_id",

            "bgv_id",

            "document_id"
        ]

        for field in required_fields:

            if not data.get(field):

                return {

                    "status": "error",

                    "message":
                    f"{field} is required"
                }

        result = (
            AIServiceConnector
            .verify_pan(

                candidate_id=data.get(
                    "candidate_id"
                ),

                bgv_id=data.get(
                    "bgv_id"
                ),

                document_id=data.get(
                    "document_id"
                ),

                token=token
            )
        )

        return {

            "status": "success",

            "message":
            "PAN verification completed",

            "data": result
        }