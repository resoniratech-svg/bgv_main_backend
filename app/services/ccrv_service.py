from app.services.ai_service_connector import (
    AIServiceConnector
)


class CCRVService:

    # ==========================================
    # VERIFY CCRV
    # ==========================================

    @staticmethod
    def verify_ccrv(

        candidate_id,
        bgv_id,
        token

    ):

        return (

            AIServiceConnector
            .verify_ccrv(

                candidate_id=
                candidate_id,

                bgv_id=
                bgv_id,

                token=
                token

            )

        )

    # ==========================================
    # GET CCRV RESULT
    # ==========================================

    @staticmethod
    def get_result(

        candidate_id,
        token

    ):

        return (

            AIServiceConnector
            .get_ccrv_result(

                candidate_id=
                candidate_id,

                token=
                token

            )

        )