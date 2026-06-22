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
    
    @staticmethod
    def parse_resume(file_path, candidate_id):

        url = f"{AI_SERVICE_BASE_URL}/resume/parse"

        files = {
            "resume": open(file_path, "rb")
        }

        data = {
            "candidate_id": candidate_id
        }

        response = requests.post(
            url,
            files=files,
            data=data
        )

        return response.json()
    
    @staticmethod
    def screen_watchlist(
        candidate_id,
        full_name,
        dob=None,
        gender=None,
    ):

        url = f"{AI_SERVICE_BASE_URL}/watchlist/screen"

        print("WATCHLIST INPUTS")
        print(type(candidate_id), candidate_id)
        print(type(full_name), full_name)
        print("DOB RECEIVED IN CONNECTOR")
        print(dob)
        print(type(dob))
        payload = {
            "candidate_id": candidate_id,
            "full_name": full_name,
            "dob": dob,
            "gender": gender,
        }

        print("WATCHLIST PAYLOAD:")
        print(payload)

        response = requests.post(
            url,
            json=payload
        )

        return response.json()
    
    @staticmethod
    def generate_report(candidate_id):

        url = f"{AI_SERVICE_BASE_URL}/reports/generate"

        payload = {
            "candidate_id": candidate_id
        }

        response = requests.post(
            url,
            json=payload
        )

        return response.json()
    
    @staticmethod
    def download_report(candidate_id, token):

        url = (
            f"{AI_SERVICE_BASE_URL}"
            f"/reports/download/{candidate_id}"
        )

        headers = {
            "Authorization": token
        }

        response = requests.get(
            url,
            headers=headers,
            stream=True
        )

        return response
    @staticmethod
    def verify_salary_slip(
        file_path,
        candidate_id
    ):

        url = (
            f"{AI_SERVICE_BASE_URL}"
            "/salary-slip/verify"
        )

        data = {
            "candidate_id": candidate_id
        }

        try:

            with open(
                file_path,
                "rb"
            ) as file:

                files = {
                    "file": file
                }

                response = requests.post(
                    url,
                    files=files,
                    data=data,
                    timeout=120
                )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:

            print(
                "SALARY SLIP API ERROR:",
                str(e)
            )

            return {
                "success": False,
                "message": str(e)
            }