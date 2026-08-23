from functools import wraps

from flask_jwt_extended import get_jwt
from flask import current_app

from app.utils.exceptions import FraudException


def role_required(*allowed_roles):

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):

            claims = get_jwt()

            user_role = str(claims.get("role", "")).strip().upper()

            normalized_allowed = [str(role).strip().upper() for role in allowed_roles]

            # SUPER_ADMIN has access to all protected routes
            if user_role == "SUPER_ADMIN":
                return fn(*args, **kwargs)

            # ADMIN has access to all protected admin routes
            if user_role == "ADMIN":
                return fn(*args, **kwargs)

            # Other roles must be explicitly allowed
            if user_role not in normalized_allowed:
                current_app.logger.warning(
                    f"Access denied for role: {user_role}. "
                    f"Allowed roles: {normalized_allowed}"
                )

                raise FraudException("Access denied", 403)

            return fn(*args, **kwargs)

        return wrapper

    return decorator
