from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.verification_type import VerificationType
from app.utils.role_required import role_required
from app.services.audit_service import log_action

verification_type_bp = Blueprint("verification_types", __name__)


# =================================
# GET ALL VERIFICATION TYPES
# =================================
@verification_type_bp.route("/", methods=["GET"])
@jwt_required()
def get_verification_types():
    types = VerificationType.query.filter_by(is_deleted=False).all()

    result = []
    for t in types:
        result.append({
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "is_active": t.is_active,
            "created_at": str(t.created_at)
        })

    return jsonify(result), 200


# =================================
# CREATE VERIFICATION TYPE - Admin
# =================================
@verification_type_bp.route("/", methods=["POST"])
@jwt_required()
@role_required("Admin")
def create_verification_type():

    try:
        data = request.get_json()

        vt = VerificationType(
            name=data.get("name"),
            description=data.get("description"),
            is_active=True,
            is_deleted=False
        )

        db.session.add(vt)
        db.session.commit()

        log_action(
            action="VERIFICATION_TYPE_CREATED",
            entity_type="VERIFICATION_TYPE",
            entity_id=vt.id
        )

        return jsonify({
            "message": "Verification type created",
            "id": vt.id
        }), 201

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "error": "Verification type already exists"
        }), 409

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# =================================
# UPDATE VERIFICATION TYPE - Admin
# =================================
@verification_type_bp.route("/<int:type_id>", methods=["PUT"])
@jwt_required()
@role_required("Admin")
def update_verification_type(type_id):
    vt = VerificationType.query.filter_by(id=type_id, is_deleted=False).first()

    if not vt:
        return jsonify({"error": "Verification type not found"}), 404

    data = request.get_json()
    vt.name = data.get("name", vt.name)
    vt.description = data.get("description", vt.description)
    vt.is_active = data.get("is_active", vt.is_active)

    db.session.commit()

    log_action(
        action="VERIFICATION_TYPE_UPDATED",
        entity_type="VERIFICATION_TYPE",
        entity_id=vt.id
    )

    return jsonify({"message": "Verification type updated"}), 200


# =================================
# DELETE VERIFICATION TYPE - Admin
# =================================
@verification_type_bp.route("/<int:type_id>", methods=["DELETE"])
@jwt_required()
@role_required("Admin")
def delete_verification_type(type_id):
    vt = VerificationType.query.filter_by(id=type_id, is_deleted=False).first()

    if not vt:
        return jsonify({"error": "Verification type not found"}), 404

    vt.is_deleted = True
    db.session.commit()

    log_action(
        action="VERIFICATION_TYPE_DELETED",
        entity_type="VERIFICATION_TYPE",
        entity_id=vt.id
    )

    return jsonify({"message": "Verification type deleted"}), 200