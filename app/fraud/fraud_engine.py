from decimal import Decimal
from app.extensions import db
from app.models.fraud_check import FraudCheck
from app.models.risk_flag import RiskFlag
from app.models.bgv_request import BGVRequest
# from app.compliance.audit_service import AuditService # Needs to be ported or adapted
from flask import current_app

class FraudEngine:

    def __init__(self, rules):
        self.rules = rules

    def execute(self, bgv_id, data):
        current_app.logger.info(
            f"Fraud execution started for BGV ID: {bgv_id}"
        )
        total_score = Decimal("0.00")
        issues_detected = []
        for rule in self.rules:
            result = rule.evaluate(data)
            if result:
                total_score += Decimal(result["risk_score"])
                issues_detected.append(result)

                # Adapted logging logic
                current_app.logger.warning(f"Fraud detected for BGV {bgv_id}: {result['issue']}")

                fraud_entry = FraudCheck(
                    bgv_id=bgv_id,
                    issue=result["issue"],
                    risk_score=result["risk_score"]
                )
                db.session.add(fraud_entry)

                flag_entry = RiskFlag(
                    bgv_id=bgv_id,
                    flag_type=result["issue"],
                    severity=result["severity"]
                )
                db.session.add(flag_entry)

        status = self.decision_engine(total_score)
        current_app.logger.info(
            f"Fraud completed for BGV ID: {bgv_id} | Score: {total_score} | Status: {status}"
        )
        bgv = BGVRequest.query.get(bgv_id)
        if not bgv:
             return {"error": "BGV request not found"}

        bgv.status = status
        bgv.trust_score = float(total_score) # Syncing trust_score

        db.session.commit()

        return {
            "fraud_score": float(total_score),
            "status": status,
            "issues": issues_detected
        }

    def decision_engine(self, fraud_score):
        if fraud_score > 70:
            return "Rejected"
        elif 40 <= fraud_score <= 70:
            return "Review Required"
        return "Verified"
