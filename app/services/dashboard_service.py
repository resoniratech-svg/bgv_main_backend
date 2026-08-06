# from app.models.bgv_request import BGVRequest


# class DashboardService:
#     @staticmethod
#     def get_summary():
#         # Actual implementation using models
#         total = BGVRequest.query.filter_by(is_deleted=False).count()
#         pending = BGVRequest.query.filter_by(
#             status="Initiated", is_deleted=False
#         ).count()
#         completed = BGVRequest.query.filter_by(
#             status="Completed", is_deleted=False
#         ).count()
#         rejected = BGVRequest.query.filter_by(
#             final_decision="Rejected", is_deleted=False
#         ).count()

#         return {
#             "total_requests": total,
#             "PENDING": pending,
#             "completed": completed,
#             "rejected": rejected,
#         }

#     @staticmethod
#     def get_candidate_history(candidate_id):
#         # Simplistic implementation for now
#         requests = BGVRequest.query.filter_by(id=candidate_id, is_deleted=False).all()
#         return [r.to_dict() if hasattr(r, "to_dict") else str(r) for r in requests]
