from app.extensions import db
from app.models.audit_log import AuditLog


def log_action(action, entity_type, entity_id, performed_by=None):

    log = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        performed_by=performed_by
    )

    db.session.add(log)
    db.session.commit()