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
    def get_latest_report_by_candidate(candidate_id):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT *
        FROM bgv_reports
        WHERE candidate_id=%s
        ORDER BY id DESC
        LIMIT 1
        """

        cursor.execute(query, (candidate_id,))
        report = cursor.fetchone()
        print("REPORT FOUND =", report)

        cursor.close()
        connection.close()
        return report

    @staticmethod
    def get_complete_report(candidate_id):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT
            cvs.candidate_id,
            cvs.candidate_name,
            cvs.email,
            cvs.phone,
            cvs.aadhaar_status,
            cvs.pan_status,
            cvs.passport_status,
            cvs.face_match_status,
            cvs.resume_status,
            cvs.education_status,
            cvs.employment_status,
            cvs.credit_status,
            cvs.court_status,
            cvs.watchlist_status,
            cvs.dl_status,
            cvs.deepfake_status,
            cvs.salary_slip_status,
            cvs.overall_status,
            cvs.risk_level,
            br.generated_at
        FROM candidate_verification_summary cvs
        LEFT JOIN bgv_reports br
            ON br.candidate_id = cvs.candidate_id
        WHERE cvs.candidate_id = %s
        ORDER BY br.id DESC
        LIMIT 1
        """

        cursor.execute(query, (candidate_id,))
        report = cursor.fetchone()
        cursor.close()
        connection.close()
        return report

    @staticmethod
    def get_latest_bgv_id(candidate_id):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT bgv_id
            FROM bgv_reports
            WHERE candidate_id=%s
            ORDER BY id DESC
            LIMIT 1
        """,
            (candidate_id,),
        )

        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result

    @staticmethod
    def get_report_preview(candidate_id):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT
            cvs.*,
            c.first_name,
            c.last_name,
            c.email,
            c.phone
        FROM candidate_verification_summary cvs
        INNER JOIN candidates c
            ON c.id = cvs.candidate_id
        WHERE cvs.candidate_id = %s
        LIMIT 1
        """

        cursor.execute(query, (candidate_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result

    @staticmethod
    def get_report_view_data(candidate_id):
        from pymysql.cursors import DictCursor

        connection = get_connection()
        cursor = connection.cursor(DictCursor)

        query = """
        SELECT
            candidate_id,
            candidate_name,
            email,
            phone,
            aadhaar_status,
            pan_status,
            passport_status,
            dl_status,
            face_match_status,
            resume_status,
            education_status,
            employment_status,
            salary_slip_status,
            credit_status,
            court_status,
            watchlist_status,
            deepfake_status,
            overall_status,
            risk_level
        FROM candidate_verification_summary
        WHERE candidate_id=%s
        LIMIT 1
        """

        cursor.execute(query, (candidate_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result

    # Method 1: Added get_report_by_candidate
    @staticmethod
    def get_report_by_candidate(candidate_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM bgv_reports
        WHERE candidate_id = %s
        LIMIT 1
        """

        cursor.execute(query, (candidate_id,))
        report = cursor.fetchone()
        cursor.close()
        connection.close()
        return report

    @staticmethod
    def save_report_details(report_data):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO bgv_reports (
            candidate_id,
            report_reference_id,
            report_name,
            report_type,
            report_status,
            verification_status,
            file_name,
            file_path,
            file_url,
            storage_provider
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            report_data["candidate_id"],
            report_data["report_reference_id"],
            report_data["report_name"],
            report_data["report_type"],
            report_data["report_status"],
            report_data["verification_status"],
            report_data["file_name"],
            report_data["file_path"],
            report_data["file_url"],
            report_data["storage_provider"],
        )

        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()

    # Method 2: Added update_report_details below save_report_details
    @staticmethod
    def update_report_details(report_data):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        UPDATE bgv_reports
        SET
            report_name=%s,
            report_type=%s,
            report_status=%s,
            verification_status=%s,
            file_name=%s,
            file_path=%s,
            file_url=%s,
            storage_provider=%s
        WHERE candidate_id=%s
        """

        values = (
            report_data["report_name"],
            report_data["report_type"],
            report_data["report_status"],
            report_data["verification_status"],
            report_data["file_name"],
            report_data["file_path"],
            report_data["file_url"],
            report_data["storage_provider"],
            report_data["candidate_id"],
        )

        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
