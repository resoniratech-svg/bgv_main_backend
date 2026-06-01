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

    @staticmethod
    def get_all_candidates():

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        SELECT
            id,
            CONCAT(first_name, ' ', last_name) AS full_name,
            email,
            phone,
            status
        FROM candidates
        WHERE is_deleted = 0
        """

        cursor.execute(query)

        candidates = cursor.fetchall()

        cursor.close()
        connection.close()

        return candidates
    @staticmethod
    def get_candidate_by_id(candidate_id):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        SELECT
            id,
            CONCAT(first_name, ' ', last_name) AS full_name,
            email,
            phone,
            status
        FROM candidates
        WHERE id = %s
        """

        cursor.execute(query, (candidate_id,))

        candidate = cursor.fetchone()

        cursor.close()
        connection.close()

        return candidate
    
    @staticmethod
    def update_candidate_status(candidate_id, data):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        UPDATE candidates
        SET status = %s
        WHERE id = %s
        """

        cursor.execute(
            query,
            (
                data.get("status"),
                candidate_id
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return {
            "status": "success",
            "message": "Candidate status updated successfully"
        }
    @staticmethod
    def update_candidate(candidate_id, data):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        UPDATE candidates
        SET
            first_name = %s,
            last_name = %s,
            email = %s,
            phone = %s
        WHERE id = %s
        """

        cursor.execute(
            query,
            (
                data.get("first_name"),
                data.get("last_name"),
                data.get("email"),
                data.get("phone"),
                candidate_id
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return {
            "status": "success",
            "message": "Candidate updated successfully"
        }
    @staticmethod
    def delete_candidate(candidate_id):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        UPDATE candidates
        SET is_deleted = 1
        WHERE id = %s
        """

        cursor.execute(
            query,
            (candidate_id,)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return {
            "status": "success",
            "message": "Candidate deleted successfully"
        }