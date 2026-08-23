from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import os
from datetime import datetime, timedelta
import secrets
from app.services.email_service import EmailService
from app.extensions import bcrypt
from app.models.user import User
from app.extensions import db

auth_bp = Blueprint("auth", __name__)


# ===============================
# REGISTER
# ===============================
@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        username = data.get("username")
        password = data.get("password")

        full_name = data.get("full_name")
        email = data.get("email")
        phone = data.get("phone")

        role = "SUPER_ADMIN"

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return jsonify(
                {"success": False, "message": "Username already exists"}
            ), 409

        if email:
            existing_email = User.query.filter_by(email=email).first()

            if existing_email:
                return jsonify(
                    {"success": False, "message": "Email already exists"}
                ), 409

        new_user = User(
            username=username,
            full_name=full_name,
            email=email,
            phone=phone,
            role=role,
            created_by=1,  # Temporary
        )

        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify(
            {"success": True, "message": "User registered successfully"}
        ), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({"error": str(e)}), 500


# ===============================
# LOGIN
# ===============================
@auth_bp.route("/login", methods=["POST"])
def login():

    try:
        data = request.get_json()

        print("\n========================")
        print("LOGIN ATTEMPT")
        print("========================")

        print("REQUEST DATA =", data)

        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        username = data.get("username")
        password = data.get("password")

        print("USERNAME =", username)
        print("PASSWORD =", password)

        user = User.query.filter_by(username=username, is_active=True).first()

        print("USER FOUND =", user)

        if user:
            print("DB HASH =", user.password_hash)

            password_match = user.check_password(password)

            print("PASSWORD MATCH =", password_match)

        if not user:
            print("USER NOT FOUND")

            return jsonify({"error": "Invalid credentials"}), 401

        if not user.check_password(password):
            print("PASSWORD INCORRECT")

            return jsonify({"error": "Invalid credentials"}), 401

        user.last_login = datetime.now()

        db.session.commit()

        access_token = create_access_token(
            identity=str(user.id), additional_claims={"role": user.role}
        )

        print("LOGIN SUCCESSFUL")

        return jsonify(
            {"access_token": access_token, "username": user.username, "role": user.role}
        ), 200

    except Exception as e:
        print("LOGIN ERROR =", str(e))

        return jsonify({"error": str(e)}), 500


# ===============================
# FORGOT PASSWORD
# ===============================
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():

    try:
        data = request.get_json()

        email = data.get("email")

        if not email:
            return jsonify({"success": False, "message": "Email is required"}), 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify(
                {"success": False, "message": "No account found with this email"}
            ), 404

        reset_token = secrets.token_urlsafe(32)

        user.reset_token = reset_token

        user.reset_token_expiry = datetime.now() + timedelta(hours=1)

        db.session.commit()

        frontend_url = os.getenv("FRONTEND_URL")

        reset_link = f"{frontend_url}/reset-password/{reset_token}"

        EmailService.send_password_reset_email(
            user.email, user.full_name or user.username, reset_link
        )

        return jsonify({"success": True, "message": "Password reset email sent"}), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"success": False, "message": str(e)}), 500


# ===============================
# CURRENT LOGGED IN USER
# ===============================
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():

    try:
        user_id = get_jwt_identity()

        user = db.session.get(User, int(user_id))

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(
            {
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
                "is_active": user.is_active,
                "last_login": (
                    user.last_login.isoformat() if user.last_login else None
                ),
                "created_at": (
                    user.created_at.isoformat() if user.created_at else None
                ),
                "created_by": user.created_by,
            }
        ), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===============================
# UPDATE PROFILE
# ===============================
@auth_bp.route("/update-profile", methods=["PUT"])
@jwt_required()
def update_profile():

    try:
        user_id = get_jwt_identity()

        user = db.session.get(User, int(user_id))

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        data = request.get_json()

        username = data.get("username")

        full_name = data.get("full_name")

        email = data.get("email")

        phone = data.get("phone")

        existing_user = User.query.filter(
            User.username == username, User.id != user.id
        ).first()

        if existing_user:
            return jsonify(
                {"success": False, "message": "Username already exists"}
            ), 400

        existing_email = User.query.filter(
            User.email == email, User.id != user.id
        ).first()

        if existing_email:
            return jsonify({"success": False, "message": "Email already exists"}), 400

        user.username = username
        user.full_name = full_name
        user.email = email
        user.phone = phone

        db.session.commit()

        return jsonify(
            {"success": True, "message": "Profile updated successfully"}
        ), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"success": False, "message": str(e)}), 500


# ===============================
# CHANGE PASSWORD
# ===============================
@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    print("RESET PASSWORD ROUTE HIT")
    try:
        user_id = get_jwt_identity()

        user = db.session.get(User, int(user_id))

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        data = request.get_json()

        current_password = data.get("current_password")

        new_password = data.get("new_password")

        if not user.check_password(current_password):
            return jsonify(
                {"success": False, "message": "Current password is incorrect"}
            ), 400

        print("DB URL =", db.engine.url)
        print("USER ID =", user.id)
        print("OLD HASH =", user.password_hash)

        user.password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")

        print("NEW HASH =", user.password_hash)

        db.session.commit()

        print("COMMIT DONE")

        db.session.commit()

        return jsonify(
            {"success": True, "message": "Password updated successfully"}
        ), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"success": False, "message": str(e)}), 500


# ===============================
# RESET PASSWORD
# ===============================
@auth_bp.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):

    try:
        print("RESET PASSWORD ROUTE HIT")
        print("TOKEN =", token)
        print("DB URL =", db.engine.url)

        user = User.query.filter_by(reset_token=token).first()

        print("USER =", user)

        if not user:
            return jsonify({"success": False, "message": "Invalid reset token"}), 400

        print("OLD HASH =", user.password_hash)

        data = request.get_json()

        print("DATA =", data)

        new_password = data.get("new_password")

        print("NEW PASSWORD =", new_password)

        user.password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")

        print("NEW HASH =", user.password_hash)

        user.reset_token = None
        user.reset_token_expiry = None

        db.session.commit()

        print("COMMIT DONE")

        return jsonify({"success": True, "message": "Password reset successful"}), 200

    except Exception as e:
        db.session.rollback()

        print("ERROR =", e)

        return jsonify({"success": False, "message": str(e)}), 500
