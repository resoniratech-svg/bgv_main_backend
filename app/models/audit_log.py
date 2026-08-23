from app.extensions import db
from datetime import datetime


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, nullable=True)

    action = db.Column(db.String(255), nullable=False)

    module_name = db.Column(db.String(100), nullable=True)

    entity_type = db.Column(db.String(100), nullable=True)

    entity_id = db.Column(db.Integer, nullable=True)

    ip_address = db.Column(db.String(100), nullable=True)

    user_agent = db.Column(db.Text, nullable=True)

    request_method = db.Column(db.String(20), nullable=True)

    endpoint = db.Column(db.String(255), nullable=True)

    old_values = db.Column(db.JSON, nullable=True)

    new_values = db.Column(db.JSON, nullable=True)

    status = db.Column(db.String(50), nullable=True)
    changes = db.Column(db.JSON)
    remarks = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "module_name": self.module_name,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "ip_address": self.ip_address,
            "request_method": self.request_method,
            "endpoint": self.endpoint,
            "status": self.status,
            "remarks": self.remarks,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
