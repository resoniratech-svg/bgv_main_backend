from app.database import connection
from app.database.connection import get_connection


class CandidateVerificationSummaryRepository:
    @staticmethod
    def get_fraud_cases():

        connection = get_connection()

        cursor = connection.cursor()

        status_columns = [
            ("aadhaar_status", "Aadhaar Verification"),
            ("pan_status", "PAN Verification"),
            ("passport_status", "Passport Verification"),
            ("face_match_status", "Face Match"),
            ("resume_status", "Resume Parsing"),
            ("education_status", "Education Verification"),
            ("employment_status", "Employment Verification"),
            ("credit_status", "Credit Check"),
            ("court_status", "Court Records Check"),
            ("watchlist_status", "Watchlist Screening"),
            ("dl_status", "Driving License Verification"),
            ("deepfake_status", "Deepfake Detection"),
            ("salary_slip_status", "Salary Slip Verification"),
        ]

        queries = []

        for column, module in status_columns:
            queries.append(f"""

            SELECT

            candidate_id,
            candidate_name,

            '{module}' AS module,

            COALESCE(risk_level,'HIGH') AS risk_level,

            UPPER({column}) AS status

            FROM candidate_verification_summary

            WHERE

            {column} IS NOT NULL

            AND UPPER({column}) NOT IN (

            'VERIFIED',
            'PENDING_REVIEW'

            )

            """)

        final_query = " UNION ALL ".join(queries)

        cursor.execute(final_query)

        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return rows

    @staticmethod
    def create_or_update_module_status(
        candidate_id, candidate_name, email, phone, column_name, status, risk_level=None
    ):

        connection = get_connection()

        cursor = connection.cursor()

        check_query = """
        SELECT id
        FROM candidate_verification_summary
        WHERE candidate_id = %s
        """

        cursor.execute(check_query, (candidate_id,))

        existing = cursor.fetchone()

        if existing:
            query = f"""
            UPDATE candidate_verification_summary
            SET
                {column_name} = %s,
                risk_level = %s,
                updated_at = NOW()
            WHERE candidate_id = %s
            """

            cursor.execute(query, (status, risk_level, candidate_id))

        else:
            query = f"""
            INSERT INTO
            candidate_verification_summary (

                candidate_id,
                candidate_name,
                email,
                phone,
                {column_name},
                risk_level

            )

            VALUES (

                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """

            cursor.execute(
                query, (candidate_id, candidate_name, email, phone, status, risk_level)
            )

        connection.commit()

        cursor.close()

        connection.close()

        return {"success": True}

    @staticmethod
    def get_candidate_summary(candidate_id):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        SELECT *
        FROM candidate_verification_summary
        WHERE candidate_id = %s
        """

        cursor.execute(query, (candidate_id,))

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return result

    @staticmethod
    def get_pending_candidates(column_name):

        connection = get_connection()

        cursor = connection.cursor()

        query = f"""
        SELECT

            c.id AS candidate_id,

            CONCAT(
                c.first_name,
                ' ',
                COALESCE(
                    c.last_name,
                    ''
                )
            ) AS candidate_name,

            c.email,

            c.phone,

            cvs.{column_name}

        FROM candidates c

        LEFT JOIN
            candidate_verification_summary cvs

        ON
            c.id = cvs.candidate_id

        WHERE

            c.status IN (
                'DOCUMENTS_SUBMITTED',
                'UNDER_VERIFICATION'
            )

            AND (

                cvs.{column_name} IS NULL

                OR

                cvs.{column_name} = 'PENDING_REVIEW'

            )

            AND c.is_deleted = 0
        """

        cursor.execute(query)

        results = cursor.fetchall()

        cursor.close()

        connection.close()

        return results

    @staticmethod
    def get_module_statistics(column_name):

        connection = get_connection()
        cursor = connection.cursor()

        query = f"""
        SELECT

COUNT(DISTINCT c.id) AS total,

SUM(
    CASE
        WHEN cvs.{column_name} = 'Verified'
        THEN 1
        ELSE 0
    END
) AS verified,

SUM(
    CASE
        WHEN cvs.{column_name} IS NULL
          OR cvs.{column_name} = 'PENDING_REVIEW'
        THEN 1
        ELSE 0
    END
) AS pending,

SUM(
    CASE
        WHEN cvs.{column_name} = 'Fraud'
        THEN 1
        ELSE 0
    END
) AS fraud

FROM candidates c

LEFT JOIN candidate_verification_summary cvs
ON c.id = cvs.candidate_id

WHERE
    c.status IN (
        'DOCUMENTS_SUBMITTED',
        'UNDER_VERIFICATION'
    )
    AND c.is_deleted = 0
        """

        cursor.execute(query)

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result

    @staticmethod
    def get_candidates_by_status(column_name, status):

        connection = get_connection()
        cursor = connection.cursor()

        if status == "PENDING_REVIEW":
            query = f"""
            SELECT

                c.id AS candidate_id,

                CONCAT(
                    c.first_name,
                    ' ',
                    COALESCE(
                        c.last_name,
                        ''
                    )
                ) AS candidate_name,

                c.email,

                c.phone,

                COALESCE(
                    cvs.{column_name},
                    'PENDING_REVIEW'
                ) AS status,

                cvs.risk_level

            FROM candidates c

            LEFT JOIN
                candidate_verification_summary cvs

            ON
                c.id = cvs.candidate_id

            WHERE

                (
                    cvs.{column_name} IS NULL
                    OR
                    cvs.{column_name} = 'PENDING_REVIEW'
                )

                AND c.status IN (
                    'DOCUMENTS_SUBMITTED',
                    'UNDER_VERIFICATION'
                )

                AND c.is_deleted = 0
            """

            cursor.execute(query)

        else:
            query = f"""
            SELECT

                c.id AS candidate_id,

                CONCAT(
                    c.first_name,
                    ' ',
                    COALESCE(
                        c.last_name,
                        ''
                    )
                ) AS candidate_name,

                c.email,

                c.phone,

                cvs.{column_name} AS status,

                cvs.risk_level

            FROM candidates c

            INNER JOIN
                candidate_verification_summary cvs

            ON
                c.id = cvs.candidate_id

            WHERE

                cvs.{column_name} = %s

                AND c.is_deleted = 0
            """

            cursor.execute(query, (status,))

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return results

    @staticmethod
    def get_dashboard_summary():

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT

            COUNT(DISTINCT c.id) AS total_candidates,

            SUM(
                CASE
                    WHEN cvs.overall_status = 'VERIFIED'
                    THEN 1
                    ELSE 0
                END
            ) AS verified,
            SUM(
                CASE
                    WHEN DATE(cvs.updated_at) = CURDATE()
                    AND cvs.overall_status = 'VERIFIED'
                    THEN 1
                    ELSE 0
                END
            ) AS completed_today,
            SUM(
                CASE
                    WHEN c.status IN (
                        'DOCUMENTS_SUBMITTED',
                        'UNDER_VERIFICATION'
                    )
                    THEN 1
                    ELSE 0
                END
            ) AS pending,

            SUM(
                CASE
                    WHEN cvs.risk_level = 'HIGH'
                    THEN 1
                    ELSE 0
                END
            ) AS high_risk,

            SUM(
                CASE
                    WHEN cvs.risk_level = 'MEDIUM'
                    THEN 1
                    ELSE 0
                END
            ) AS medium_risk,

            SUM(
                CASE
                    WHEN cvs.risk_level = 'LOW'
                    THEN 1
                    ELSE 0
                END
            ) AS low_risk

            

        FROM candidates c

        LEFT JOIN candidate_verification_summary cvs
            ON c.id = cvs.candidate_id

        WHERE c.is_deleted = 0
        """

        cursor.execute(query)

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        # Safe parsing with defaults handles standard cursor index offsets safely
        if result is None:
            return {
                "total_candidates": 0,
                "verified": 0,
                "completed_today": 0,
                "pending": 0,
                "high_risk": 0,
                "medium_risk": 0,
                "low_risk": 0,
            }

        return {
            "total_candidates": result.get("total_candidates", 0),
            "verified": result.get("verified", 0),
            "completed_today": result.get("completed_today", 0),
            "pending": result.get("pending", 0),
            "high_risk": result.get("high_risk", 0),
            "medium_risk": result.get("medium_risk", 0),
            "low_risk": result.get("low_risk", 0),
        }

    @staticmethod
    def get_overall_status(candidate_id):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        SELECT overall_status
        FROM candidate_verification_summary
        WHERE candidate_id = %s
        """

        cursor.execute(query, (candidate_id,))

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result

    @staticmethod
    def get_case(candidate_id):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        SELECT *
        FROM candidate_verification_summary
        WHERE candidate_id = %s
        """

        cursor.execute(query, (candidate_id,))

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result

    @staticmethod
    def approve_case(candidate_id, module):

        connection = get_connection()

        cursor = connection.cursor()

        module_map = {
            "Aadhaar Verification": "aadhaar_status",
            "PAN Verification": "pan_status",
            "Passport Verification": "passport_status",
            "Face Match": "face_match_status",
            "Resume Parsing": "resume_status",
            "Education Verification": "education_status",
            "Employment Verification": "employment_status",
            "Credit Check": "credit_status",
            "Court Records Check": "court_status",
            "Watchlist Screening": "watchlist_status",
            "Driving License Verification": "dl_status",
            "Deepfake Detection": "deepfake_status",
            "Salary Slip Verification": "salary_slip_status",
        }

        column = module_map.get(module)

        if not column:
            return False

        query = f"""

        UPDATE candidate_verification_summary

        SET

            {column} = 'VERIFIED',

            updated_at = NOW()

        WHERE

            candidate_id = %s

        """

        cursor.execute(query, (candidate_id,))

        connection.commit()

        cursor.close()

        connection.close()

        return True

    @staticmethod
    def reject_case(candidate_id, module):

        connection = get_connection()

        cursor = connection.cursor()

        module_map = {
            "Aadhaar Verification": "aadhaar_status",
            "PAN Verification": "pan_status",
            "Passport Verification": "passport_status",
            "Face Match": "face_match_status",
            "Resume Parsing": "resume_status",
            "Education Verification": "education_status",
            "Employment Verification": "employment_status",
            "Credit Check": "credit_status",
            "Court Records Check": "court_status",
            "Watchlist Screening": "watchlist_status",
            "Driving License Verification": "dl_status",
            "Deepfake Detection": "deepfake_status",
            "Salary Slip Verification": "salary_slip_status",
        }

        column = module_map.get(module)

        if not column:
            return False

        query = f"""

        UPDATE candidate_verification_summary


        SET


            {column}='REJECTED',


            updated_at=NOW()


        WHERE


            candidate_id=%s


        """

        cursor.execute(query, (candidate_id,))

        connection.commit()

        cursor.close()

        connection.close()

        return True

    @staticmethod
    def request_reverification(candidate_id, module):

        connection = get_connection()

        cursor = connection.cursor()

        module_map = {
            "Aadhaar Verification": "aadhaar_status",
            "PAN Verification": "pan_status",
            "Passport Verification": "passport_status",
            "Face Match": "face_match_status",
            "Resume Parsing": "resume_status",
            "Education Verification": "education_status",
            "Employment Verification": "employment_status",
            "Credit Check": "credit_status",
            "Court Records Check": "court_status",
            "Watchlist Screening": "watchlist_status",
            "Driving License Verification": "dl_status",
            "Deepfake Detection": "deepfake_status",
            "Salary Slip Verification": "salary_slip_status",
        }

        column = module_map.get(module)

        if not column:
            return False

        query = f"""

        UPDATE candidate_verification_summary


        SET


            {column}='PENDING_REVIEW',


            updated_at=NOW()


        WHERE


            candidate_id=%s


        """

        cursor.execute(query, (candidate_id,))

        connection.commit()

        cursor.close()

        connection.close()

        return True

    @staticmethod
    def get_by_candidate_id(candidate_id):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        SELECT *
        FROM candidate_verification_summary
        WHERE candidate_id = %s
        LIMIT 1
        """

        cursor.execute(query, (candidate_id,))

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result
