from app.database.connection import get_connection
import uuid


class BGVRepository:

    @staticmethod
    def create_bgv_request(data):

        connection = get_connection()

        cursor = connection.cursor()

        request_id = f"BGV-{uuid.uuid4().hex[:10].upper()}"

        query = """
        INSERT INTO bgv_requests (
            candidate_id,
            request_id,
            company_name,
            package_name,
            status
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            data.get("candidate_id"),
            request_id,
            data.get("company_name"),
            data.get("package_name"),
            "INITIATED"
        )

        cursor.execute(query, values)

        connection.commit()

        bgv_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return {
            "bgv_id": bgv_id,
            "request_id": request_id
        }
    @staticmethod
    def get_bgv_by_candidate_id(candidate_id):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        SELECT id
        FROM bgv_requests
        WHERE candidate_id = %s
        ORDER BY id DESC
        LIMIT 1
        """

        cursor.execute(
            query,
            (candidate_id,)
        )

        row = cursor.fetchone()

        if row:

            bgv = {
                "id": row[0]
            }

        else:

            bgv = None

        cursor.close()
        connection.close()

        return bgv