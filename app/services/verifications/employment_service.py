from app.services.verifications.base import BaseVerificationService


class EmploymentVerificationService(BaseVerificationService):

    def execute(self, data):
        # Simulated logic
        if data.get("employment_verified"):
            return {
                "verification_type": "Employment",
                "status": "Verified",
                "module_score": 85.50,
                "remarks": "Employment verified successfully"
            }

        return {
            "verification_type": "Employment",
            "status": "Failed",
            "module_score": 20.00,
            "remarks": "Employment verification failed"
        }