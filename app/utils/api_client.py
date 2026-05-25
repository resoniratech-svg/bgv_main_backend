import requests


class APIClient:

    DEFAULT_TIMEOUT = 30

    @staticmethod
    def post(
        url,
        payload=None,
        headers=None,
        timeout=None
    ):

        try:

            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=(
                    timeout
                    or APIClient.DEFAULT_TIMEOUT
                )
            )

            return {
                "success": True,
                "status_code": response.status_code,
                "response": response.json()
            }

        except requests.exceptions.Timeout:

            return {
                "success": False,
                "message": "External API timeout"
            }

        except requests.exceptions.ConnectionError:

            return {
                "success": False,
                "message": "External API connection error"
            }

        except Exception as e:

            return {
                "success": False,
                "message": str(e)
            }

    @staticmethod
    def get(
        url,
        headers=None,
        timeout=None
    ):

        try:

            response = requests.get(
                url,
                headers=headers,
                timeout=(
                    timeout
                    or APIClient.DEFAULT_TIMEOUT
                )
            )

            return {
                "success": True,
                "status_code": response.status_code,
                "response": response.json()
            }

        except requests.exceptions.Timeout:

            return {
                "success": False,
                "message": "External API timeout"
            }

        except requests.exceptions.ConnectionError:

            return {
                "success": False,
                "message": "External API connection error"
            }

        except Exception as e:

            return {
                "success": False,
                "message": str(e)
            }