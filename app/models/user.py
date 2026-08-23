from datetime import datetime
from app.extensions import db, bcrypt


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False, index=True)

    password_hash = db.Column(db.String(255), nullable=False)

    full_name = db.Column(db.String(255), nullable=True)

    email = db.Column(db.String(255), unique=True, nullable=True)

    phone = db.Column(db.String(20), nullable=True)

    role = db.Column(db.String(50), nullable=False, default="SUPER_ADMIN")

    is_active = db.Column(db.Boolean, default=True, nullable=False)

    last_login = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    created_by = db.Column(db.Integer, nullable=True)

    reset_token = db.Column(db.String(255), nullable=True)

    reset_token_expiry = db.Column(db.DateTime, nullable=True)

    # =========================
    # HASH PASSWORD
    # =========================
    def set_password(self, raw_password: str):

        self.password_hash = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    # =========================
    # VERIFY PASSWORD
    # =========================
    def check_password(self, raw_password: str) -> bool:

        return bcrypt.check_password_hash(self.password_hash, raw_password)

    # =========================
    # JSON RESPONSE
    # =========================
    def to_dict(self):

        return {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "is_active": self.is_active,
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S")
            if self.last_login
            else None,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.created_at
            else None,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.updated_at
            else None,
            "created_by": self.created_by,
        }

    def __repr__(self):

        return f"<User {self.username}>"
