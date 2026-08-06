import uuid
import traceback
from flask import jsonify
from app.database.connection import get_connection
from app.services.notification_service import NotificationService


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
            country,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            candidate_code,
            data.get("first_name"),
            data.get("last_name"),
            data.get("email"),
            data.get("phone"),
            data.get("country"),
            "PENDING",
        )

        cursor.execute(query, values)
        connection.commit()

        candidate_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return {"candidate_id": candidate_id, "candidate_code": candidate_code}

    @staticmethod
    def get_all_candidates():
        try:
            print("GET_ALL_CANDIDATES START")
            connection = get_connection()
            print("DB CONNECTED")

            cursor = connection.cursor()
            print("CURSOR CREATED")

            # Updated to fetch company name via left join
            query = """
            SELECT
                c.id,
                CONCAT(c.first_name, ' ', c.last_name) AS full_name,
                c.email,
                c.phone,
                br.company_name,
                br.bgv_id,
                c.status,
                DATE(c.created_at) AS created_at,
                DATE(c.updated_at) AS updated_at
            FROM candidates c
            LEFT JOIN bgv_requests br
                ON br.candidate_id = c.id
                AND br.is_deleted = 0
            WHERE c.is_deleted = 0
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
            print("\n========== REPOSITORY ERROR ==========")
            traceback.print_exc()
            print("======================================\n")
            raise

    @staticmethod
    def get_candidate_by_id(candidate_id):
        connection = get_connection()
        cursor = connection.cursor()

        # Fixed to return explicit first_name, last_name, country, and company_name
        query = """
            SELECT
                c.id,
                c.first_name,
                c.last_name,

                CONCAT(
                    c.first_name,
                    ' ',
                    c.last_name
                ) AS full_name,

                c.email,
                c.phone,

                c.date_of_birth AS dob,
                c.gender,

                c.country,

                br.company_name,
                br.bgv_id,
                c.status,

                DATE(c.created_at) AS created_at,
                DATE(c.updated_at) AS updated_at

            FROM candidates c

            LEFT JOIN bgv_requests br
                ON br.candidate_id = c.id

            WHERE c.id = %s
            LIMIT 1
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
        cursor.execute(query, (status, candidate_id))
        connection.commit()
        cursor.close()
        connection.close()

        # =====================================
        # SEND EMAIL WHEN DOCUMENTS SUBMITTED
        # =====================================
        if status == "DOCUMENTS_SUBMITTED":
            try:
                from app.services.email_service import EmailService

                candidate = CandidateRepository.get_candidate_by_id(candidate_id)
                email_sent = EmailService.send_admin_alert(
                    subject="Candidate Documents Submitted",
                    message=f"""
                Candidate Name: {candidate.get("full_name")}
                Candidate ID: {candidate.get("id")}
                Status: DOCUMENTS_SUBMITTED

                Candidate has uploaded documents successfully.
                Start verification process.
                """,
                )

                if email_sent:
                    print("DOCUMENT SUBMISSION EMAIL SENT")

                    NotificationService.create_notification(
                        candidate_id=candidate_id,
                        bgv_id=candidate.get("bgv_id"),
                        title="Admin Alert Sent",
                        description=f"Admin has been notified that {candidate.get('full_name')} submitted documents.",
                        notification_type="Info",
                    )
            #         EmailService.send_admin_alert(
            #             subject="Candidate Documents Submitted",
            #             message=f"""
            # Candidate Name: {candidate.get("full_name")}
            # Candidate ID: {candidate.get("id")}
            # Status: DOCUMENTS_SUBMITTED

            # Candidate has uploaded documents successfully.
            # Start verification process.
            # """,
            #         )
            #         print("DOCUMENT SUBMISSION EMAIL SENT")
            #         NotificationService.create_notification(
            #             candidate_id=candidate_id,
            #             bgv_id=candidate.get("bgv_id"),
            #             title="Documents Submitted",
            #             description=f"{candidate.get('full_name')} has submitted all verification documents.",
            #             notification_type="Success",
            #         )
            except Exception as e:
                traceback.print_exc()
                return jsonify({"status": "error", "message": str(e)}), 500

        return {"status": "success", "message": "Candidate status updated successfully"}

    @staticmethod
    def update_candidate(candidate_id, data):
        connection = get_connection()
        cursor = connection.cursor()

        # 1. Update candidate baseline profile data (including country)
        candidate_query = """
        UPDATE candidates
        SET
            first_name = %s,
            last_name = %s,
            email = %s,
            phone = %s,
            country = %s
        WHERE id = %s
        """

        cursor.execute(
            candidate_query,
            (
                data.get("first_name"),
                data.get("last_name"),
                data.get("email"),
                data.get("phone"),
                data.get("country"),
                candidate_id,
            ),
        )

        # 2. Update relational context inside the bgv_requests table
        bgv_query = """
        UPDATE bgv_requests
        SET company_name = %s
        WHERE candidate_id = %s
        """

        cursor.execute(bgv_query, (data.get("company_name"), candidate_id))

        connection.commit()
        cursor.close()
        connection.close()

        return {"status": "success", "message": "Candidate updated successfully"}

    @staticmethod
    def delete_candidate(candidate_id):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        UPDATE candidates
        SET
            is_deleted = 1,
            email = CONCAT(email, '_deleted_', id)
        WHERE id = %s
        """

        cursor.execute(query, (candidate_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return {"status": "success", "message": "Candidate deleted successfully"}
