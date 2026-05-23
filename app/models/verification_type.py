from app.extensions import db
from datetime import datetime

class VerificationType(db.Model):
    __tablename__ = "verification_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    verification_results = db.relationship(
        "VerificationResult",
        back_populates="verification_type",
        lazy=True
    )

    def __repr__(self):
        return f"<VerificationType {self.name}>"