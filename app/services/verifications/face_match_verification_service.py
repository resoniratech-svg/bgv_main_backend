from app.services.ai_service_connector import (

    AIServiceConnector

)



class FaceMatchVerificationService:



    @staticmethod
    def verify(

            candidate_id,

            bgv_id,

            document_id,

            token

    ):



        return (


            AIServiceConnector


            .verify_face_match(


                candidate_id,


                bgv_id,


                document_id,


                token

            )

        )



    @staticmethod
    def get_result(

            candidate_id,

            token

    ):



        return (


            AIServiceConnector


            .get_face_match_result(


                candidate_id,


                token

            )

        )
