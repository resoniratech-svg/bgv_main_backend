from app.extensions import db
from datetime import datetime

class VerificationResult(db.Model):
    __tablename__ = "verification_results"

    id = db.Column(db.Integer, primary_key=True)
    bgv_id = db.Column(db.Integer, db.ForeignKey("bgv_requests.id"), nullable=False)
    verification_type_id = db.Column(db.Integer, db.ForeignKey("verification_types.id"), nullable=False)
    status = db.Column(db.String(50))
    module_score = db.Column(db.Float) 
    remarks = db.Column(db.Text)
    document_path = db.Column(db.String(255)) # New field for file uploads
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ Both back_populates must match exactly
    verification_type = db.relationship("VerificationType", back_populates="verification_results")
    bgv = db.relationship("BGVRequest", back_populates="verification_results")

    def __repr__(self):
        return f"<VerificationResult BGV:{self.bgv_id} Type:{self.verification_type_id}>"