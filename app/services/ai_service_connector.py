import os
import requests

AI_SERVICE_BASE_URL = os.getenv("AI_SERVICE_URL")


class AIServiceConnector:
    @staticmethod
    def process_ocr(file_path, candidate_id, document_type, token):
        url = f"{AI_SERVICE_BASE_URL}/ocr"
        headers = {"Authorization": token}
        files = {"file": open(file_path, "rb")}
        data = {"candidate_id": candidate_id, "document_type": document_type}

        response = requests.post(url, headers=headers, files=files, data=data)
        return response.json()

    @staticmethod
    def verify_ocr(extracted_data, expected_data, token):
        url = f"{AI_SERVICE_BASE_URL}/ocr/verify"
        headers = {"Authorization": token, "Content-Type": "application/json"}
        payload = {"extracted_data": extracted_data, "expected_data": expected_data}

        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    @staticmethod
    def verify_pan(candidate_id, bgv_id, document_id, token):

        url = f"{AI_SERVICE_BASE_URL}/pan/verify"

        headers = {"Authorization": token, "Content-Type": "application/json"}

        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "document_id": document_id,
        }

        response = requests.post(url, headers=headers, json=payload)

        return response.json()

    @staticmethod
    def parse_resume(file_path, candidate_id):

        url = f"{AI_SERVICE_BASE_URL}/resume/parse"

        files = {"resume": open(file_path, "rb")}

        data = {"candidate_id": candidate_id}

        response = requests.post(url, files=files, data=data)

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

        response = requests.post(url, json=payload)

        return response.json()

    @staticmethod
    def generate_report(candidate_id):

        url = f"{AI_SERVICE_BASE_URL}/reports/generate"

        payload = {"candidate_id": candidate_id}

        response = requests.post(url, json=payload)

        return response.json()

    @staticmethod
    def download_report(candidate_id, token):

        url = f"{AI_SERVICE_BASE_URL}/reports/download/{candidate_id}"

        headers = {"Authorization": token}

        response = requests.get(url, headers=headers)

        return response

    @staticmethod
    def get_pan_result(candidate_id, token):

        url = f"{AI_SERVICE_BASE_URL}/pan/result/{candidate_id}"

        headers = {"Authorization": token}

        response = requests.get(url, headers=headers)

        return response.json()

    @staticmethod
    def verify_face_match(candidate_id, bgv_id, document_id, token):

        url = f"{AI_SERVICE_BASE_URL}/face-match/verify"

        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }

        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "document_id": document_id,
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
        )

        return response.json()

    @staticmethod
    def get_face_match_result(candidate_id, token):

        url = f"{AI_SERVICE_BASE_URL}/face-match/result/{candidate_id}"

        headers = {
            "Authorization": token,
        }

        response = requests.get(
            url,
            headers=headers,
        )

        return response.json()

    @staticmethod
    def verify_salary_slip(file_path, candidate_id):

        url = f"{AI_SERVICE_BASE_URL}/salary-slip/verify"

        data = {"candidate_id": candidate_id}

        try:
            with open(file_path, "rb") as file:
                files = {"file": file}

                response = requests.post(url, files=files, data=data, timeout=120)

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            print("SALARY SLIP API ERROR:", str(e))

            return {"success": False, "message": str(e)}
            headers = headers

        return response.json()

    @staticmethod
    def generate_aadhaar_qr(candidate_id, bgv_id, token):
        url = f"{AI_SERVICE_BASE_URL}/aadhaar/generate-qr"
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = token
        payload = {"candidate_id": candidate_id, "bgv_id": bgv_id}

        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    @staticmethod
    def get_aadhaar_status(candidate_id, token=None):

        url = f"{AI_SERVICE_BASE_URL}/aadhaar/status/{candidate_id}"

        headers = {}

        if token:
            headers["Authorization"] = token

        response = requests.get(url, headers=headers)

        return response.json()

    @staticmethod
    def get_aadhaar_result(candidate_id, token):
        url = f"{AI_SERVICE_BASE_URL}/aadhaar/result/{candidate_id}"
        headers = {"Authorization": token}

        response = requests.get(url, headers=headers)
        return response.json()

    @staticmethod
    def verify_aadhaar(candidate_id, bgv_id, document_id, token):
        url = f"{AI_SERVICE_BASE_URL}/aadhaar/verify"
        headers = {"Authorization": token, "Content-Type": "application/json"}
        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "document_id": document_id,
        }

        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    @staticmethod
    def verify_passport(candidate_id, bgv_id, document_id, token):
        url = f"{AI_SERVICE_BASE_URL}/passport/verify"
        headers = {"Authorization": token, "Content-Type": "application/json"}
        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "document_id": document_id,
        }

        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    @staticmethod
    def verify_driving_license(
        candidate_id, bgv_id, front_document_id, back_document_id, token
    ):
        url = f"{AI_SERVICE_BASE_URL}/driving-license/verify"
        headers = {"Authorization": token, "Content-Type": "application/json"}
        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "front_document_id": front_document_id,
            "back_document_id": back_document_id,
        }

        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    @staticmethod
    def get_salary_slip_result(candidate_id):

        url = f"{AI_SERVICE_BASE_URL}/salary-slip/result/{candidate_id}"

        print("\n====================")
        print("SALARY RESULT URL")
        print(url)

        response = requests.get(url)

        print("STATUS CODE")
        print(response.status_code)

        print("RESPONSE TEXT")
        print(response.text)

        print("====================\n")

        return response.json()

    @staticmethod
    def verify_deepfake(candidate_id, bgv_id, document_id, token):

        url = f"{AI_SERVICE_BASE_URL}/deepfake/verify"

        headers = {"Authorization": token, "Content-Type": "application/json"}

        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "document_id": document_id,
        }

        print("\n===================")
        print("DEEPFAKE URL")
        print(url)

        print("PAYLOAD")
        print(payload)

        response = requests.post(url, headers=headers, json=payload)

        print("STATUS CODE")
        print(response.status_code)

        print("RESPONSE TEXT")
        print(response.text)

        print("===================\n")

        return response.json()

    @staticmethod
    def get_deepfake_result(candidate_id, token):

        url = f"{AI_SERVICE_BASE_URL}/deepfake/result/{candidate_id}"

        headers = {"Authorization": token}

        response = requests.get(url, headers=headers)

        return response.json()
