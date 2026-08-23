from app.extensions import db
from datetime import datetime
from decimal import Decimal

class FraudCheck(db.Model):
    __tablename__ = "fraud_checks"

    id = db.Column(db.Integer, primary_key=True)
    bgv_id = db.Column(db.Integer, db.ForeignKey("bgv_requests.id"), nullable=False)
    issue = db.Column(db.String(255), nullable=False)
    risk_score = db.Column(db.Numeric(5,2), default=Decimal("0.00"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    bgv = db.relationship("BGVRequest", backref=db.backref("fraud_checks", lazy=True))

    def __repr__(self):
        return f"<FraudCheck BGV:{self.bgv_id} Issue:{self.issue}>"
