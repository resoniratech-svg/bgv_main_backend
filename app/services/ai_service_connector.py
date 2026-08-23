import os
import requests

AI_SERVICE_BASE_URL = os.getenv("AI_SERVICE_URL")


class AIServiceConnector:
    @staticmethod
    def process_ocr(file_path, candidate_id, document_type, token):
        url = f"{AI_SERVICE_BASE_URL}/ocr"
        headers = {"Authorization": token}
        data = {"candidate_id": candidate_id, "document_type": document_type}

        # Context manager ensures the file stream closes cleanly after the request
        with open(file_path, "rb") as f:
            files = {"file": f}
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

    # @staticmethod
    # def get_aadhaar_result(candidate_id, token):
    #     url = f"{AI_SERVICE_BASE_URL}/aadhaar/result/{candidate_id}"
    #     headers = {"Authorization": token}

    #     response = requests.get(url, headers=headers)
    #     return response.json()

    @staticmethod
    def get_aadhaar_result(candidate_id, token=None):

        url = f"{AI_SERVICE_BASE_URL}/aadhaar/result/{candidate_id}"

        headers = {}

        if token:
            headers["Authorization"] = token

        response = requests.get(url, headers=headers, timeout=60)

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

    ########################################
    # PASSPORT VERIFICATION
    ########################################
    @staticmethod
    def verify_passport(
        candidate_id,
        bgv_id,
        front_document_id,
        back_document_id,
        token,
    ):
        url = f"{AI_SERVICE_BASE_URL}/passport/verify"

        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }

        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "front_document_id": front_document_id,
            "back_document_id": back_document_id,
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
        )

        return response.json()

    ########################################
    # GET PASSPORT RESULT
    ########################################
    @staticmethod
    def get_passport_result(candidate_id, token):
        url = f"{AI_SERVICE_BASE_URL}/passport/result/{candidate_id}"

        headers = {
            "Authorization": token,
        }

        response = requests.get(
            url,
            headers=headers,
        )

        return response.json()

    ########################################
    # DRIVING LICENSE VERIFICATION
    ########################################

    @staticmethod
    def verify_driving_license(
        candidate_id,
        bgv_id,
        front_document_id,
        back_document_id,
        token,
    ):

        url = f"{AI_SERVICE_BASE_URL}/driving-license/verify"

        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }

        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "front_document_id": front_document_id,
            "back_document_id": back_document_id,
        }

        print("=" * 80)
        print("DRIVING LICENSE AI SERVICE REQUEST")
        print("=" * 80)
        print("URL:", url)
        print("PAYLOAD:", payload)
        print("=" * 80)

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=180,
            )

        except requests.exceptions.Timeout:
            print("=" * 80)
            print("DRIVING LICENSE AI SERVICE TIMEOUT")
            print("=" * 80)

            return {
                "success": False,
                "message": ("Driving License verification AI service timed out"),
            }

        except requests.exceptions.ConnectionError as e:
            print("=" * 80)
            print("DRIVING LICENSE AI SERVICE CONNECTION ERROR")
            print(str(e))
            print("=" * 80)

            return {
                "success": False,
                "message": ("Unable to connect to Driving License AI service"),
            }

        except requests.exceptions.RequestException as e:
            print("=" * 80)
            print("DRIVING LICENSE AI SERVICE REQUEST ERROR")
            print(str(e))
            print("=" * 80)

            return {
                "success": False,
                "message": ("Driving License AI service request failed"),
                "error": str(e),
            }

        print("=" * 80)
        print("DRIVING LICENSE AI SERVICE RESPONSE")
        print("=" * 80)
        print("STATUS:", response.status_code)
        print("BODY:", response.text)
        print("=" * 80)

        # ==================================================
        # PARSE RESPONSE
        # ==================================================

        try:
            result = response.json()

        except ValueError:
            return {
                "success": False,
                "message": ("AI Service returned an invalid Driving License response"),
                "status_code": response.status_code,
                "raw_response": response.text,
            }

        # ==================================================
        # HTTP ERROR
        # ==================================================

        if not response.ok:
            return {
                "success": False,
                "message": result.get(
                    "message",
                    "Driving License verification failed",
                ),
                "status_code": response.status_code,
                "data": result,
            }

        # ==================================================
        # RETURN AI RESPONSE
        # ==================================================

        return result

    ########################################
    # GET DRIVING LICENSE RESULT
    ########################################

    @staticmethod
    def get_driving_license_result(
        candidate_id,
        token,
    ):

        url = f"{AI_SERVICE_BASE_URL}/driving-license/result/{candidate_id}"

        headers = {
            "Authorization": token,
        }

        print("=" * 80)
        print("GET DRIVING LICENSE RESULT")
        print("=" * 80)
        print("URL:", url)
        print("CANDIDATE ID:", candidate_id)
        print("=" * 80)

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=120,
            )

        except requests.exceptions.Timeout:
            print("=" * 80)
            print("DRIVING LICENSE RESULT TIMEOUT")
            print("=" * 80)

            return {
                "success": False,
                "message": ("Driving License result service timed out"),
            }

        except requests.exceptions.ConnectionError as e:
            print("=" * 80)
            print("DRIVING LICENSE RESULT CONNECTION ERROR")
            print(str(e))
            print("=" * 80)

            return {
                "success": False,
                "message": ("Unable to connect to Driving License result service"),
            }

        except requests.exceptions.RequestException as e:
            print("=" * 80)
            print("DRIVING LICENSE RESULT REQUEST ERROR")
            print(str(e))
            print("=" * 80)

            return {
                "success": False,
                "message": ("Driving License result request failed"),
                "error": str(e),
            }

        print("=" * 80)
        print("DRIVING LICENSE RESULT RESPONSE")
        print("=" * 80)
        print("STATUS:", response.status_code)
        print("BODY:", response.text)
        print("=" * 80)

        # ==================================================
        # PARSE RESPONSE
        # ==================================================

        try:
            result = response.json()

        except ValueError:
            return {
                "success": False,
                "message": (
                    "AI Service returned an invalid Driving License result response"
                ),
                "status_code": response.status_code,
                "raw_response": response.text,
            }

        # ==================================================
        # HTTP ERROR
        # ==================================================

        if not response.ok:
            return {
                "success": False,
                "message": result.get(
                    "message",
                    "Driving License result not found",
                ),
                "status_code": response.status_code,
                "data": result,
            }

        # ==================================================
        # RETURN RESULT
        # ==================================================

        return result

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

    ########################################
    # VERIFY CCRV
    ########################################
    @staticmethod
    def verify_ccrv(candidate_id, bgv_id, token):
        url = f"{AI_SERVICE_BASE_URL}/ccrv/verify"
        headers = {"Authorization": token, "Content-Type": "application/json"}
        payload = {"candidate_id": candidate_id, "bgv_id": bgv_id}

        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    ########################################
    # GET CCRV RESULT
    ########################################
    @staticmethod
    def get_ccrv_result(candidate_id, token):
        url = f"{AI_SERVICE_BASE_URL}/ccrv/result/{candidate_id}"
        headers = {"Authorization": token}

        response = requests.get(url, headers=headers)
        return response.json()

    ########################################
    # SAVE CANDIDATE CONSENT
    ########################################
    @staticmethod
    def save_candidate_consent(
        candidate_id,
        bgv_id,
        verification_type,
        consent_status,
        consent_text,
        consent_version,
        consent_source,
        token,
    ):
        url = f"{AI_SERVICE_BASE_URL}/candidate-consent"
        headers = {"Authorization": token, "Content-Type": "application/json"}
        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "verification_type": verification_type,
            "consent_status": consent_status,
            "consent_text": consent_text,
            "consent_version": consent_version,
            "consent_source": consent_source,
        }

        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    ########################################
    # GET CANDIDATE CONSENT
    ########################################
    @staticmethod
    def get_candidate_consent(candidate_id, bgv_id, verification_type, token):
        url = f"{AI_SERVICE_BASE_URL}/candidate-consent/{candidate_id}"
        headers = {"Authorization": token}
        params = {"bgv_id": bgv_id, "verification_type": verification_type}

        response = requests.get(url, headers=headers, params=params)
        return response.json()

    ########################################
    # CREDIT BUREAU VERIFICATION
    ########################################
    @staticmethod
    def verify_credit_bureau(candidate_id, bgv_id, first_name, last_name, phone, token):
        url = f"{AI_SERVICE_BASE_URL}/credit-bureau/verify"
        headers = {"Authorization": token, "Content-Type": "application/json"}
        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
        }

        print("=" * 80)
        print("AI CONNECTOR PAYLOAD")
        print(payload)
        print("=" * 80)
        print("URL =", url)

        response = requests.post(url, headers=headers, json=payload, timeout=180)

        print("=" * 80)
        print("AI SERVICE STATUS :", response.status_code)
        print("AI SERVICE HEADERS :", response.headers)
        print("AI SERVICE TEXT :")
        print(response.text)
        print("=" * 80)

        try:
            body = response.json()
        except Exception:
            raise Exception(
                f"AI Service returned invalid response.\n"
                f"Status : {response.status_code}\n"
                f"Body : {response.text}"
            )

        if response.status_code != 200:
            return body

        return body

    ########################################
    # CREDIT BUREAU RESULT
    ########################################
    @staticmethod
    def get_credit_bureau_result(candidate_id, token):
        url = f"{AI_SERVICE_BASE_URL}/credit-bureau/result/{candidate_id}"
        headers = {"Authorization": token}

        response = requests.get(url, headers=headers, timeout=120)

        print("=" * 80)
        print("CREDIT BUREAU RESULT RESPONSE")
        print(response.status_code)
        print(response.text)
        print("=" * 80)

        return response.json()

    ########################################
    # SALARY SLIP OCR
    ########################################
    @staticmethod
    def verify_salary_slip(candidate_id, bgv_id, document_id, token):
        url = f"{AI_SERVICE_BASE_URL}/salary-slip/ocr"
        headers = {"Authorization": token, "Content-Type": "application/json"}
        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "document_id": document_id,
        }

        print("=" * 80)
        print("SALARY SLIP OCR REQUEST")
        print(payload)
        print("=" * 80)
        print("URL =", url)

        response = requests.post(url, headers=headers, json=payload, timeout=180)

        print("=" * 80)
        print("SALARY SLIP OCR RESPONSE")
        print(response.status_code)
        print(response.text)
        print("=" * 80)

        response.raise_for_status()
        return response.json()

    ########################################
    # GET SALARY SLIP OCR RESULT
    ########################################
    @staticmethod
    def get_salary_slip_result(candidate_id, token):
        url = f"{AI_SERVICE_BASE_URL}/salary-slip/result/{candidate_id}"
        headers = {"Authorization": token}

        response = requests.get(url, headers=headers, timeout=120)

        print("=" * 80)
        print("SALARY SLIP RESULT")
        print(response.status_code)
        print(response.text)
        print("=" * 80)

        response.raise_for_status()
        return response.json()

    # =====================================================
    # VERIFY EMPLOYMENT
    # =====================================================
    @staticmethod
    def verify_employment(candidate_id, bgv_id, mobile_number, token):
        url = f"{AI_SERVICE_BASE_URL}/employment/verify"
        headers = {"Authorization": token, "Content-Type": "application/json"}
        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "mobile_number": mobile_number,
        }

        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    # =====================================================
    # GET EMPLOYMENT RESULT
    # =====================================================
    @staticmethod
    def get_employment_result(candidate_id, token):
        url = f"{AI_SERVICE_BASE_URL}/employment/result/{candidate_id}"
        headers = {"Authorization": token}

        response = requests.get(url, headers=headers)
        return response.json()

    # ########################################
    # # BANK STATEMENT UPLOAD
    # ########################################
    # @staticmethod
    # def upload_bank_statement(
    #     candidate_id, bgv_id, document_id, bank_name, bank_statement_password, token
    # ):
    #     url = f"{AI_SERVICE_BASE_URL}/bank-statement/upload"

    #     headers = {"Authorization": token, "Content-Type": "application/json"}

    #     payload = {
    #         "candidate_id": candidate_id,
    #         "bgv_id": bgv_id,
    #         "document_id": document_id,
    #         "bank_name": bank_name,
    #         "bank_statement_password": bank_statement_password,
    #     }

    #     response = requests.post(url, headers=headers, json=payload, timeout=180)

    #     return response.json()

    # ########################################
    # # BANK STATEMENT RESULT
    # ########################################
    # @staticmethod
    # def get_bank_statement_result(candidate_id, bgv_id, token):

    #     url = f"{AI_SERVICE_BASE_URL}/bank-statement/result/{candidate_id}"

    #     headers = {
    #         "Authorization": token,
    #     }

    #     params = {
    #         "bgv_id": bgv_id,
    #     }

    #     response = requests.get(
    #         url,
    #         headers=headers,
    #         params=params,
    #         timeout=120,
    #     )

    #     return response.json()

    ########################################
    # BANK STATEMENT UPLOAD
    ########################################
    @staticmethod
    def upload_bank_statement(
        candidate_id, bgv_id, document_id, bank_name, bank_statement_password, token
    ):
        url = f"{AI_SERVICE_BASE_URL}/bank-statement/upload"

        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }

        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "document_id": document_id,
            "bank_name": bank_name,
            "bank_statement_password": bank_statement_password,
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=180,
        )

        return response.json()

    ########################################
    # BANK STATEMENT RESULT
    ########################################
    @staticmethod
    def get_bank_statement_result(candidate_id, bgv_id, token):

        url = f"{AI_SERVICE_BASE_URL}/bank-statement/result/{candidate_id}"

        headers = {
            "Authorization": token,
        }

        params = {
            "bgv_id": bgv_id,
        }

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=120,
        )

        return response.json()

    # ########################################
    # # GET AADHAAR RESULT
    # ########################################
    # @staticmethod
    # def fetch_aadhaar_result(secure_token, token):

    #     url = f"{AI_SERVICE_BASE_URL}/candidate/aadhaar/result/{secure_token}"

    #     headers = {}

    #     if token:
    #         headers["Authorization"] = token

    #     response = requests.get(url, headers=headers, timeout=120)

    #     return response.json()

    @staticmethod
    def save_aadhaar_result(
        candidate_id,
        bgv_id,
        aadhaar_data,
    ):

        url = f"{AI_SERVICE_BASE_URL}/aadhaar/result"

        headers = {
            "Content-Type": "application/json",
        }

        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "aadhaar_data": aadhaar_data,
        }

        print("=" * 80)
        print("SAVE AADHAAR RESULT TO AI SERVICE")
        print("URL:", url)
        print("CANDIDATE ID:", candidate_id)
        print("BGV ID:", bgv_id)
        print("=" * 80)

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=120,
        )

        print("AI SERVICE STATUS:", response.status_code)
        print("AI SERVICE RESPONSE:", response.text)

        return response.json()
