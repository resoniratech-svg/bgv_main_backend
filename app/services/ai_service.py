import os
import requests

AI_SERVICE_URL = os.getenv("AI_SERVICE_URL")


def process_ocr(token, candidate_id, document_type, file_path):

    headers = {"Authorization": f"Bearer {token}"}

    with open(file_path, "rb") as f:
        files = {"file": f}

        data = {"candidate_id": candidate_id, "document_type": document_type}

        response = requests.post(
            f"{AI_SERVICE_URL}/ocr", headers=headers, files=files, data=data
        )

    return response.json()
