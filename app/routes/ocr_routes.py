from flask import Blueprint, request, jsonify
from app.services.ai_service_connector import AIServiceConnector
import traceback

ocr_bp = Blueprint("ocr_bp", __name__)


@ocr_bp.route("/ocr", methods=["POST"])
def process_ocr():

    try:

        print("========== OCR API HIT ==========")

        token = request.headers.get("Authorization")
        file = request.files.get("file")

        candidate_id = request.form.get("candidate_id")
        document_type = request.form.get("document_type")

        print("TOKEN:", token)
        print("CANDIDATE ID:", candidate_id)
        print("DOCUMENT TYPE:", document_type)
        print("FILE:", file)

        if not file:

            return jsonify({
                "status": "error",
                "message": "File is required"
            }), 400

        file_path = f"uploads/{file.filename}"

        print("FILE PATH:", file_path)

        file.save(file_path)

        result = AIServiceConnector.process_ocr(
            file_path=file_path,
            candidate_id=candidate_id,
            document_type=document_type,
            token=token
        )

        print("OCR RESULT:", result)

        return jsonify(result), 200

    except Exception as e:

        traceback.print_exc()

        print("OCR ERROR:", str(e))

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@ocr_bp.route(
    "/ocr/document",
    methods=["POST"]
)
def process_document_ocr():

    try:

        print("========== OCR DOCUMENT API HIT ==========")

        data = request.get_json()

        document_id = data.get(
            "document_id"
        )

        candidate_id = data.get(
            "candidate_id"
        )

        print("DOCUMENT ID:", document_id)
        print("CANDIDATE ID:", candidate_id)

        from app.repositories.document_repository import (
            DocumentRepository
        )

        document = (
            DocumentRepository.get_document_by_id(
                document_id
            )
        )

        print("DOCUMENT:", document)

        if not document:

            return jsonify({
                "status": "error",
                "message": "Document not found"
            }), 404

        token = request.headers.get(
            "Authorization"
        )

        print("TOKEN:", token)

        result = (
            AIServiceConnector.process_ocr(
                file_path=document["file_path"],
                candidate_id=candidate_id,
                document_type=document.get(
                    "document_type",
                    "OCR"
                ),
                token=token
            )
        )

        from app.repositories.bgv_repository import (
            BGVRepository
        )

        bgv = (
            BGVRepository.get_bgv_by_candidate_id(
                candidate_id
            )
        )

        print("OCR RESULT:", result)
        print("BGV:", bgv)

        return jsonify(result), 200

    except Exception as e:

        traceback.print_exc()

        print("OCR DOCUMENT ERROR:", str(e))

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500