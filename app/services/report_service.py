from app.models.bgv_request import BGVRequest
from app.models.fraud_check import FraudCheck
from app.models.risk_flag import RiskFlag
from app.utils.exceptions import FraudException
from app.repositories.report_repository import (
    ReportRepository
)

class ReportService:
    @staticmethod
    def get_all_reports():

        reports = (
            ReportRepository
            .get_all_reports()
        )

        return reports
    @staticmethod
    def generate_report(bgv_id):

        bgv = BGVRequest.query.get(bgv_id)

        if not bgv:
            raise FraudException("BGV request not found", 404)

        fraud_checks = FraudCheck.query.filter_by(bgv_id=bgv_id).all()
        risk_flags = RiskFlag.query.filter_by(bgv_id=bgv_id).all()

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
                } for fc in fraud_checks
            ],
            "risk_flags": [
                {
                    "flag_type": rf.flag_type,
                    "severity": rf.severity
                } for rf in risk_flags
            ]
        }
