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
        data = {
            "candidate_id": candidate_id,
            "document_type": document_type
        }

        # Context manager ensures the file stream closes cleanly after the request
        with open(file_path, "rb") as f:
            files = {"file": f}
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
    def verify_pan(candidate_id, bgv_id, document_id, token):
        url = f"{AI_SERVICE_BASE_URL}/pan/verify"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "document_id": document_id
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )
        return response.json()
    
    @staticmethod
    def get_pan_result(candidate_id, token):
        url = f"{AI_SERVICE_BASE_URL}/pan/result/{candidate_id}"
        headers = {
            "Authorization": token
        }

        response = requests.get(
            url,
            headers=headers
        )
        return response.json()

    @staticmethod
    def generate_aadhaar_qr(candidate_id, bgv_id, token):
        url = f"{AI_SERVICE_BASE_URL}/aadhaar/generate-qr"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )
        return response.json()

    @staticmethod
    def get_aadhaar_status(candidate_id, token):
        url = f"{AI_SERVICE_BASE_URL}/aadhaar/status/{candidate_id}"
        headers = {
            "Authorization": token
        }

        response = requests.get(
            url,
            headers=headers
        )
        return response.json()

    @staticmethod
    def get_aadhaar_result(candidate_id, token):
        url = f"{AI_SERVICE_BASE_URL}/aadhaar/result/{candidate_id}"
        headers = {
            "Authorization": token
        }

        response = requests.get(
            url,
            headers=headers
        )
        return response.json()

    @staticmethod
    def verify_aadhaar(candidate_id, bgv_id, document_id, token):
        url = f"{AI_SERVICE_BASE_URL}/aadhaar/verify"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "document_id": document_id
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )
        return response.json()
    
    @staticmethod
    def verify_passport(candidate_id, bgv_id, document_id, token):
        url = f"{AI_SERVICE_BASE_URL}/passport/verify"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "document_id": document_id
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )
        return response.json()
    
    @staticmethod
    def get_passport_result(candidate_id, token):

        url = (
            f"{AI_SERVICE_BASE_URL}"
            f"/passport/result/{candidate_id}"
        )

        headers = {
            "Authorization": token
        }

        response = requests.get(
            url,
            headers=headers
        )

        return response.json()

    @staticmethod
    def verify_driving_license(candidate_id, bgv_id, front_document_id, back_document_id, token):
        url = f"{AI_SERVICE_BASE_URL}/driving-license/verify"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "front_document_id": front_document_id,
            "back_document_id": back_document_id
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )
        return response.json()
    
    @staticmethod
    def get_driving_license_result(

        candidate_id,

        token

    ):

        url = (

            f"{AI_SERVICE_BASE_URL}"

            f"/driving-license/result/{candidate_id}"

        )

        headers = {

            "Authorization": token

        }

        response = requests.get(

            url,

            headers=headers

        )

        return response.json()

    ########################################
    # VERIFY DEEPFAKE
    ########################################
    @staticmethod
    def verify_deepfake(candidate_id, bgv_id, document_id, token):
        url = f"{AI_SERVICE_BASE_URL}/deepfake/verify"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        payload = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "document_id": document_id
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )
        return response.json()

    ########################################
    # GET RESULT
    ########################################
    @staticmethod
    def get_deepfake_result(candidate_id, token):
        url = f"{AI_SERVICE_BASE_URL}/deepfake/result/{candidate_id}"
        headers = {
            "Authorization": token
        }

        response = requests.get(
            url,
            headers=headers
        )
        return response.json()
    

    
@staticmethod
def get_deepfake_result(

        candidate_id,

        token

):



    url=(


        f"{AI_SERVICE_BASE_URL}"


        f"/deepfake/result/{candidate_id}"


    )



    headers={


        "Authorization":

        token


    }



    response=requests.get(


        url,


        headers=headers


    )



    return response.json()



@staticmethod
def verify_face_match(

        candidate_id,
        bgv_id,
        document_id,
        token

):


    url=(

        f"{AI_SERVICE_BASE_URL}"

        "/face-match/verify"

    )


    headers={

        "Authorization":token,

        "Content-Type":

        "application/json"

    }


    payload={

        "candidate_id":

        candidate_id,


        "bgv_id":

        bgv_id,


        "document_id":

        document_id

    }



    response=requests.post(

        url,

        headers=headers,

        json=payload

    )


    return response.json()



# ==========================================
# GET FACE MATCH RESULT
# ==========================================

@staticmethod
def get_face_match_result(

        candidate_id,

        token

):



    url=(

        f"{AI_SERVICE_BASE_URL}"

        f"/face-match/result/{candidate_id}"

    )



    headers={


        "Authorization":

        token

    }



    response=requests.get(

        url,

        headers=headers

    )

    return response.json()

########################################
# VERIFY CCRV
########################################

@staticmethod
def verify_ccrv(

        candidate_id,

        bgv_id,

        token

):

    url = (

        f"{AI_SERVICE_BASE_URL}"

        "/ccrv/verify"

    )

    headers = {

        "Authorization": token,

        "Content-Type": "application/json"

    }

    payload = {

        "candidate_id": candidate_id,

        "bgv_id": bgv_id

    }

    response = requests.post(

        url,

        headers=headers,

        json=payload

    )

    return response.json()


########################################
# GET CCRV RESULT
########################################

@staticmethod
def get_ccrv_result(

        candidate_id,

        token

):

    url = (

        f"{AI_SERVICE_BASE_URL}"

        f"/ccrv/result/{candidate_id}"

    )

    headers = {

        "Authorization": token

    }

    response = requests.get(

        url,

        headers=headers

    )

    return response.json()
