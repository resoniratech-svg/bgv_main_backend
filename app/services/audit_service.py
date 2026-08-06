from flask import request
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models.audit_log import AuditLog

import json


class AuditService:
    @staticmethod
    def log_action(
        action,
        status="SUCCESS",
        entity_type=None,
        entity_id=None,
        module_name=None,
        remarks=None,
        old_values=None,
        new_values=None,
        changes=None,
    ):

        try:
            verify_jwt_in_request(optional=True)

            user_id = get_jwt_identity()

        except:
            user_id = None

        old_values = (
            json.loads(json.dumps(old_values, default=str)) if old_values else None
        )

        new_values = (
            json.loads(json.dumps(new_values, default=str)) if new_values else None
        )

        log = AuditLog(
            user_id=user_id,
            action=action,
            module_name=module_name,
            entity_type=entity_type,
            entity_id=entity_id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent"),
            request_method=request.method,
            endpoint=request.path,
            old_values=old_values,
            new_values=new_values,
            changes=changes,
            status=status,
            remarks=remarks,
        )
        print("AUDIT OLD:", old_values)
        print("AUDIT NEW:", new_values)
        print("ADDING AUDIT")

        db.session.add(log)

        print("COMMITTING AUDIT")

        db.session.commit()

        print("AUDIT COMMITTED")
