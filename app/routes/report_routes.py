from flask import (
    Blueprint,
    jsonify,
    request,
    send_file
)
from io import BytesIO
from flask_jwt_extended import jwt_required
from app.reporting.report_service import ReportService
from app.utils.rbac import role_required
from flask import send_file
from io import BytesIO
from app.services.ai_service_connector import (
    AIServiceConnector
)
from app.repositories.report_repository import (
    ReportRepository
)
report_bp = Blueprint("report", __name__)


@report_bp.route("", methods=["GET"])
@jwt_required()
def get_all_reports():

    data = ReportService.get_all_reports()

    return jsonify({
        "status": "success",
        "data": data
    }), 200
@report_bp.route(
    "/generate/<int:candidate_id>",
    methods=["POST"]
)
@jwt_required()
@role_required(
    "Admin",
    "Compliance",
    "SUPER_ADMIN"
)
def generate_pdf_report(candidate_id):

    result = (
        AIServiceConnector.generate_report(
            candidate_id
        )
    )

    return jsonify(result), 200

@report_bp.route("/<int:bgv_id>", methods=["GET"])
@jwt_required()
@role_required(
    "Admin",
    "Compliance",
    "SUPER_ADMIN"
)
def generate_report(bgv_id):

    data = ReportService.generate_report(bgv_id)

    return jsonify({
        "status": "success",
        "data": data
    }), 200

@report_bp.route(
    "/download/<int:candidate_id>",
    methods=["GET"]
)
@jwt_required()
@role_required(
    "Admin",
    "Compliance",
    "SUPER_ADMIN"
)
def download_pdf_report(candidate_id):

    token = request.headers.get(
        "Authorization"
    )

    response = (
        AIServiceConnector
        .download_report(
            candidate_id,
            token
        )
    )

    if response.status_code != 200:

        return jsonify({
            "status": "failed",
            "message": "Report not found"
        }), response.status_code

    filename = (
        response.headers.get(
            "X-Report-Name"
        )
        or
        f"candidate_{candidate_id}.pdf"
    )

    report = (
        ReportRepository
        .get_latest_report_by_candidate(
            candidate_id
        )
    )
    print(report)
    response = send_file(
        BytesIO(response.content),
        as_attachment=True,
        download_name=report["file_name"],
        mimetype="application/pdf"
    )

    response.headers[
        "Access-Control-Expose-Headers"
    ] = "Content-Disposition"

    return response