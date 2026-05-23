from app.extensions import db
from datetime import datetime

class ConsentRecord(db.Model):
    __tablename__ = "consent_records"

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, nullable=False) # Linked to BGV candidate
    consent_status = db.Column(db.Boolean, default=False)
    consent_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ConsentRecord Candidate:{self.candidate_id} Status:{self.consent_status}>"
