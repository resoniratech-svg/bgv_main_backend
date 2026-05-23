from app.database.connection import get_connection
import uuid


class CandidateRepository:

    @staticmethod
    def create_candidate(data):

        connection = get_connection()

        cursor = connection.cursor()

        candidate_code = f"CAND-{uuid.uuid4().hex[:8].upper()}"

        query = """
        INSERT INTO candidates (
            candidate_code,
            first_name,
            last_name,
            email,
            phone,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            candidate_code,
            data.get("first_name"),
            data.get("last_name"),
            data.get("email"),
            data.get("phone"),
            "PENDING"
        )

        cursor.execute(query, values)

        connection.commit()

        candidate_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return {
            "candidate_id": candidate_id,
            "candidate_code": candidate_code
        }