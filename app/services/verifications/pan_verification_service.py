import os
import requests


class PanVerificationService:

    BASE_URL = os.getenv("SUREPASS_BASE_URL")
    API_KEY = os.getenv("SUREPASS_API_KEY")

    @classmethod
    def verify_pan(cls, pan_number):

        url = f"{cls.BASE_URL}/pan/pan"

        headers = {
            "Authorization": f"Bearer {cls.API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "id_number": pan_number
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )

        return response.json()