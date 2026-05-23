import os
import requests

AI_SERVICE_BASE_URL = os.getenv("AI_SERVICE_URL")


class AIServiceConnector:

    @staticmethod
    def process_ocr(file_path, candidate_id, document_type, token):

        url = f"{AI_SERVICE_BASE_URL}/ocr"

        headers = {
            "Authorization": token
        }

        files = {
            "file": open(file_path, "rb")
        }

        data = {
            "candidate_id": candidate_id,
            "document_type": document_type
        }

        response = requests.post(
            url,
            headers=headers,
            files=files,
            data=data
        )

        return response.json()

    @staticmethod
    def verify_ocr(extracted_data, expected_data, token):

        url = f"{AI_SERVICE_BASE_URL}/ocr/verify"

        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }

        payload = {
            "extracted_data": extracted_data,
            "expected_data": expected_data
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )

        return response.json()