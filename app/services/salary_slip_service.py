from app.services.ai_service_connector import (
    AIServiceConnector
)


class SalarySlipService:

    ####################################################
    # SALARY SLIP OCR
    ####################################################

    @staticmethod
    def verify_salary_slip(

            candidate_id,
            bgv_id,
            document_id,
            token

    ):

        ####################################################
        # VALIDATIONS
        ####################################################

        if not candidate_id:

            raise Exception(

                "Candidate ID is required."

            )

        if not bgv_id:

            raise Exception(

                "BGV ID is required."

            )

        if not document_id:

            raise Exception(

                "Document ID is required."

            )

        ####################################################
        # AI SERVICE
        ####################################################

        print("=" * 80)
        print("SALARY SLIP OCR")
        print("Candidate ID :", candidate_id)
        print("BGV ID       :", bgv_id)
        print("Document ID  :", document_id)
        print("=" * 80)

        return (

            AIServiceConnector
            .verify_salary_slip(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                document_id=document_id,

                token=token

            )

        )

    ####################################################
    # GET OCR RESULT
    ####################################################

    @staticmethod
    def get_result(

            candidate_id,
            token

    ):

        if not candidate_id:

            raise Exception(

                "Candidate ID is required."

            )

        return (

            AIServiceConnector
            .get_salary_slip_result(

                candidate_id,

                token

            )

        )