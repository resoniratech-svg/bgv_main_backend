from app.extensions import db
from datetime import datetime

class RiskFlag(db.Model):
    __tablename__ = "risk_flags"

    id = db.Column(db.Integer, primary_key=True)
    bgv_id = db.Column(db.Integer, db.ForeignKey("bgv_requests.id"), nullable=False)
    flag_type = db.Column(db.String(100))
    severity = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    bgv = db.relationship("BGVRequest", backref=db.backref("risk_flags", lazy=True))

    def __repr__(self):
        return f"<RiskFlag BGV:{self.bgv_id} Type:{self.flag_type}>"
