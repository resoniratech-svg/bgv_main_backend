import os
import requests
from msal import ConfidentialClientApplication


class EmailService:
#=======================
# VERIFICATION EMAIL
#=======================
    @staticmethod
    def send_verification_email(
        candidate_email,
        candidate_name,
        upload_url
    ):

        tenant_id = os.getenv("GRAPH_TENANT_ID")
        client_id = os.getenv("GRAPH_CLIENT_ID")
        client_secret = os.getenv("GRAPH_CLIENT_SECRET")
        sender_email = os.getenv("GRAPH_SENDER_EMAIL")

        authority = (
            f"https://login.microsoftonline.com/{tenant_id}"
        )

        app = ConfidentialClientApplication(
            client_id,
            authority=authority,
            client_credential=client_secret
        )

        token_result = app.acquire_token_for_client(
            scopes=[
                "https://graph.microsoft.com/.default"
            ]
        )

        access_token = token_result["access_token"]

        email_body = f"""
Hello {candidate_name},

Please complete your Background Verification process.

Upload documents here:

{upload_url}

This link expires in 48 hours.

Regards,
Kraves Team
"""

        endpoint = (
            f"https://graph.microsoft.com/v1.0/users/{sender_email}/sendMail"
        )

        payload = {
            "message": {
                "subject": "Background Verification Request",
                "body": {
                    "contentType": "Text",
                    "content": email_body
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": candidate_email
                        }
                    }
                ]
            }
        }

        response = requests.post(
            endpoint,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            json=payload
        )

        print("EMAIL STATUS:", response.status_code)
        print("EMAIL RESPONSE:", response.text)

        print(response.status_code)
        print(response.text)

        return response.status_code == 202
    
#=======================
# ADMIN ALERT
#=======================
    @staticmethod
    def send_admin_alert(
        subject,
        message
    ):

        tenant_id = os.getenv(
            "GRAPH_TENANT_ID"
        )

        client_id = os.getenv(
            "GRAPH_CLIENT_ID"
        )

        client_secret = os.getenv(
            "GRAPH_CLIENT_SECRET"
        )

        sender_email = os.getenv(
            "GRAPH_SENDER_EMAIL"
        )

        authority = (
            f"https://login.microsoftonline.com/{tenant_id}"
        )

        app = ConfidentialClientApplication(
            client_id,
            authority=authority,
            client_credential=client_secret
        )

        token_result = (
            app.acquire_token_for_client(
                scopes=[
                    "https://graph.microsoft.com/.default"
                ]
            )
        )

        access_token = (
            token_result["access_token"]
        )

        endpoint = (
            f"https://graph.microsoft.com/v1.0/users/{sender_email}/sendMail"
        )

        payload = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":
                            "kraves@resonira.com"
                        }
                    }
                ]
            }
        }

        response = requests.post(
            endpoint,
            headers={
                "Authorization":
                f"Bearer {access_token}",
                "Content-Type":
                "application/json"
            },
            json=payload
        )

        print(
            "ADMIN EMAIL STATUS:",
            response.status_code
        )

        return (
            response.status_code == 202
        )

    # =======================
# PASSWORD RESET EMAIL
# =======================
    @staticmethod
    def send_password_reset_email(
        recipient_email,
        user_name,
        reset_link
    ):

        tenant_id = os.getenv(
            "GRAPH_TENANT_ID"
        )

        client_id = os.getenv(
            "GRAPH_CLIENT_ID"
        )

        client_secret = os.getenv(
            "GRAPH_CLIENT_SECRET"
        )

        sender_email = os.getenv(
            "GRAPH_SENDER_EMAIL"
        )

        authority = (
            f"https://login.microsoftonline.com/{tenant_id}"
        )

        app = ConfidentialClientApplication(
            client_id,
            authority=authority,
            client_credential=client_secret
        )

        token_result = (
            app.acquire_token_for_client(
                scopes=[
                    "https://graph.microsoft.com/.default"
                ]
            )
        )

        access_token = (
            token_result["access_token"]
        )

        email_body = f"""
    Hello {user_name},

    A request was received to reset your password.

    Click the link below:

    {reset_link}

    This link will expire in 1 hour.

    If you did not request this reset,
    please ignore this email.

    Regards,
    Kraves Team
    """

        endpoint = (
            f"https://graph.microsoft.com/v1.0/users/{sender_email}/sendMail"
        )

        payload = {
            "message": {
                "subject":
                "Password Reset Request",
                "body": {
                    "contentType":
                    "Text",
                    "content":
                    email_body
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":
                            recipient_email
                        }
                    }
                ]
            }
        }

        response = requests.post(
            endpoint,
            headers={
                "Authorization":
                f"Bearer {access_token}",
                "Content-Type":
                "application/json"
            },
            json=payload
        )

        print(
            "RESET EMAIL STATUS:",
            response.status_code
        )

        print(
            "RESET EMAIL RESPONSE:",
            response.text
        )

        return (
            response.status_code == 202
        )