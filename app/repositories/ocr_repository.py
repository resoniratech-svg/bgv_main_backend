from app.database.connection import get_connection
import json


class OCRRepository:

    @staticmethod
    def create_ocr_result(
        verification_result_id,
        document_type,
        extracted_text,
        extracted_json,
        confidence_score=100,
        remarks="OCR Extraction Completed"
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO ocr_results
        (
            verification_result_id,
            document_type,
            extracted_text,
            extracted_json,
            confidence_score,
            remarks
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """

        values = (
            verification_result_id,
            document_type,
            extracted_text,
            json.dumps(extracted_json),
            confidence_score,
            remarks
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        ocr_result_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return ocr_result_id