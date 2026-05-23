from flask import Blueprint, request, jsonify
from app.services.ai_service_connector import AIServiceConnector

ocr_bp = Blueprint("ocr_bp", __name__)


@ocr_bp.route("/ocr", methods=["POST"])
def process_ocr():

    try:
        token = request.headers.get("Authorization")

        file = request.files.get("file")

        candidate_id = request.form.get("candidate_id")
        document_type = request.form.get("document_type")

        if not file:
            return jsonify({
                "status": "error",
                "message": "File is required"
            }), 400

        file_path = f"uploads/{file.filename}"

        file.save(file_path)

        result = AIServiceConnector.process_ocr(
            file_path=file_path,
            candidate_id=candidate_id,
            document_type=document_type,
            token=token
        )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500