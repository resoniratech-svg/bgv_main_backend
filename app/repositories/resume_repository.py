from app.database.connection import get_connection


class ResumeRepository:

    @staticmethod
    def get_parsed_resume(candidate_id):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        SELECT *
        FROM parsed_candidates
        WHERE candidate_id = %s
        ORDER BY id DESC
        LIMIT 1
        """

        cursor.execute(
            query,
            (candidate_id,)
        )

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result