from app.database.connection import get_connection


class NotificationRepository:
    @staticmethod
    def create_notification(data):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO notifications
        (
            candidate_id,
            bgv_id,
            title,
            description,
            type
        )
        VALUES (%s,%s,%s,%s,%s)
        """

        cursor.execute(
            query,
            (
                data.get("candidate_id"),
                data.get("bgv_id"),
                data.get("title"),
                data.get("description"),
                data.get("type"),
            ),
        )

        connection.commit()

        notification_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return notification_id

    @staticmethod
    def get_notifications():

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT *
        FROM notifications
        ORDER BY created_at DESC
        """

        cursor.execute(query)

        notifications = cursor.fetchall()

        cursor.close()
        connection.close()

        return notifications

    @staticmethod
    def mark_as_read(notification_id):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        UPDATE notifications
        SET is_read = TRUE
        WHERE id = %s
        """

        cursor.execute(query, (notification_id,))

        connection.commit()

        cursor.close()
        connection.close()

        return {"status": "success"}

    @staticmethod
    def mark_all_as_read():

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        UPDATE notifications
        SET is_read = TRUE
        WHERE is_read = FALSE
        """

        cursor.execute(query)

        connection.commit()

        cursor.close()
        connection.close()

        return {"status": "success"}
