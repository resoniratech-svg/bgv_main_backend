from flask import Blueprint, request, jsonify

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

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500