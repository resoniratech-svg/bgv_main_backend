from app.models.audit_log import AuditLog
from app.extensions import db
from flask_jwt_extended import get_jwt_identity

class AuditService:

    @staticmethod
    def log_action(action, entity_type=None, entity_id=None):
        performed_by = None
        try:
            performed_by = get_jwt_identity()
        except:
            pass

        log = AuditLog(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            performed_by=performed_by
        )
        db.session.add(log)
        db.session.commit()