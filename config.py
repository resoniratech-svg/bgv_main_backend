import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# BASE CONFIG
# ==========================================
class BaseConfig:
    DEBUG = False

    # to send request to candidates
    FRONTEND_URL = os.getenv("FRONTEND_URL")

    # ==============================
    # Database Configuration
    # ==============================
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "bgv_database")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:Akanksha123@127.0.0.1:3306/bgv_database"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ==============================
    # JWT Configuration
    # ==============================
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "bgv_ai_enterprise_jwt_secret_key_2026_secure"
    )

    # Access Token Expiry
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

    # Refresh Token Expiry
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    # Optional (clean error key formatting)
    JWT_ERROR_MESSAGE_KEY = "message"

    # ==============================
    # THIRD PARTY API CONFIG
    # ==============================

    # Surepass
    SUREPASS_BASE_URL = os.getenv("SUREPASS_BASE_URL")
    SUREPASS_API_KEY = os.getenv("SUREPASS_API_KEY")

    # Didit
    DIDIT_BASE_URL = os.getenv("DIDIT_BASE_URL")
    DIDIT_API_KEY = os.getenv("DIDIT_API_KEY")

    # Fama
    FAMA_BASE_URL = os.getenv("FAMA_BASE_URL")
    FAMA_API_KEY = os.getenv("FAMA_API_KEY")

    # Indian Kanoon
    INDIAN_KANOON_BASE_URL = os.getenv("INDIAN_KANOON_BASE_URL")
    INDIAN_KANOON_API_KEY = os.getenv("INDIAN_KANOON_API_KEY")


# ==========================================
# DEVELOPMENT CONFIG
# ==========================================
class DevelopmentConfig(BaseConfig):
    DEBUG = True


# ==========================================
# PRODUCTION CONFIG
# ==========================================
class ProductionConfig(BaseConfig):
    DEBUG = False

    # Production can override expiry if needed
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=9)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


# ==========================================
# CONFIG MAPPING
# ==========================================
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}


Config = config_map.get(
    os.getenv("FLASK_ENV", "development"),
    DevelopmentConfig
)