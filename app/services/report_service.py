from app.models.bgv_request import BGVRequest
from app.models.fraud_check import FraudCheck
from app.models.risk_flag import RiskFlag
from app.utils.exceptions import FraudException
from app.repositories.report_repository import ReportRepository
from app.services.notification_service import NotificationService


class ReportService:
    @staticmethod
    def get_all_reports():

        reports = ReportRepository.get_all_reports()

        result = []

        for report in reports:
            result.append(
                {
                    "id": report["id"],
                    "candidate_id": report["candidate_id"],
                    "candidate_name": report["candidate_name"],
                    "report_name": report["report_name"],
                    "report_status": report["report_status"],
                    "verification_status": report["verification_status"],
                    "file_name": report["file_name"],
                    "file_url": report["file_url"],
                    "generated_at": str(report["generated_at"])
                    if report["generated_at"]
                    else None,
                }
            )

        return result

    @staticmethod
    def generate_report(bgv_id):

        bgv = BGVRequest.query.get(bgv_id)

        if not bgv:
            raise FraudException("BGV request not found", 404)

        fraud_checks = FraudCheck.query.filter_by(bgv_id=bgv_id).all()
        risk_flags = RiskFlag.query.filter_by(bgv_id=bgv_id).all()

        from app.services.audit_service import AuditService

        AuditService.log_action(
            action="VIEW_REPORT",
            module_name="REPORTS",
            entity_type="candidate",
            entity_id=bgv.candidate_id,
            status="SUCCESS",
            remarks=f"Viewed BGV report #{bgv_id}",
        )
        NotificationService.create_notification(
            candidate_id=bgv.candidate_id,
            bgv_id=bgv_id,
            title="BGV Report Generated",
            description=f"Background verification report generated successfully for BGV {bgv_id}.",
            notification_type="Success",
        )
        return {
            "bgv_id": bgv.id,
            "candidate_name": bgv.candidate_name,
            "status": bgv.status,
            "trust_score": bgv.trust_score,
            "final_decision": bgv.final_decision,
            "fraud_issues": [
                {
                    "issue": fc.issue,
                    "risk_score": float(fc.risk_score),
                }
                for fc in fraud_checks
            ],
            "risk_flags": [
                {
                    "flag_type": rf.flag_type,
                    "severity": rf.severity,
                }
                for rf in risk_flags
            ],
        }

    @staticmethod
    def view_report(candidate_id):

        report = ReportRepository.get_latest_report_by_candidate(candidate_id)

        if not report:
            raise Exception("Report not found")
        NotificationService.create_notification(
            candidate_id=candidate_id,
            title="BGV Report Viewed",
            description="A background verification report was viewed.",
            notification_type="Info",
        )
        return report


@staticmethod
def get_report_view(candidate_id):

    report = ReportRepository.get_report_view_data(candidate_id)

    if report is None:
        raise FraudException("Report not found", 404)

    return {
        "candidate": {
            "name": report["candidate_name"],
            "email": report["email"],
            "phone": report["phone"],
        },
        "modules": [
            {"name": "Aadhaar", "status": report["aadhaar_status"]},
            {"name": "PAN", "status": report["pan_status"]},
            {"name": "Passport", "status": report["passport_status"]},
            {"name": "Driving License", "status": report["dl_status"]},
            {"name": "Face Match", "status": report["face_match_status"]},
            {"name": "Resume", "status": report["resume_status"]},
            {"name": "Education", "status": report["education_status"]},
            {"name": "Employment", "status": report["employment_status"]},
            {"name": "Salary Slip", "status": report["salary_slip_status"]},
            {"name": "Credit Bureau", "status": report["credit_status"]},
            {"name": "Court Record", "status": report["court_status"]},
            {"name": "Watchlist", "status": report["watchlist_status"]},
            {"name": "Deepfake", "status": report["deepfake_status"]},
        ],
        "overall_status": report["overall_status"],
        "risk_level": report["risk_level"],
    }
