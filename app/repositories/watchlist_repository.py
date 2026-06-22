from app.database.connection import get_connection


class WatchlistRepository:

    @staticmethod
    def get_by_candidate_id(candidate_id):

        connection = get_connection()

        cursor = connection.cursor()

        # Updated to point to the correct table
        query = """
            SELECT *
            FROM global_watchlist_results
            WHERE candidate_id = %s
            ORDER BY id DESC
            LIMIT 1
        """

        cursor.execute(
            query,
            (candidate_id,)
        )

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result