from app.database import connection
from app.database.connection import get_connection


class CandidateVerificationSummaryRepository:

    @staticmethod
    def create_or_update_module_status(

        candidate_id,
        candidate_name,
        email,
        phone,
        column_name,
        status,
        risk_level=None

    ):

        connection = get_connection()

        cursor = connection.cursor()

        check_query = """
        SELECT id
        FROM candidate_verification_summary
        WHERE candidate_id = %s
        """

        cursor.execute(
            check_query,
            (candidate_id,)
        )

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

            cursor.execute(

                query,

                (
                    status,
                    risk_level,
                    candidate_id
                )
            )

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

                query,

                (
                    candidate_id,
                    candidate_name,
                    email,
                    phone,
                    status,
                    risk_level
                )
            )

        connection.commit()

        cursor.close()

        connection.close()

        return {
            "success": True
        }

    @staticmethod
    def get_candidate_summary(

        candidate_id
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        SELECT *
        FROM candidate_verification_summary
        WHERE candidate_id = %s
        """

        cursor.execute(
            query,
            (candidate_id,)
        )

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

            c.status = 'DOCUMENTS_SUBMITTED'

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
    c.status = 'DOCUMENTS_SUBMITTED'
    AND c.is_deleted = 0
        """

        cursor.execute(query)

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result
    
    @staticmethod
    def get_candidates_by_status(
        column_name,
        status
    ):

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

                AND c.status = 'DOCUMENTS_SUBMITTED'

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

            cursor.execute(
                query,
                (status,)
            )

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

        return {
            "total_candidates": result["total_candidates"] or 0,
            "verified": result["verified"] or 0,
            "pending": result["pending"] or 0,
            "high_risk": result["high_risk"] or 0,
            "medium_risk": result["medium_risk"] or 0,
            "low_risk": result["low_risk"] or 0,
            "completed_today": result["completed_today"] or 0,
        }