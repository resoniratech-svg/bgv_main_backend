from flask import Flask, app
from flask_cors import CORS
from sqlalchemy import text

from app.config import Config
from app.extensions import db, jwt, bcrypt, migrate, limiter
from app.routes.candidate_routes import candidate_bp
# ==============================
# Blueprints
# ==============================
from app.routes.auth_routes import auth_bp
from app.routes.verification_type_routes import verification_type_bp

from app.routes.dashboard_routes import dashboard_bp
from app.routes.report_routes import report_bp
from app.routes.compliance_routes import compliance_bp
from app.routes.passport_routes import passport_bp
from app.routes.court_routes import court_bp
from app.routes.din_routes import din_bp
from app.routes.global_database_routes import global_database_bp
from app.routes.reference_routes import reference_bp
from app.routes.credit_check_routes import credit_check_bp
from app.routes.aadhaar_routes import aadhaar_bp
from app.routes.pan_routes import pan_bp
from app.routes.employment_routes import employment_bp
from app.routes.education_routes import education_bp
from app.routes.face_match_routes import face_match_bp
from app.routes.ocr_routes import ocr_bp
from app.routes.resume_routes import resume_bp
from app.routes.bgv_routes import bgv_bp
from app.routes.candidate_link_routes import candidate_link_bp
from app.routes.document_routes import document_bp
from app.routes.health_routes import health_bp
from app.routes.pdf_report_routes import (
    pdf_report_bp
)
from app.routes.didit_routes import (
    didit_bp
)

from app.routes.driving_license_routes import (
    driving_license_bp
)

from app.routes.deepfake_routes import (

    deepfake_bp

)


# ==============================
# Utils
# ==============================
from app.utils.error_handler import register_error_handlers
from app.utils.logger import setup_logger
from app.routes.submission_routes import (
    submission_bp
)
# ==============================
# Import Models
# ==============================
from app.models import (
    User,
    BGVRequest,
    VerificationResult,
    VerificationType,
    AuditLog
)


def create_app():

    app = Flask(__name__)

    print("CREATE_APP IS EXECUTING")

    # ==============================
    # Root Route
    # ==============================
    @app.route("/")
    def home():
        return {
            "message": "BGV Service Running Successfully"
        }

    # ==============================
    # Load Config
    # ==============================
    app.config.from_object(Config)

    # ==============================
    # Enable CORS
    # ==============================
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "*"
            }
        }
    )

    # ==============================
    # Initialize Extensions
    # ==============================
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    # ==============================
    # Register Blueprints
    # ==============================

    # Authentication APIs
    app.register_blueprint(
        auth_bp,
        url_prefix="/api/v1/auth"
    )
    # BGV APIs
    app.register_blueprint(
        bgv_bp,
        url_prefix="/api/v1/bgv"
    )

    # Verification Type APIs
    app.register_blueprint(
        verification_type_bp,
        url_prefix="/api/v1/verification-types"
    )

    
    # Dashboard APIs
    app.register_blueprint(
        dashboard_bp,
        url_prefix="/api/v1/dashboard"
    )

    # Report APIs
    app.register_blueprint(
        report_bp,
        url_prefix="/api/v1/report"
    )

    # Compliance APIs
    app.register_blueprint(
        compliance_bp,
        url_prefix="/api/v1/compliance"
    )
    app.register_blueprint(
        passport_bp,
        url_prefix="/api/v1/passport"
    )
    app.register_blueprint(
        court_bp,
        url_prefix="/api/v1/court"
    )
    
    app.register_blueprint(
        din_bp,
        url_prefix="/api/v1/din"
    )
    app.register_blueprint(
        global_database_bp,
        url_prefix="/api/v1/global_database"
    )
    app.register_blueprint(
        reference_bp,
        url_prefix="/api/v1/reference"
    )
    app.register_blueprint(
        credit_check_bp,
        url_prefix="/api/v1/credit_check"
    )
    app.register_blueprint(
        candidate_bp,
        url_prefix="/api/v1"
    )
    app.register_blueprint(
        candidate_link_bp,
        url_prefix="/api/v1"
    )
    app.register_blueprint(
        document_bp,
        url_prefix="/api/v1"
    )
    app.register_blueprint(
        submission_bp,
        url_prefix="/api/v1"
    )
    app.register_blueprint(
        health_bp,
        url_prefix="/api/v1"
    )
    app.register_blueprint(
        pdf_report_bp,
        url_prefix="/api/v1"
    )
    app.register_blueprint(
        didit_bp,
        url_prefix="/api/v1"
    )
 

    app.register_blueprint(
    driving_license_bp,
    url_prefix="/api/v1/driving-license"
)
    app.register_blueprint(

    face_match_bp,

    url_prefix="/api/v1"

)

    app.register_blueprint(aadhaar_bp, url_prefix="/api/v1/aadhaar")
    app.register_blueprint(pan_bp, url_prefix="/api/v1/pan")
    app.register_blueprint(employment_bp, url_prefix="/api/v1/employment")
    app.register_blueprint(education_bp, url_prefix="/api/v1/education")
    
    app.register_blueprint(ocr_bp, url_prefix="/api/v1")
    app.register_blueprint(resume_bp, url_prefix="/api/v1/resume")
    
    app.register_blueprint(

    deepfake_bp,

    url_prefix="/api/v1/deepfake"

)
    # ==============================
    # Logger
    # ==============================
    setup_logger(app)

    # ==============================
    # Error Handlers
    # ==============================
    register_error_handlers(app)

    # ==============================
    # Database Health Check
    # ==============================
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            print("Database connection successful.")
            db.create_all()
            print("Database tables initialized successfully.")
        except Exception as e:
            print(f"Database connection failed: {str(e)}")

    # ==============================
    # Print Registered Routes
    # ==============================
    print("\n==============================")
    print("REGISTERED ROUTES")
    print("==============================")

    for rule in app.url_map.iter_rules():
        print(rule)

    print("==============================\n")

    return app