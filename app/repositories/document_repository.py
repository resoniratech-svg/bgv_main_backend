from app.database import connection
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


    @staticmethod
    def get_candidate_documents(candidate_id):

        connection = get_connection()

        cursor = connection.cursor()
        query = """
        SELECT
            id,
            document_type,
            original_filename,
            stored_filename,
            file_path,
            upload_status
        FROM candidate_uploaded_documents
        WHERE candidate_id = %s
        """

        print("CANDIDATE ID:", candidate_id)

        cursor.execute(
            query,
            (candidate_id,)
        )

        rows = cursor.fetchall()

        print("RAW ROWS:", rows)

        documents = []

        for row in rows:

            documents.append({

                "id": row["id"],

                "document_type": row["document_type"],

                "original_filename": row["original_filename"],

                "stored_filename": row["stored_filename"],

                "file_path": row["file_path"],

                "upload_status": row["upload_status"]

            })

        print("DOCUMENTS:", documents)

        cursor.close()
        connection.close()

        return documents
    
    @staticmethod
    def get_document_by_id(document_id):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        SELECT
            id,
            file_path,
            original_filename
        FROM candidate_uploaded_documents
        WHERE id = %s
        """

        cursor.execute(
            query,
            (document_id,)
        )

        document = cursor.fetchone()

        cursor.close()
        connection.close()

        return document