# from app.services.ai_service_connector import AIServiceConnector


# class AadhaarService:
#     @staticmethod
#     def generate_qr(candidate_id, bgv_id, token):
#         return AIServiceConnector.generate_aadhaar_qr(
#             candidate_id=candidate_id, bgv_id=bgv_id, token=token
#         )

#     @staticmethod
#     def get_status(candidate_id, token=None):

#         return AIServiceConnector.get_aadhaar_status(candidate_id, token)

#     @staticmethod
#     def get_result(candidate_id, token):
#         return AIServiceConnector.get_aadhaar_result(
#             candidate_id=candidate_id, token=token
#         )

#     @staticmethod
#     def verify_aadhaar(candidate_id, bgv_id, document_id, token):
#         return AIServiceConnector.verify_aadhaar(
#             candidate_id=candidate_id,
#             bgv_id=bgv_id,
#             document_id=document_id,
#             token=token,
#         )
# from app.services.ai_service_connector import AIServiceConnector


# class AadhaarService:
#     """
#     Aadhaar Service (SDK Flow)

#     Flow:
#     Candidate Portal
#             ↓
#     create_session()
#             ↓
#     AI Service → Gridlines SDK Session
#             ↓
#     aadhaar_verification_sessions

#     SDK Success
#             ↓
#     fetch_result()
#             ↓
#     aadhaar_verification_results
#     """

#     #     @staticmethod
#     #     def create_session(secure_token, token):
#     #         """
#     #         Create a new Aadhaar SDK verification session.
#     #         """
#     #         return AIServiceConnector.create_aadhaar_session(
#     #             secure_token=secure_token,
#     #             token=token,
#     #         )

#     @staticmethod
#     def fetch_result(secure_token, token):
#         """
#         Fetch Aadhaar verification result from our database.
#         """
#         return AIServiceConnector.fetch_aadhaar_result(
#             secure_token=secure_token,
#             token=token,
#         )


from app.services.ai_service_connector import AIServiceConnector


class AadhaarService:
    # ======================================================
    # SAVE AADHAAR RESULT
    # ======================================================

    @staticmethod
    def save_result(
        candidate_id,
        bgv_id,
        aadhaar_data,
    ):
        """
        Save successful Gridlines Aadhaar SDK result
        through the AI service and update the main
        candidate verification summary.
        """

        # ==================================================
        # STEP 1
        # SAVE ACTUAL AADHAAR RESULT
        # ==================================================

        result = AIServiceConnector.save_aadhaar_result(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            aadhaar_data=aadhaar_data,
        )

        # ==================================================
        # CHECK AI SERVICE RESULT
        # ==================================================

        if not result or not result.get("success"):
            return result

        # ==================================================
        # STEP 2
        # UPDATE CANDIDATE VERIFICATION SUMMARY
        # ==================================================

        from app.services.candidate_verification_summary_service import (
            CandidateVerificationSummaryService,
        )

        summary_result = CandidateVerificationSummaryService.update_module_status(
            candidate_id=candidate_id,
            module_name="Aadhaar",
            status="PENDING_REVIEW",
            risk_level=None,
        )

        if not summary_result.get("success", False):
            return {
                "success": False,
                "message": (
                    "Aadhaar result was saved, but candidate "
                    "verification summary could not be updated"
                ),
                "aadhaar_result": result,
                "summary_result": summary_result,
            }

        # ==================================================
        # STEP 3
        # AUDIT LOG
        # ==================================================

        from app.services.audit_service import AuditService

        AuditService.log_action(
            action="AADHAAR_VERIFICATION_COMPLETED",
            module_name="Aadhaar",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks=(
                "Aadhaar verification completed successfully "
                "through Gridlines and moved to pending review"
            ),
            old_values={
                "aadhaar_status": None,
            },
            new_values={
                "aadhaar_status": "PENDING_REVIEW",
                "bgv_id": bgv_id,
            },
        )

        # ==================================================
        # FINAL RESPONSE
        # ==================================================

        return {
            "success": True,
            "message": "Aadhaar verification result saved successfully",
            "verification_result_id": result.get("verification_result_id"),
            "verification_status": result.get(
                "verification_status",
                "VERIFIED",
            ),
            "summary_status": "PENDING_REVIEW",
        }

    # ======================================================
    # GET AADHAAR RESULT
    # ======================================================

    @staticmethod
    def get_result(candidate_id, token=None):
        """
        Fetch Aadhaar verification result from AI service.
        """

        return AIServiceConnector.get_aadhaar_result(
            candidate_id=candidate_id,
            token=token,
        )

    # ======================================================
    # SAVE AADHAAR DECISION
    # ======================================================

    @staticmethod
    def save_decision(data):

        from app.repositories.candidate_verification_summary_repository import (
            CandidateVerificationSummaryRepository,
        )

        from app.services.candidate_verification_summary_service import (
            CandidateVerificationSummaryService,
        )

        from app.services.audit_service import AuditService

        from app.services.notification_service import NotificationService

        # ==================================================
        # GET REQUEST DATA
        # ==================================================

        candidate_id = data.get("candidate_id")
        decision = data.get("decision")

        # ==================================================
        # VALIDATE CANDIDATE
        # ==================================================

        if not candidate_id:
            return {
                "status": "error",
                "message": "candidate_id is required",
            }

        # ==================================================
        # VALIDATE DECISION
        # ==================================================

        if not decision:
            return {
                "status": "error",
                "message": "decision is required",
            }

        # ==================================================
        # ALLOWED DECISIONS
        # ==================================================

        allowed_decisions = [
            "Verified",
            "Not Verified",
            "Fraud",
            "Rejected",
        ]

        if decision not in allowed_decisions:
            return {
                "status": "error",
                "message": "Invalid Aadhaar decision",
            }

        # ==================================================
        # GET EXISTING SUMMARY
        # ==================================================

        summary = CandidateVerificationSummaryRepository.get_by_candidate_id(
            candidate_id
        )

        old_decision = None

        if summary:
            old_decision = summary.get("aadhaar_status")

        # ==================================================
        # UPDATE AADHAAR DECISION
        # ==================================================

        result = CandidateVerificationSummaryService.update_module_status(
            candidate_id=candidate_id,
            module_name="Aadhaar",
            status=decision,
        )

        if not result.get("success", True):
            return result

        # ==================================================
        # NOTIFICATION
        # ==================================================

        if decision == "Verified":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Aadhaar Verified",
                description=("Aadhaar verification has been verified by the reviewer."),
                notification_type="Success",
            )

        elif decision == "Not Verified":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Aadhaar Not Verified",
                description=(
                    "Aadhaar verification has been marked as not verified "
                    "by the reviewer."
                ),
                notification_type="Warning",
            )

        elif decision == "Fraud":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Aadhaar Fraud Detected",
                description=(
                    "Aadhaar verification has been marked as fraudulent "
                    "by the reviewer."
                ),
                notification_type="Critical",
            )

        elif decision == "Rejected":
            NotificationService.create_notification(
                candidate_id=candidate_id,
                title="Aadhaar Rejected",
                description=("Aadhaar verification has been rejected by the reviewer."),
                notification_type="Warning",
            )

        # ==================================================
        # AUDIT LOG
        # ==================================================

        AuditService.log_action(
            action="AADHAAR_DECISION",
            module_name="Aadhaar",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks=f"Aadhaar decision updated to {decision}",
            old_values={
                "decision": old_decision,
            },
            new_values={
                "decision": decision,
            },
        )

        # ==================================================
        # RESPONSE
        # ==================================================

        return {
            "status": "success",
            "message": "Aadhaar decision saved",
        }
