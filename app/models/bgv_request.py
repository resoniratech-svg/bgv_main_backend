from datetime import datetime
from app.extensions import db

class BGVRequest(db.Model):
    __tablename__ = "bgv_requests"

    id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(50), default="Initiated", nullable=False)
    trust_score = db.Column(db.Float, default=0.0, nullable=False)
    final_decision = db.Column(db.String(50), nullable=True)
    is_locked = db.Column(db.Boolean, default=False, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # ✅ Correct relationship name matching VerificationResult
    verification_results = db.relationship(
        "VerificationResult",
        back_populates="bgv",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<BGVRequest {self.candidate_name}>"