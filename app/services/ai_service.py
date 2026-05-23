import requests


AI_SERVICE_URL = "http://127.0.0.1:5001/api/v1"


def process_ocr(
    token,
    candidate_id,
    document_type,
    file_path
):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    files = {
        "file": open(file_path, "rb")
    }

    data = {
        "candidate_id": candidate_id,
        "document_type": document_type
    }

    response = requests.post(
        f"{AI_SERVICE_URL}/ocr",
        headers=headers,
        files=files,
        data=data
    )

    return response.json()