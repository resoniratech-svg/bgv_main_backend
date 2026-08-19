import uuid
from app.database.connection import get_connection

class CandidateRepository:

    @staticmethod
    def create_candidate(data: dict) -> dict:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Generate a short, upper-case unique code
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

        try:
            cursor.execute(query, values)
            connection.commit()
            candidate_id = cursor.lastrowid
            
            return {
                "candidate_id": candidate_id,
                "candidate_code": candidate_code
            }
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_candidates() -> list:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT
            id, candidate_code, first_name, last_name, email, phone,
            status, date_of_birth, gender, created_at, updated_at
        FROM candidates
        ORDER BY created_at DESC
        """

        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_candidate_by_id(candidate_id: int) -> dict:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT
            id, candidate_code, first_name, last_name, email, phone,
            status, date_of_birth, gender, created_at, updated_at
        FROM candidates
        WHERE id = %s
        """

        try:
            cursor.execute(query, (candidate_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_candidate_profile(candidate_id: int, date_of_birth: str, gender: str) -> bool:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        UPDATE candidates
        SET
            date_of_birth = %s,
            gender = %s
        WHERE id = %s
        """

        try:
            cursor.execute(query, (date_of_birth, gender, candidate_id))
            connection.commit()
            return cursor.rowcount > 0  # Returns True if a row was actually updated
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()