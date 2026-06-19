from app.services.ai_service_connector import (
    AIServiceConnector
)


class AadhaarService:

    @staticmethod
    def generate_qr(
        candidate_id,
        bgv_id,
        token
    ):

        return (

            AIServiceConnector
            .generate_aadhaar_qr(

                candidate_id=
                candidate_id,

                bgv_id=
                bgv_id,

                token=
                token

            )

        )

    @staticmethod
    def get_status(
        candidate_id,
        token
    ):

        return (

            AIServiceConnector
            .get_aadhaar_status(

                candidate_id=
                candidate_id,

                token=
                token

            )

        )

    @staticmethod
    def verify_aadhaar(

        candidate_id,
        bgv_id,
        document_id,
        token

    ):

        return (

            AIServiceConnector
            .verify_aadhaar(

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