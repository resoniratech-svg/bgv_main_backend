from app.provider_config import DIDIT

from app.utils.api_client import APIClient


class DiditClient:

    @staticmethod
    def create_session(payload):

        url = (
            f"{DIDIT['base_url']}/v3/session/"
        )

        headers = {

            "x-api-key": DIDIT["api_key"],

            "Content-Type": "application/json"
        }

        response = APIClient.post(

            url=url,

            payload=payload,

            headers=headers
        )

        return response