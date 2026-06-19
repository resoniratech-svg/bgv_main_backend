from app.services.ai_service_connector import (
    AIServiceConnector
)


class PassportService:

    @staticmethod
    def verify_passport(

        candidate_id,
        bgv_id,
        document_id,
        token

    ):

        return (

            AIServiceConnector
            .verify_passport(

                candidate_id=
                candidate_id,

                bgv_id=
                bgv_id,

                document_id=
                document_id,

                token=
                token

            )

        )