from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from app.models.bgv_request import BGVRequest
from app.models.verification_result import VerificationResult
from app.models.audit_log import AuditLog
from app.extensions import db


class BGVService:

    # =====================================================
    # INTERNAL: AUDIT LOGGER
    # =====================================================
    @staticmethod
    def _log_action(bgv_id, action):
        try:
            user_id = get_jwt_identity()
        except Exception:
            user_id = None

        log = AuditLog(
            bgv_id=bgv_id,
            action=action,
            performed_by=user_id
        )

        db.session.add(log)

    # =====================================================
    # CREATE BGV
    # =====================================================
    @staticmethod
    def create_bgv_request(data):

        bgv = BGVRequest(
            candidate_name=data.get("candidate_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            verification_type=data.get("verification_type"),
            status="Pending",
            trust_score=0,
            remarks=data.get("remarks"),
            is_locked=False,
            is_deleted=False,
            final_decision=None
        )

        db.session.add(bgv)
        db.session.commit()

        return bgv

    # =====================================================
    # GET PAGINATED + FILTERS
    # =====================================================
    @staticmethod
    def get_paginated_requests(page, per_page, filters=None):

        query = BGVRequest.query.filter_by(is_deleted=False)

        if filters:
            if filters.get("status"):
                query = query.filter(
                    BGVRequest.status.ilike(f"%{filters['status']}%")
                )

            if filters.get("candidate_name"):
                query = query.filter(
                    BGVRequest.candidate_name.ilike(f"%{filters['candidate_name']}%")
                )

            if filters.get("email"):
                query = query.filter(
                    BGVRequest.email.ilike(f"%{filters['email']}%")
                )

        return query.order_by(BGVRequest.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    # =====================================================
    # GET SINGLE
    # =====================================================
    @staticmethod
    def get_request_by_id(bgv_id):
        return BGVRequest.query.filter_by(
            id=bgv_id,
            is_deleted=False
        ).first()

    # =====================================================
    # UPDATE
    # =====================================================
    @staticmethod
    def update_bgv(bgv_id, data):

        bgv = BGVService.get_request_by_id(bgv_id)

        if not bgv:
            return None

        if bgv.is_locked:
            raise Exception("Cannot update finalized BGV")

        bgv.candidate_name = data.get("candidate_name", bgv.candidate_name)
        bgv.email = data.get("email", bgv.email)
        bgv.phone = data.get("phone", bgv.phone)
        bgv.verification_type = data.get(
            "verification_type", bgv.verification_type
        )
        bgv.remarks = data.get("remarks", bgv.remarks)
        bgv.updated_at = datetime.utcnow()

        BGVService._log_action(bgv.id, "Updated BGV")

        db.session.commit()
        return bgv

    # =====================================================
    # SOFT DELETE
    # =====================================================
    @staticmethod
    def delete_bgv(bgv_id):

        bgv = BGVService.get_request_by_id(bgv_id)

        if not bgv:
            return None

        if bgv.is_locked:
            raise Exception("Cannot delete finalized BGV")

        bgv.is_deleted = True
        bgv.updated_at = datetime.utcnow()

        BGVService._log_action(bgv.id, "Soft Deleted BGV")

        db.session.commit()
        return bgv

    # =====================================================
    # ADD VERIFICATION RESULT
    # =====================================================
    @staticmethod
    def add_verification_result(bgv_id, data):

        bgv = BGVService.get_request_by_id(bgv_id)

        if not bgv:
            return None

        if bgv.is_locked:
            raise Exception("Cannot modify finalized BGV")

        verification = VerificationResult(
            bgv_id=bgv.id,
            verification_type=data.get("verification_type"),
            status=data.get("status"),
            module_score=data.get("module_score"),
            remarks=data.get("remarks"),
            is_deleted=False
        )

        db.session.add(verification)

        # Recalculate trust score
        BGVService._recalculate_logic(bgv.id)

        BGVService._log_action(bgv.id, "Added Verification")

        db.session.commit()
        return verification

    # =====================================================
    # MANUAL RECALCULATE
    # =====================================================
    @staticmethod
    def recalculate_trust_score(bgv_id):

        bgv = BGVService.get_request_by_id(bgv_id)

        if not bgv:
            return None

        if bgv.is_locked:
            raise Exception("Cannot recalc finalized BGV")

        BGVService._recalculate_logic(bgv_id)

        BGVService._log_action(bgv.id, "Manual Trust Score Recalculation")

        db.session.commit()

        return bgv

    # =====================================================
    # TRUST SCORE LOGIC
    # =====================================================
    @staticmethod
    def _recalculate_logic(bgv_id):

        bgv = BGVRequest.query.filter_by(
            id=bgv_id,
            is_deleted=False
        ).first()

        if not bgv:
            return

        verifications = VerificationResult.query.filter_by(
            bgv_id=bgv_id,
            is_deleted=False
        ).all()

        total = len(verifications)

        if total == 0:
            bgv.trust_score = 0
            bgv.status = "Pending"
            return

        passed = len(
            [v for v in verifications if v.status and v.status.lower() == "pass"]
        )

        score = int((passed / total) * 100)

        bgv.trust_score = score

        if score >= 80:
            bgv.status = "Approved"
        elif score >= 50:
            bgv.status = "Review"
        else:
            bgv.status = "Rejected"

        bgv.updated_at = datetime.utcnow()

    # =====================================================
    # FINALIZE BGV
    # =====================================================
    @staticmethod
    def finalize_bgv(bgv_id, final_decision):

        bgv = BGVService.get_request_by_id(bgv_id)

        if not bgv:
            return None

        if bgv.is_locked:
            raise Exception("BGV already finalized")

        if not final_decision:
            raise Exception("Final decision is required")

        bgv.final_decision = final_decision
        bgv.status = final_decision
        bgv.is_locked = True
        bgv.updated_at = datetime.utcnow()

        BGVService._log_action(bgv.id, f"Finalized as {final_decision}")

        db.session.commit()

        return bgv