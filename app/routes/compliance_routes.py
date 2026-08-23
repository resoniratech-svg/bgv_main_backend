from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.consent_record import ConsentRecord

compliance_bp = Blueprint("compliance", __name__)


@compliance_bp.route("/consent", methods=["POST"])
@jwt_required()
def create_consent():
    try:
        data = request.get_json() or {}

        candidate_id = data.get("candidate_id") or data.get("bgv_id")
        consent = data.get("consent", True)

        if not candidate_id:
            return jsonify({"error": "candidate_id or bgv_id is required"}), 400

        existing = ConsentRecord.query.filter_by(candidate_id=candidate_id).first()

        if existing:
            existing.consent_status = bool(consent)
        else:
            record = ConsentRecord(
                candidate_id=candidate_id,
                consent_status=bool(consent)
            )
            db.session.add(record)

        db.session.commit()

        return jsonify({
            "message": "Consent recorded successfully",
            "candidate_id": candidate_id,
            "consent": bool(consent)
        }), 201

    except Exception as e:

        import traceback

        print("\n========== CANDIDATE ERROR ==========")
        traceback.print_exc()
        print("=====================================\n")

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500