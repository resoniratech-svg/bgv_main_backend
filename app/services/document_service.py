import os
import uuid
from app.repositories.document_repository import (
    DocumentRepository
)
from werkzeug.utils import secure_filename


from app.repositories.candidate_link_repository import (
    CandidateLinkRepository
)


class DocumentService:

    UPLOAD_FOLDER = "uploads"

    @staticmethod
    def upload_document(
        secure_token,
        document_type,
        file
    ):
        validation_result = (
            CandidateLinkRepository.validate_secure_token(
                secure_token
            )
        )

        if validation_result["status"] == "error":

            return validation_result

        candidate_data = validation_result["data"]

        if not file:

            return {
                "status": "error",
                "message": "File is required"
            }

        allowed_extensions = [
            "pdf",
            "jpg",
            "jpeg",
            "png"
        ]

        allowed_mime_types = [
            "application/pdf",
            "image/jpeg",
            "image/png"
        ]

        original_filename = secure_filename(
            file.filename
        )

        if "." not in original_filename:

            return {
                "status": "error",
                "message": "Invalid file"
            }

        extension = (
            original_filename
            .split(".")[-1]
            .lower()
        )

        if extension not in allowed_extensions:

            return {
                "status": "error",
                "message": (
                    "Unsupported file type"
                )
            }

        if file.mimetype not in allowed_mime_types:

            return {
                "status": "error",
                "message": (
                    "Invalid mime type"
                )
            }

        MAX_FILE_SIZE = 10 * 1024 * 1024

        file.seek(0, 2)

        file_size = file.tell()

        file.seek(0)

        if file_size > MAX_FILE_SIZE:
            return {
                "status": "error",
                "message": (
                    "File size exceeds 10MB"
                )
            }

        stored_filename = (
            f"{uuid.uuid4().hex}.{extension}"
        )

        os.makedirs(
            DocumentService.UPLOAD_FOLDER,
            exist_ok=True
        )

        file_path = os.path.join(
            DocumentService.UPLOAD_FOLDER,
            stored_filename
        )

        file.save(file_path)

        data = {

            "candidate_id": candidate_data["candidate_id"],

            "bgv_id": candidate_data["bgv_id"],

            "access_link_id": candidate_data["id"],

            "document_type": document_type,

            "original_filename": original_filename,

            "stored_filename": stored_filename,

            "file_path": file_path,

            "mime_type": file.mimetype,

            "file_size": os.path.getsize(file_path)
        }
        DocumentRepository.delete_existing_document(
            candidate_data["candidate_id"],
            document_type
        )

        result = (
            DocumentRepository.save_uploaded_document(
                data
            )
        )

        return {

            "status": "success",

            "message": "Document uploaded successfully",

            "data": {
                "document_id": result["document_id"],
                "stored_filename": stored_filename
            }
        }
    
    @staticmethod
    def get_candidate_documents(candidate_id):

        documents = (
            DocumentRepository.get_candidate_documents(
                candidate_id
            )
        )

        return {
            "status": "success",
            "data": documents
        }
    @staticmethod
    def get_document_file(document_id):

        return (
            DocumentRepository.get_document_by_id(
                document_id
            )
        )