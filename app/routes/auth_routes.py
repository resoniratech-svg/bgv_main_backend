from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
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
        role = "SUPER_ADMIN"

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return jsonify({"error": "Username already exists"}), 409

        new_user = User(
            username=username,
            role=role
        )

        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User registered successfully"
        }), 201

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

        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(
            username=username,
            is_active=True
        ).first()

        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401

     
        access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": "SUPER_ADMIN"}
        )
        return jsonify({
            "access_token": access_token,
            "username": user.username,
            "role": "SUPER_ADMIN"
        }), 200

    except Exception as e:
        print("LOGIN ERROR:", str(e))

        return jsonify({
        "error": str(e)
        }), 500