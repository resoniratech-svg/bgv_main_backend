from app.services.ai_service_connector import (
    AIServiceConnector
)


class DeepfakeService:


    @staticmethod
    def verify_deepfake(

            candidate_id,

            bgv_id,

            document_id,

            token

    ):


        response = (

            AIServiceConnector

            .verify_deepfake(

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


        return response



    @staticmethod
    def get_result(

            candidate_id,

            token

    ):



        response = (

            AIServiceConnector

            .get_deepfake_result(

                candidate_id,

                token

            )

        )


        return response

