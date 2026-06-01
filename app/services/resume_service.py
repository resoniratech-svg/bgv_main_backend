# class ResumeService:
#     @staticmethod
#     def verify(data):
#         return {
#             "status":"success",
#             "verification_status":"Verified",
#             "module":"Resume",
#             "data":data
#         }


import os

from app.repositories.document_repository import (
    DocumentRepository
)
from app.repositories.resume_repository import (
    ResumeRepository
)
from app.services.ai_service_connector import (
    AIServiceConnector
)


class ResumeService:

    @staticmethod
    def parse_resume(candidate_id):

        resume_document = (
            DocumentRepository.get_resume_document(
                candidate_id
            )
        )

        if not resume_document:

            return {
                "status": "error",
                "message": "Resume not uploaded"
            }

        project_root = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "../.."
            )
        )

        full_path = os.path.join(
            project_root,
            resume_document["file_path"]
        )

        if not os.path.exists(full_path):

            return {
                "status": "error",
                "message": "Resume file not found"
            }

        result = (
            AIServiceConnector.parse_resume(
                full_path,
                candidate_id
            )
        )

        return {
            "status": "success",
            "candidate_id": candidate_id,
            "resume_data": result
        }
    @staticmethod
    def get_parsed_resume(candidate_id):

        result = (
            ResumeRepository.get_parsed_resume(
                candidate_id
            )
        )

        if not result:

            return {
                "status": "error",
                "message": "No parsed resume found"
            }

        return {
            "status": "success",
            "data": result
        }