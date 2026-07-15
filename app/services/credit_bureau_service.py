from app.repositories.candidate_repository import CandidateRepository
from app.services.ai_service_connector import AIServiceConnector


class CreditBureauService:

    @staticmethod
    def verify_credit_bureau(candidate_id, bgv_id, token):
        print("=" * 80)
        print("INSIDE CreditBureauService")
        print("candidate_id =", candidate_id)
        print("bgv_id =", bgv_id)
        print("=" * 80)

        ####################################################
        # GET CANDIDATE
        ####################################################
        candidate = CandidateRepository.get_candidate_by_id(candidate_id)
        print("Candidate Object:", candidate)

        if not candidate:
            raise Exception("Candidate not found.")

        ####################################################
        # REQUIRED FIELDS
        ####################################################
        first_name = candidate.get("first_name")
        last_name = candidate.get("last_name") or ""
        phone = candidate.get("phone")

        # Moved print statements down so variables are defined before printing
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Phone: {phone}")

        ####################################################
        # VALIDATIONS
        ####################################################
        if not first_name:
            raise Exception("Candidate first name not found.")

        if not phone:
            raise Exception("Candidate phone number not found.")

        ####################################################
        # AI SERVICE
        ####################################################
        print("CALLING AI CONNECTOR")
        return AIServiceConnector.verify_credit_bureau(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            token=token
        )

    ####################################################
    # RESULT
    ####################################################
    @staticmethod
    def get_result(candidate_id, token):
        return AIServiceConnector.get_credit_bureau_result(candidate_id, token)