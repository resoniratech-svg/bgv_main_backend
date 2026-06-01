from app.models.bgv_request import BGVRequest


class DashboardService:

    @staticmethod
    def get_summary():

        total_requests = BGVRequest.query.filter_by(
            is_deleted=False
        ).count()

        pending = BGVRequest.query.filter_by(
            status="PENDING",
            is_deleted=False
        ).count()

        completed = BGVRequest.query.filter_by(
            status="Completed",
            is_deleted=False
        ).count()

        rejected = BGVRequest.query.filter_by(
            status="Rejected",
            is_deleted=False
        ).count()

        approved = BGVRequest.query.filter_by(
            status="Approved",
            is_deleted=False
        ).count()

        return {
            "total_requests": total_requests,
            "PENDING": pending,
            "completed": completed,
            "rejected": rejected,
            "approved": approved
        }

    @staticmethod
    def get_candidate_history(candidate_id):

        bgvs = BGVRequest.query.filter_by(
            id=candidate_id,
            is_deleted=False
        ).all()

        if not bgvs:
            return []

        result = []

        for bgv in bgvs:
            result.append({
                "bgv_id": bgv.id,
                "candidate_name": bgv.candidate_name,
                "email": bgv.email,
                "phone": bgv.phone,
                "status": bgv.status,
                "trust_score": bgv.trust_score,
                "final_decision": bgv.final_decision,
                "created_at": str(bgv.created_at)
            })

        return result