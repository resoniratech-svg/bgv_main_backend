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

    return jsonify([user.to_dict() for user in users]), 200


# =========================
# UPDATE USER
# =========================
@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()
        old_values = {
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "is_active": user.is_active,
        }
        # =========================
        # CHECK DUPLICATE USERNAME
        # =========================
        username = data.get("username")

        if username:
            existing_username = User.query.filter(
                User.username == username, User.id != user_id
            ).first()

            if existing_username:
                return jsonify({"error": "Username already exists"}), 400

        if existing_username:
            return jsonify({"error": "Username already exists"}), 400

        # =========================
        # CHECK DUPLICATE EMAIL
        # =========================
        email = data.get("email")

        if email:
            existing_email = User.query.filter(
                User.email == email, User.id != user_id
            ).first()

            if existing_email:
                return jsonify({"error": "Email already exists"}), 400
        user.username = data.get("username", user.username)

        user.full_name = data.get("full_name", user.full_name)

        user.email = data.get("email", user.email)

        user.phone = data.get("phone", user.phone)

        user.role = data.get("role", user.role)

        password = data.get("password")

        if password:
            user.set_password(password)

        user.updated_at = datetime.utcnow()

        db.session.commit()

        print("USER UPDATED IN DATABASE")

        from app.services.audit_service import AuditService

        new_values = {
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "is_active": user.is_active,
        }

        print("CALLING AUDIT SERVICE")

        AuditService.log_action(
            action="UPDATE_USER",
            module_name="USERS",
            entity_type="user",
            entity_id=user.id,
            status="SUCCESS",
            remarks=f"Updated user {user.username}",
            old_values=old_values,
            new_values=new_values,
        )

        print("AUDIT SAVED")
        print("OLD VALUES:", old_values)
        print("NEW VALUES:", new_values)
        return jsonify(
            {"message": "User updated successfully", "user": user.to_dict()}
        ), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"error": str(e)}), 500


# =========================
# TOGGLE USER STATUS
# =========================
@user_bp.route("/<int:user_id>/status", methods=["PUT"])
def toggle_user_status(user_id):

    try:
        user = User.query.get(user_id)
        old_status = user.is_active
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.is_active = not user.is_active

        db.session.commit()
        from app.services.audit_service import AuditService

        AuditService.log_action(
            action="USER_STATUS_CHANGED",
            module_name="USERS",
            entity_type="user",
            entity_id=user.id,
            status="SUCCESS",
            remarks=f"User {'Activated' if user.is_active else 'Suspended'}",
            old_values={
                "username": user.username,
                "full_name": user.full_name,
                "is_active": old_status,
            },
            new_values={
                "username": user.username,
                "full_name": user.full_name,
                "is_active": user.is_active,
            },
        )
        return jsonify(
            {"message": "Status updated successfully", "is_active": user.is_active}
        ), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"error": str(e)}), 500


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        from app.services.audit_service import AuditService

        AuditService.log_action(
            action="DELETE_USER",
            module_name="USERS",
            entity_type="user",
            entity_id=user.id,
            status="SUCCESS",
            remarks=f"Deleted user {user.username}",
            old_values={
                "username": user.username,
                "full_name": user.full_name,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
                "is_active": user.is_active,
            },
        )
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"error": str(e)}), 500


@user_bp.route("/<int:user_id>/status", methods=["PUT"])
def update_status(user_id):

    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()

        user.is_active = data.get("is_active", user.is_active)

        db.session.commit()

        return jsonify({"message": "Status updated successfully"}), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"error": str(e)}), 500
