from app.database.connection import get_connection


class ReportRepository:

    @staticmethod
    def get_all_reports():

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        SELECT

            br.id,

            br.candidate_id,

            CONCAT(
                c.first_name,
                ' ',
                IFNULL(c.last_name, '')
            ) AS candidate_name,

            c.email,

            br.report_name,

            br.report_status,

            br.verification_status,

            br.file_name,

            br.file_url,

            br.generated_at

        FROM bgv_reports br

        INNER JOIN candidates c
            ON c.id = br.candidate_id

        WHERE br.is_deleted = 0

        ORDER BY br.generated_at DESC
        """

        cursor.execute(query)

        reports = cursor.fetchall()

        print("REPORTS =", reports)

        cursor.close()

        connection.close()

        return reports


    @staticmethod
    def get_latest_report_by_candidate(
        candidate_id
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        SELECT *
        FROM bgv_reports
        WHERE candidate_id = %s
        AND is_deleted = 0
        ORDER BY id DESC
        LIMIT 1
        """

        cursor.execute(
            query,
            (candidate_id,)
        )

        report = cursor.fetchone()

        cursor.close()
        connection.close()

        return report