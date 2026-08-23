from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# 🔹 Database
db = SQLAlchemy()

# 🔹 JWT Authentication
jwt = JWTManager()

# 🔹 Password Hashing
bcrypt = Bcrypt()

# 🔹 Database Migrations
migrate = Migrate()

# 🔹 Rate Limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)