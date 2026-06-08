from app.database.connection import get_connection

from datetime import datetime, timedelta
import uuid


class CandidateLinkRepository:

    @staticmethod
    def create_secure_link(data):

        connection = get_connection()

        cursor = connection.cursor()

        secure_token = uuid.uuid4().hex

        expires_at = datetime.utcnow() + timedelta(hours=48)

        query = """
        INSERT INTO candidate_access_links (
            candidate_id,
            bgv_id,
            secure_token,
            status,
            expires_at
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            data.get("candidate_id"),
            data.get("bgv_id"),
            secure_token,
            "ACTIVE",
            expires_at
        )

        cursor.execute(query, values)

        connection.commit()

        link_id = cursor.lastrowid

        cursor.close()
        connection.close()

        upload_url = (
            f"http://localhost:3000/upload/{secure_token}"
        )

        return {
            "link_id": link_id,
            "secure_token": secure_token,
            "upload_url": upload_url,
            "expires_at": str(expires_at)
        }

    @staticmethod
    def validate_secure_token(secure_token):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        SELECT
            cal.id,
            cal.candidate_id,
            br.bgv_id,
            cal.status,
            cal.expires_at,
            c.first_name,
            c.last_name,
            c.email

        FROM candidate_access_links cal

        INNER JOIN candidates c
            ON cal.candidate_id = c.id

        INNER JOIN bgv_requests br
            ON cal.bgv_id = br.id

        WHERE cal.secure_token = %s
        """

        cursor.execute(query, (secure_token,))

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if not result:

            return {
                "status": "error",
                "message": "Invalid secure link"
            }

        if result["status"] != "ACTIVE":

            return {
                "status": "error",
                "message": "Link already used or locked"
            }

        expires_at = result["expires_at"]
        if isinstance(expires_at, str):
            expires_at = datetime.fromisoformat(
                  expires_at
            )

        if datetime.utcnow() > expires_at:
            return {
                "status": "error",
                "message": "Link expired"
            }
        return {
            "status": "success",
            "message": "Valid secure link",
            "data": result
        }