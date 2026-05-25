from app.database.connection import get_connection


class DocumentRepository:

    @staticmethod
    def save_uploaded_document(data):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO candidate_uploaded_documents (

            candidate_id,
            bgv_id,
            access_link_id,
            document_type,
            original_filename,
            stored_filename,
            file_path,
            mime_type,
            file_size,
            upload_status

        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (

            data.get("candidate_id"),
            data.get("bgv_id"),
            data.get("access_link_id"),
            data.get("document_type"),
            data.get("original_filename"),
            data.get("stored_filename"),
            data.get("file_path"),
            data.get("mime_type"),
            data.get("file_size"),
            "UPLOADED"

        )

        cursor.execute(query, values)

        connection.commit()

        document_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return {
            "document_id": document_id
        }