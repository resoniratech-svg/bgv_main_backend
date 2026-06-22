from app.services.ai_service_connector import (
    AIServiceConnector
)


class DrivingLicenseService:

    @staticmethod
    def verify_driving_license(

        candidate_id,
        bgv_id,
        front_document_id,
        back_document_id,
        token

    ):

        return (

            AIServiceConnector
            .verify_driving_license(

                candidate_id=
                candidate_id,

                bgv_id=
                bgv_id,

                front_document_id=
                front_document_id,

                back_document_id=
                back_document_id,

                token=
                token

            )

        )