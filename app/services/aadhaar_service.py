import os
import time
import requests

from app.repositories.verification_repository import VerificationRepository
from app.repositories.api_log_repository import APILogRepository


class AadhaarService:

    @staticmethod
    def verify(data):

        aadhaar_number = data.get("aadhaar_number")
        bgv_id = data.get("bgv_id")
        verification_type_id = data.get("verification_type_id")

        if not aadhaar_number:
            return {
                "status": "error",
                "message": "aadhaar_number is required"
            }

        surepass_url = os.getenv("SUREPASS_BASE_URL")
        surepass_api_key = os.getenv("SUREPASS_API_KEY")

        endpoint = f"{surepass_url}/aadhaar-v2/generate-otp"

        headers = {
            "Authorization": f"Bearer {surepass_api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "id_number": aadhaar_number
        }

        try:

            start_time = time.time()

            response = requests.post(
                endpoint,
                json=payload,
                headers=headers,
                timeout=30
            )

            response_time_ms = int(
                (time.time() - start_time) * 1000
            )

            result = response.json()

            # =====================================
            # API LOGGING
            # =====================================

            APILogRepository.create_api_log(
                module_name="AADHAAR_VERIFICATION",
                provider_name="SUREPASS",
                endpoint=endpoint,
                request_payload=payload,
                response_payload=result,
                response_status_code=response.status_code,
                response_time_ms=response_time_ms,
                status="SUCCESS" if response.status_code == 200 else "FAILED",
                error_message=result.get("message")
            )

            # =====================================
            # SUCCESS FLOW
            # =====================================

            if result.get("success") is True:

                verification_result_id = (
                    VerificationRepository.create_verification_result(
                        bgv_id=bgv_id,
                        verification_type_id=verification_type_id,
                        status="OTP_SENT",
                        remarks="Aadhaar OTP sent successfully",
                        module_score=95
                    )
                )

                return {
                    "status": "success",
                    "module": "Aadhaar",
                    "verification_status": "OTP_SENT",
                    "verification_result_id": verification_result_id,
                    "surepass_response": result
                }

            # =====================================
            # FAILURE FLOW
            # =====================================

            else:

                verification_result_id = (
                    VerificationRepository.create_verification_result(
                        bgv_id=bgv_id,
                        verification_type_id=verification_type_id,
                        status="FAILED",
                        remarks=result.get("message"),
                        module_score=0
                    )
                )

                return {
                    "status": "error",
                    "module": "Aadhaar",
                    "verification_status": "FAILED",
                    "verification_result_id": verification_result_id,
                    "surepass_response": result
                }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }