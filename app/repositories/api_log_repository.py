from app.database.connection import get_connection
import json


class APILogRepository:

    @staticmethod
    def create_api_log(
        module_name,
        provider_name,
        endpoint,
        request_payload,
        response_payload,
        response_status_code,
        response_time_ms,
        status,
        error_message=None
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO api_logs (
            module_name,
            provider_name,
            endpoint,
            request_payload,
            response_payload,
            response_status_code,
            response_time_ms,
            status,
            error_message
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            module_name,
            provider_name,
            endpoint,
            json.dumps(request_payload),
            json.dumps(response_payload),
            response_status_code,
            response_time_ms,
            status,
            error_message
        )

        cursor.execute(query, values)

        connection.commit()

        api_log_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return api_log_id