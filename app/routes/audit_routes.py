from flask import Blueprint, jsonify
from sqlalchemy import func

from app.extensions import db
from app.models.audit_log import AuditLog


audit_bp = Blueprint("audit", __name__)


# ---------------------------------------------------------
# Test Endpoint
# ---------------------------------------------------------
@audit_bp.route("/test", methods=["GET"])
def test_audit():

    try:
        log = AuditLog(
            user_id=4,
            action="TEST_AUDIT",
            module_name="AUDIT",
            entity_type="candidate",
            entity_id=1,
            status="SUCCESS",
            remarks="Inserted from Postman",
        )

        db.session.add(log)

        db.session.commit()

        return jsonify({"success": True, "message": "Audit log inserted"}), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"success": False, "message": str(e)}), 500


# ---------------------------------------------------------
# Get All Logs
# ---------------------------------------------------------
@audit_bp.route("/logs", methods=["GET"])
def get_logs():

    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).all()

    return jsonify({"success": True, "data": [log.to_dict() for log in logs]}), 200


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------
@audit_bp.route("/stats", methods=["GET"])
def get_stats():

    total = AuditLog.query.count()

    success = AuditLog.query.filter(func.upper(AuditLog.status) == "SUCCESS").count()

    warning = AuditLog.query.filter(func.upper(AuditLog.status) == "WARNING").count()

    critical = AuditLog.query.filter(func.upper(AuditLog.status) == "CRITICAL").count()

    return jsonify(
        {
            "success": True,
            "data": {
                "total": total,
                "success": success,
                "warning": warning,
                "critical": critical,
            },
        }
    ), 200
