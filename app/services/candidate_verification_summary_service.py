from app.repositories.candidate_verification_summary_repository import (
    CandidateVerificationSummaryRepository
)

from app.repositories.candidate_repository import (
    CandidateRepository
)


class CandidateVerificationSummaryService:

    @staticmethod
    def update_module_status(

        candidate_id,
        module_name,
        status,
        risk_level=None

    ):

        candidate = (
            CandidateRepository.get_candidate_by_id(
                candidate_id
            )
        )

        if not candidate:

            return {
                "success": False,
                "message": "Candidate not found"
            }

        module_column_map = {

            "Aadhaar":
                "aadhaar_status",

            "PAN":
                "pan_status",

            "Passport":
                "passport_status",

            "Face Match":
                "face_match_status",

            "Resume Parsing":
                "resume_status",

            "Education":
                "education_status",

            "Employment":
                "employment_status",

            "Credit Bureau":
                "credit_status",

            "Court Record":
                "court_status",

            "Watchlist":
                "watchlist_status"
        }

        column_name = (
            module_column_map.get(
                module_name
            )
        )

        if not column_name:

            return {
                "success": False,
                "message": "Invalid module"
            }

        return (
            CandidateVerificationSummaryRepository
            .create_or_update_module_status(

                candidate_id=
                candidate_id,

                candidate_name=
                candidate["full_name"],

                email=
                candidate["email"],

                phone=
                candidate["phone"],

                column_name=
                column_name,

                status=
                status,

                risk_level=
                risk_level
            )
        )

    @staticmethod
    def get_candidate_summary(
        candidate_id
    ):

        return (
            CandidateVerificationSummaryRepository
            .get_candidate_summary(
                candidate_id
            )
        )
    
    @staticmethod
    def get_pending_candidates(module_name):

        column_mapping = {

            "aadhaar": "aadhaar_status",
            "pan": "pan_status",
            "passport": "passport_status",
            "dl": "dl_status",
            "face-match": "face_match_status",

            "deepfake": "deepfake_status",
            "resume": "resume_status",

            "education": "education_status",
            "employment": "employment_status",

            "salary-slip": "salary_slip_status",

            "credit": "credit_status",
            "court": "court_status",
            "watchlist": "watchlist_status"
        }

        column_name = column_mapping.get(
            module_name
        )

        if not column_name:

            raise Exception(
                f"Invalid module: {module_name}"
            )

        return (
            CandidateVerificationSummaryRepository
            .get_pending_candidates(
                column_name
            )
        )
    
    @staticmethod
    def get_module_statistics(module_name):

        column_mapping = {

            "aadhaar": "aadhaar_status",
            "pan": "pan_status",
            "passport": "passport_status",
            "dl": "dl_status",
            "face-match": "face_match_status",

            "deepfake": "deepfake_status",
            "resume": "resume_status",

            "education": "education_status",
            "employment": "employment_status",

            "salary-slip": "salary_slip_status",

            "credit": "credit_status",
            "court": "court_status",
            "watchlist": "watchlist_status"
        }

        column_name = column_mapping.get(
            module_name
        )

        if not column_name:

            raise Exception(
                f"Invalid module: {module_name}"
            )

        return (
            CandidateVerificationSummaryRepository
            .get_module_statistics(
                column_name
            )
        )
    
    
    @staticmethod
    def get_candidates_by_status(
            module_name,
            status
        ):

            column_mapping = {

                "aadhaar": "aadhaar_status",
                "pan": "pan_status",
                "passport": "passport_status",
                "dl": "dl_status",
                "face-match": "face_match_status",

                "deepfake": "deepfake_status",
                "resume": "resume_status",

                "education": "education_status",
                "employment": "employment_status",

                "salary-slip": "salary_slip_status",

                "credit": "credit_status",
                "court": "court_status",
                "watchlist": "watchlist_status"
            }

            column_name = column_mapping.get(
                module_name
            )

            if not column_name:

                raise Exception(
                    f"Invalid module: {module_name}"
                )

            return (
                CandidateVerificationSummaryRepository
                .get_candidates_by_status(
                    column_name,
                    status
                )
            )