from app.models.bgv_request import BGVRequest
from app.models.fraud_check import FraudCheck
from app.models.risk_flag import RiskFlag
from app.repositories.report_repository import ReportRepository
from app.utils.exceptions import FraudException


class ReportService:

    @staticmethod
    def get_all_reports():

        reports = ReportRepository.get_all_reports()

        result = []

        for report in reports:

            result.append({

                "id": report["id"],
                "candidate_id": report["candidate_id"],
                 "candidate_name": report["candidate_name"],
                "report_name": report["report_name"],
                "report_status": report["report_status"],
                "verification_status": report["verification_status"],
                "file_name": report["file_name"],
                "file_url": report["file_url"],
                "generated_at": str(
                    report.get("generated_at")
                ) if report.get("generated_at")
                else None

            })

        return result

    @staticmethod
    def generate_report(bgv_id):

        bgv = BGVRequest.query.get(bgv_id)

        if not bgv:
            raise FraudException(
                "BGV request not found",
                404
            )

        fraud_checks = FraudCheck.query.filter_by(
            bgv_id=bgv_id
        ).all()

        risk_flags = RiskFlag.query.filter_by(
            bgv_id=bgv_id
        ).all()

        return {
            "bgv_id": bgv.id,
            "candidate_name": bgv.candidate_name,
            "status": bgv.status,
            "trust_score": bgv.trust_score,
            "final_decision": bgv.final_decision,

            "fraud_issues": [
                {
                    "issue": fc.issue,
                    "risk_score": float(fc.risk_score)
                }
                for fc in fraud_checks
            ],

            "risk_flags": [
                {
                    "flag_type": rf.flag_type,
                    "severity": rf.severity
                }
                for rf in risk_flags
            ]
        }