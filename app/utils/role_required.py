from functools import wraps
from flask_jwt_extended import get_jwt
from flask import jsonify


def role_required(*allowed_roles):

    def wrapper(fn):

        @wraps(fn)
        def decorator(*args, **kwargs):

            claims = get_jwt()
            role = claims.get("role")

            if role not in allowed_roles:
                return jsonify({
                    "error": f"Unauthorized. Required roles: {allowed_roles}, your role: {role}"
                }), 403

            return fn(*args, **kwargs)

        return decorator

    return wrapper