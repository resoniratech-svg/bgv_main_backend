import os
import requests


class SurepassClient:

    BASE_URL = os.getenv("SUREPASS_BASE_URL")
    API_KEY = os.getenv("SUREPASS_API_KEY")

    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    @staticmethod
    def verify_pan(pan_number):

        url = f"{SurepassClient.BASE_URL}/pan/pan"

        payload = {
            "id_number": pan_number
        }

        response = requests.post(
            url,
            headers=SurepassClient.HEADERS,
            json=payload,
            timeout=30
        )

        return response.json()

    @staticmethod
    def verify_aadhaar(aadhaar_number):

        url = f"{SurepassClient.BASE_URL}/aadhaar-v2/generate-otp"

        payload = {
            "id_number": aadhaar_number
        }

        response = requests.post(
            url,
            headers=SurepassClient.HEADERS,
            json=payload,
            timeout=30
        )

        return response.json()