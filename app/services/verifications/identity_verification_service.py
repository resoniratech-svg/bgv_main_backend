from app.services.verifications.surepass_client import SurepassClient


class IdentityVerificationService:

    @staticmethod
    def verify_pan(pan_number):

        try:
            response = SurepassClient.verify_pan(pan_number)

            return {
                "success": True,
                "provider": "Surepass",
                "verification_type": "PAN",
                "data": response
            }

        except Exception as e:
            return {
                "success": False,
                "provider": "Surepass",
                "verification_type": "PAN",
                "error": str(e)
            }

    @staticmethod
    def verify_aadhaar(aadhaar_number):

        try:
            response = SurepassClient.verify_aadhaar(aadhaar_number)

            return {
                "success": True,
                "provider": "Surepass",
                "verification_type": "AADHAAR",
                "data": response
            }

        except Exception as e:
            return {
                "success": False,
                "provider": "Surepass",
                "verification_type": "AADHAAR",
                "error": str(e)
            }