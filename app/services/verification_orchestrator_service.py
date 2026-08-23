class VerificationOrchestratorService:

    @staticmethod
    def start_verification_process(

        candidate_id,

        bgv_id
    ):

        print(
            f"Starting verification "
            f"for Candidate: {candidate_id}"
        )

        print(
            f"BGV ID: {bgv_id}"
        )

        return {
            "status": "success",
            "message": (
                "Verification process started"
            )
        }