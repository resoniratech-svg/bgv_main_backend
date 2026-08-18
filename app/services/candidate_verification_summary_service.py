from app.repositories.candidate_verification_summary_repository import (
    CandidateVerificationSummaryRepository,
)

from app.repositories.candidate_repository import CandidateRepository


class CandidateVerificationSummaryService:
    @staticmethod
    def update_module_status(candidate_id, module_name, status, risk_level=None):

        candidate = CandidateRepository.get_candidate_by_id(candidate_id)

        if not candidate:
            return {"success": False, "message": "Candidate not found"}

        module_column_map = {
            "Aadhaar": "aadhaar_status",
            "PAN": "pan_status",
            "Passport": "passport_status",
            "Face Match": "face_match_status",
            "Driving License": "dl_status",
            "Deepfake Detection": "deepfake_status",
            "Resume Parsing": "resume_status",
            "Education": "education_status",
            "Employment": "employment_status",
            "Salary Slip": "salary_slip_status",
            "Bank Statement": "bank_statement_status",
            "Credit Bureau": "credit_status",
            "Court Record": "court_status",
            "Watchlist": "watchlist_status",
        }

        column_name = module_column_map.get(module_name)

        if not column_name:
            return {"success": False, "message": "Invalid module"}

        result = CandidateVerificationSummaryRepository.create_or_update_module_status(
            candidate_id=candidate_id,
            candidate_name=candidate["full_name"],
            email=candidate["email"],
            phone=candidate["phone"],
            column_name=column_name,
            status=status,
            risk_level=risk_level,
        )

        # =====================================
        # MOVE CANDIDATE TO UNDER_VERIFICATION
        # WHEN ANY MODULE IS PROCESSED
        # =====================================

        if status in ["Verified", "Not Verified", "Fraud", "Rejected"]:
            CandidateRepository.update_candidate_status(
                candidate_id, {"status": "UNDER_VERIFICATION"}
            )

        # =====================================
        # CHECK OVERALL STATUS
        # =====================================

        summary = CandidateVerificationSummaryRepository.get_candidate_summary(
            candidate_id
        )

        if summary:
            overall_status = summary.get("overall_status")

            if overall_status == "VERIFIED":
                CandidateRepository.update_candidate_status(
                    candidate_id, {"status": "VERIFIED"}
                )

            elif overall_status == "FRAUD":
                CandidateRepository.update_candidate_status(
                    candidate_id, {"status": "FRAUD_ALERT"}
                )

            elif overall_status == "NOT_VERIFIED":
                CandidateRepository.update_candidate_status(
                    candidate_id, {"status": "NOT_VERIFIED"}
                )

        return result

    @staticmethod
    def get_candidate_summary(candidate_id):

        return CandidateVerificationSummaryRepository.get_candidate_summary(
            candidate_id
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
            "watchlist": "watchlist_status",
            "bank-statement": "bank_statement_status",
        }

        column_name = column_mapping.get(module_name)

        if not column_name:
            raise Exception(f"Invalid module: {module_name}")

        return CandidateVerificationSummaryRepository.get_pending_candidates(
            column_name
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
            "watchlist": "watchlist_status",
            "bank-statement": "bank_statement_status",
        }

        column_name = column_mapping.get(module_name)

        if not column_name:
            raise Exception(f"Invalid module: {module_name}")

        return CandidateVerificationSummaryRepository.get_module_statistics(column_name)

    @staticmethod
    def get_candidates_by_status(module_name, status):

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
            "watchlist": "watchlist_status",
            "bank-statement": "bank_statement_status",
        }

        column_name = column_mapping.get(module_name)

        if not column_name:
            raise Exception(f"Invalid module: {module_name}")

        return CandidateVerificationSummaryRepository.get_candidates_by_status(
            column_name, status
        )

    @staticmethod
    def initialize_candidate_summary(candidate_id):
        candidate = CandidateRepository.get_candidate_by_id(candidate_id)

        if not candidate:
            return {
                "success": False,
                "message": "Candidate not found",
            }

        existing = CandidateVerificationSummaryRepository.get_by_candidate_id(
            candidate_id
        )

        if existing:
            return {
                "success": True,
                "message": "Candidate summary already exists",
            }

        CandidateVerificationSummaryRepository.create_candidate_summary(
            candidate_id=candidate_id,
            candidate_name=candidate["full_name"],
            email=candidate["email"],
            phone=candidate["phone"],
        )

        return {
            "success": True,
            "message": "Candidate verification summary created",
        }
