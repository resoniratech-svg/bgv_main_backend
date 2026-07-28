from app.services.ai_service_connector import (
    AIServiceConnector
)

from app.repositories.candidate_repository import CandidateRepository


class BankStatementService:

    ###############################################################
    # UPLOAD BANK STATEMENT
    ###############################################################

    @staticmethod
    def upload_bank_statement(

            candidate_id,
            bgv_id,
            document_id,
            token

    ):

        candidate = CandidateRepository.get_bank_statement_details(candidate_id)

        if not candidate:
            return {
                "success": False,
                "message": "Candidate not found."
            }

        bank_name = candidate.get("bank_name")
        bank_statement_password = candidate.get("bank_statement_password")

        print("=" * 80)
        print("BANK DETAILS FROM DATABASE")
        print(f"Candidate ID : {candidate_id}")
        print(f"Bank Name    : {bank_name}")
        print(f"Password     : {bank_statement_password}")
        print("=" * 80)

        return AIServiceConnector.upload_bank_statement(

            candidate_id=candidate_id,

            bgv_id=bgv_id,

            document_id=document_id,

            bank_name=bank_name,

            bank_statement_password=bank_statement_password,

            token=token

        )

    ###############################################################
    # GET RESULT
    ###############################################################

    @staticmethod
    def get_result(

            candidate_id,

            token

    ):

        return (

            AIServiceConnector
            .get_bank_statement_result(

                candidate_id=candidate_id,

                token=token

            )

        )