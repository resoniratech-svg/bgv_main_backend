from app.database.connection import get_connection
import uuid


class BGVRepository:

    @staticmethod
    def create_bgv_request(data):

        print("========== BGV CREATE START ==========")
        print("DATA:", data)

        connection = get_connection()
        cursor = connection.cursor()

        bgv_id = f"BGV-{uuid.uuid4().hex[:10].upper()}"

        query = """
        INSERT INTO bgv_requests (
            candidate_id,
            bgv_id,
            company_name,
            status
        )
        VALUES (%s, %s, %s, %s)
        """

        values = (
            data.get("candidate_id"),
            bgv_id,
            data.get("company_name"),
            "INITIATED"
        )

        print("VALUES:", values)

        cursor.execute(query, values)

        connection.commit()

        print("BGV INSERTED")
        print("LAST ID:", cursor.lastrowid)

        record_id = cursor.lastrowid

        cursor.close()
        connection.close()

        print("========== BGV CREATE END ==========")

        return {
            "id": record_id,
            "bgv_id": bgv_id
        }