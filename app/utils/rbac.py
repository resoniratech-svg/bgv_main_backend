from functools import wraps
from flask_jwt_extended import get_jwt
from flask import current_app
from app.utils.exceptions import FraudException


def role_required(*allowed_roles):

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            claims = get_jwt()
            user_role = claims.get("role")

            if user_role not in allowed_roles:

                current_app.logger.warning(
                    f"Access denied for role: {user_role}"
                )

                raise FraudException("Access denied", 403)

            return fn(*args, **kwargs)

        return wrapper

    return decorator