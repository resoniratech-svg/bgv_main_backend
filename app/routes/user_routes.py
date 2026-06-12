from flask import Blueprint, jsonify, request
from datetime import datetime
from app.models.user import User
from app.extensions import db

user_bp = Blueprint("users", __name__)


# =========================
# GET ALL USERS
# =========================
@user_bp.route("/", methods=["GET"])
def get_users():

    users = User.query.all()

    return jsonify(
        [user.to_dict() for user in users]
    ), 200


# =========================
# UPDATE USER
# =========================
@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    try:

        user = User.query.get(user_id)

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        data = request.get_json()

        user.username = data.get(
            "username",
            user.username
        )

        user.full_name = data.get(
            "full_name",
            user.full_name
        )

        user.email = data.get(
            "email",
            user.email
        )

        user.phone = data.get(
            "phone",
            user.phone
        )

        user.role = data.get(
            "role",
            user.role
        )

        if data.get("password"):

            user.set_password(
                data.get("password")
            )

        password = data.get("password")

        if password:
            user.set_password(password)

        user.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            "message": "User updated successfully",
            "user": user.to_dict()
        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500

# =========================
# TOGGLE USER STATUS
# =========================
@user_bp.route("/<int:user_id>/status", methods=["PUT"])
def toggle_user_status(user_id):

    try:

        user = User.query.get(user_id)

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        user.is_active = not user.is_active

        db.session.commit()

        return jsonify({
            "message": "Status updated successfully",
            "is_active": user.is_active
        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500
@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    try:

        user = User.query.get(user_id)

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        db.session.delete(user)

        db.session.commit()

        return jsonify({
            "message": "User deleted successfully"
        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500

@user_bp.route("/<int:user_id>/status", methods=["PUT"])
def update_status(user_id):

    try:

        user = User.query.get(user_id)

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        data = request.get_json()

        user.is_active = data.get(
            "is_active",
            user.is_active
        )

        db.session.commit()

        return jsonify({
            "message": "Status updated successfully"
        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500