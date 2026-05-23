import os
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from werkzeug.utils import secure_filename

from app.extensions import db
from flask_jwt_extended import jwt_required

from app.models.bgv_request import BGVRequest
from app.models.verification_result import VerificationResult
from app.models.verification_type import VerificationType
from app.services.audit_service import log_action
from app.utils.role_required import role_required

bgv_bp = Blueprint("bgv", __name__)


# ==============================
# CREATE BGV - HR Only
# ==============================
@bgv_bp.route("/", methods=["POST"])
@jwt_required()
@role_required(["SUPER_ADMIN"])
def create_bgv():
    try:
        data = request.get_json()

        new_bgv = BGVRequest(
            candidate_name=data.get("candidate_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            status="Initiated",
            trust_score=0,
            final_decision=None,
            is_locked=False,
            is_deleted=False
        )

        db.session.add(new_bgv)
        db.session.commit()

        log_action(
            action="BGV_CREATED",
            entity_type="BGV",
            entity_id=new_bgv.id
        )

        return jsonify({
            "message": "BGV created successfully",
            "bgv_id": new_bgv.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ==============================
# GET SINGLE BGV + VERIFICATIONS
# ==============================
@bgv_bp.route("/<int:bgv_id>", methods=["GET"])
@jwt_required()
@role_required(["SUPER_ADMIN"])
def get_bgv(bgv_id):
    bgv = BGVRequest.query.filter_by(id=bgv_id, is_deleted=False).first()

    if not bgv:
        return jsonify({"error": "BGV not found"}), 404

    verifications = VerificationResult.query.filter_by(
        bgv_id=bgv_id,
        is_deleted=False
    ).all()

    verification_list = []
    for v in verifications:
        verification_list.append({
            "id": v.id,
            "verification_type": v.verification_type.name,
            "status": v.status,
            "module_score": v.module_score,
            "remarks": v.remarks,
            "created_at": str(v.created_at)
        })

    verification_label = "BGV+" if verification_list else "BGV"

    return jsonify({
        "id": bgv.id,
        "candidate_name": bgv.candidate_name,
        "email": bgv.email,
        "phone": bgv.phone,
        "status": bgv.status,
        "trust_score": bgv.trust_score,
        "final_decision": bgv.final_decision,
        "verification_label": verification_label,
        "verifications": verification_list
    }), 200


# ==============================
# SOFT DELETE - Admin Only
# ==============================
@bgv_bp.route("/<int:bgv_id>", methods=["DELETE"])
@jwt_required()
@role_required(["SUPER_ADMIN"])
def delete_bgv(bgv_id):
    bgv = BGVRequest.query.filter_by(id=bgv_id, is_deleted=False).first()

    if not bgv:
        return jsonify({"error": "BGV not found"}), 404

    bgv.is_deleted = True
    db.session.commit()

    log_action(
        action="BGV_DELETED",
        entity_type="BGV",
        entity_id=bgv_id
    )

    return jsonify({
        "message": "BGV soft deleted"
    }), 200


# ==============================
# ADD VERIFICATION - Verifier Only
# ==============================
@bgv_bp.route("/<int:bgv_id>/verification", methods=["POST"])
@jwt_required()
@role_required(["SUPER_ADMIN"])
def add_verification(bgv_id):
    bgv = BGVRequest.query.filter_by(id=bgv_id, is_deleted=False).first()

    if not bgv:
        return jsonify({"error": "BGV not found"}), 404

    # Handle File Upload
    document_path = None
    if 'document' in request.files:
        file = request.files['document']
        if file.filename != '':
            filename = secure_filename(f"bgv_{bgv_id}_{file.filename}")
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            document_path = f"static/uploads/{filename}"

    # Handle form data or JSON
    if request.form:
        data = request.form
    else:
        data = request.get_json() or {}

    verification = VerificationResult(
        bgv_id=bgv_id,
        verification_type_id=data.get("verification_type_id"),
        status=data.get("status"),
        module_score=data.get("module_score"),
        remarks=data.get("remarks"),
        document_path=document_path
    )

    db.session.add(verification)
    db.session.commit()

    log_action(
        action="VERIFICATION_ADDED",
        entity_type="VERIFICATION",
        entity_id=verification.id
    )

    return jsonify({
        "message": "Verification added successfully",
        "document_url": document_path
    }), 201


# ==============================
# RECALCULATE TRUST SCORE
# ==============================
@bgv_bp.route("/<int:bgv_id>/recalculate", methods=["POST"])
@jwt_required()
def recalculate_trust_score(bgv_id):
    bgv = BGVRequest.query.filter_by(id=bgv_id, is_deleted=False).first()

    if not bgv:
        return jsonify({"error": "BGV not found"}), 404

    verifications = VerificationResult.query.filter_by(
        bgv_id=bgv_id,
        is_deleted=False
    ).all()

    if not verifications:
        return jsonify({"error": "No verifications found"}), 400

    total_score = sum(v.module_score or 0 for v in verifications)

    avg_score = total_score / len(verifications)

    bgv.trust_score = round(avg_score, 2)

    db.session.commit()

    log_action(
        action="TRUST_SCORE_RECALCULATED",
        entity_type="BGV",
        entity_id=bgv_id
    )

    return jsonify({
        "message": "Trust score recalculated",
        "trust_score": bgv.trust_score
    }), 200
# ==============================
# FINALIZE BGV - HR Only
# ==============================

@bgv_bp.route("/<int:bgv_id>/finalize", methods=["POST"])
@jwt_required()
@role_required(["SUPER_ADMIN"])
def finalize_bgv(bgv_id):
    try:
        bgv = BGVRequest.query.filter_by(id=bgv_id, is_deleted=False).first()

        if not bgv:
            return jsonify({"error": "BGV not found"}), 404

        if bgv.is_locked:
            return jsonify({"error": "BGV already finalized"}), 400

        if bgv.trust_score is None:
            return jsonify({"error": "Trust score not calculated"}), 400

        if bgv.trust_score >= 80:
            decision = "Approved"
        elif bgv.trust_score >= 50:
            decision = "Review Required"
        else:
            decision = "Rejected"

        bgv.final_decision = decision
        bgv.status = "Completed"
        bgv.is_locked = True

        db.session.commit()

        log_action(
            action="BGV_FINALIZED",
            entity_type="BGV",
            entity_id=bgv_id
        )

        return jsonify({
            "message": "BGV finalized successfully",
            "bgv_id": bgv.id,
            "final_decision": decision,
            "trust_score": bgv.trust_score
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500