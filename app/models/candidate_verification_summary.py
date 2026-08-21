from datetime import datetime
from app.extensions import db


class CandidateVerificationSummary(db.Model):
    __tablename__ = "candidate_verification_summary"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    candidate_id = db.Column(db.Integer, unique=True, nullable=True)
    candidate_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(50), nullable=True)

    aadhaar_status = db.Column(db.String(50), nullable=True)
    pan_status = db.Column(db.String(50), nullable=True)
    passport_status = db.Column(db.String(50), nullable=True)
    face_match_status = db.Column(db.String(50), nullable=True)
    resume_status = db.Column(db.String(50), nullable=True)
    education_status = db.Column(db.String(50), nullable=True)
    employment_status = db.Column(db.String(50), nullable=True)
    credit_status = db.Column(db.String(50), nullable=True)
    court_status = db.Column(db.String(50), nullable=True)
    watchlist_status = db.Column(db.String(50), nullable=True)
    dl_status = db.Column(db.String(50), nullable=True)
    deepfake_status = db.Column(db.String(50), nullable=True)
    salary_slip_status = db.Column(db.String(50), nullable=True)
    bank_statement_status = db.Column(db.String(50), nullable=True)

    overall_status = db.Column(db.String(50), nullable=True)
    risk_level = db.Column(db.String(50), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
