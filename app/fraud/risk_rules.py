class DuplicateDocumentRule:
    def evaluate(self, data):
        if data.get("duplicate_document"):
            return {
                "issue": "duplicate_document",
                "risk_score": 30,
                "severity": "HIGH"
            }
        return None


class EmploymentOverlapRule:
    def evaluate(self, data):
        if data.get("employment_overlap"):
            return {
                "issue": "employment_overlap",
                "risk_score": 20,
                "severity": "MEDIUM"
            }
        return None


class HighCreditRiskRule:
    def evaluate(self, data):
        credit_score = data.get("credit_score", 750)
        if credit_score < 500:
            return {
                "issue": "high_credit_risk",
                "risk_score": 40,
                "severity": "HIGH"
            }
        return None
