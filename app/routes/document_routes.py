from flask import Blueprint, request, jsonify, send_file
from flask import send_file, jsonify
import os
from app.database.connection import get_connection
from app.services.document_service import (
    DocumentService
)

document_bp = Blueprint(
    "document_bp",
    __name__
)


@document_bp.route(
    "/candidate/upload-document",
    methods=["POST"]
)
def upload_document():
    print("DOCUMENT ROUTE HIT")
    try:

        secure_token = request.form.get(
            "secure_token"
        )

        document_type = request.form.get(
            "document_type"
        )

        file = request.files.get("file")

        result = (
            DocumentService.upload_document(
                secure_token,
                document_type,
                file
            )
        )

        if result["status"] == "error":

            return jsonify(result), 400

        return jsonify(result), 201

    except Exception as e:
        import traceback
        traceback.print_exc()

        import traceback
        traceback.print_exc()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@document_bp.route(
    "/documents/<int:document_id>/view",
    methods=["GET"]
)
def view_document(document_id):
    print("######## VIEW DOCUMENT ROUTE HIT ########")
    try:

        from app.repositories.document_repository import (
            DocumentRepository
        )

        document = (
            DocumentRepository.get_document_by_id(
                document_id
            )
        )

        if not document:

            return jsonify({
                "status": "error",
                "message": "Document not found"
            }), 404

        project_root = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "../.."
            )
        )

        full_path = os.path.join(
            project_root,
            document["file_path"]
        )

        print("FULL PATH:", full_path)
        print("FILE EXISTS:", os.path.exists(full_path))

        if not os.path.exists(full_path):

            return jsonify({
                "status": "error",
                "message": f"File not found: {full_path}"
            }), 404

        return send_file(
            full_path,
            as_attachment=False
        )

    except Exception as e:

        import traceback
        traceback.print_exc()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
@staticmethod
def get_document_by_id(document_id):

    connection = get_connection()

    cursor = connection.cursor()

    query = """
    SELECT
        id,
        file_path
    FROM candidate_uploaded_documents
    WHERE id = %s
    """

    cursor.execute(
        query,
        (document_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if not row:

        return None

    return {
        "id": row[0],
        "file_path": row[1]
    }
