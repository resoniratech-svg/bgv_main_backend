from app.database.connection import get_connection


class VerificationRepository:

    @staticmethod
    def create_verification_result(
        bgv_id,
        verification_type_id,
        status,
        remarks,
        module_score
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO verification_results (
            bgv_id,
            verification_type_id,
            status,
            remarks,
            module_score
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            bgv_id,
            verification_type_id,
            status,
            remarks,
            module_score
        )

        cursor.execute(query, values)

        connection.commit()

        verification_result_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return verification_result_id