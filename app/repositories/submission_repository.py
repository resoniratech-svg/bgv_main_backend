from app.database.connection import get_connection


class SubmissionRepository:

    @staticmethod
    def create_submission(data):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO candidate_submission_status (

            candidate_id,
            bgv_id,
            access_link_id,
            submission_status,
            remarks

        )
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (

            data.get("candidate_id"),
            data.get("bgv_id"),
            data.get("access_link_id"),
            "SUBMITTED",
            data.get("remarks")

        )

        cursor.execute(query, values)

        connection.commit()

        submission_id = cursor.lastrowid

        update_query = """
        UPDATE candidate_access_links
        SET status = 'LOCKED'
        WHERE id = %s
        """

        cursor.execute(
            update_query,
            (data.get("access_link_id"),)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return {
            "submission_id": submission_id
        }