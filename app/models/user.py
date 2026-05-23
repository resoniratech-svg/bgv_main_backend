from datetime import datetime
from app.extensions import db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(50),
        nullable=False,
        default="recruiter"
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # =========================
    # HASH PASSWORD
    # =========================
    def set_password(self, raw_password: str):
        self.password_hash = bcrypt.generate_password_hash(
            raw_password
        ).decode("utf-8")

    # =========================
    # VERIFY PASSWORD
    # =========================
    def check_password(self, raw_password: str) -> bool:
        return bcrypt.check_password_hash(
            self.password_hash,
            raw_password
        )

    # =========================
    # JSON RESPONSE
    # =========================
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<User {self.username}>"