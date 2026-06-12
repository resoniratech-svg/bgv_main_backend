from flask import jsonify

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

        try:

            print("GET_ALL_CANDIDATES START")

            connection = get_connection()
            print("DB CONNECTED")

            cursor = connection.cursor()
            print("CURSOR CREATED")

            query = """
            SELECT
                id,
                CONCAT(first_name, ' ', last_name) AS full_name,
                email,
                phone,
                status,
                DATE(created_at) AS created_at,
                DATE(updated_at) AS updated_at
            FROM candidates
            WHERE is_deleted = 0
            """

            cursor.execute(query)
            print("QUERY EXECUTED")

            candidates = cursor.fetchall()
            print("FETCH COMPLETE:", len(candidates))

            cursor.close()
            connection.close()

            print("GET_ALL_CANDIDATES END")

            return candidates

        except Exception as e:

            import traceback

            print("\n========== REPOSITORY ERROR ==========")
            traceback.print_exc()
            print("======================================\n")

            raise
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
            status,
            DATE(created_at) AS created_at,
            DATE(updated_at) AS updated_at
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
        SET
            status = %s,
            updated_at = NOW()
        WHERE id = %s
"""

        status = data.get("status")

        cursor.execute(
            query,
            (
                status,
                candidate_id
            )
        )

        connection.commit()
        cursor.close()
        connection.close()
        # =====================================
        # SEND EMAIL WHEN DOCUMENTS SUBMITTED
        # =====================================

        if status == "DOCUMENTS_SUBMITTED":

            try:

                from app.services.email_service import (
                    EmailService
                )

                candidate = (
                    CandidateRepository.get_candidate_by_id(
                        candidate_id
                    )
                )

                EmailService.send_admin_alert(

                    subject="Candidate Documents Submitted",

                    message=f"""
        Candidate Name: {candidate.get('full_name')}

        Candidate ID: {candidate.get('id')}

        Status: DOCUMENTS_SUBMITTED

        Candidate has uploaded documents successfully.
        Start verification process.
        """
                )

                print(
                    "DOCUMENT SUBMISSION EMAIL SENT"
                )

            except Exception as e:

                import traceback

                traceback.print_exc()

                return jsonify({
                    "status": "error",
                    "message": str(e)
                }), 500

        

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