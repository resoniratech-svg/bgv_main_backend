from flask import Blueprint, jsonify, request, send_file
from io import BytesIO
from flask_jwt_extended import jwt_required
from app.reporting.report_service import ReportService
from app.utils.rbac import role_required
from flask import send_file
from io import BytesIO
from app.services.ai_service_connector import AIServiceConnector
from app.repositories.report_repository import ReportRepository

report_bp = Blueprint("report", __name__)


@report_bp.route("", methods=["GET"])
@jwt_required()
def get_all_reports():

    data = ReportService.get_all_reports()

    return jsonify({"status": "success", "data": data}), 200


@report_bp.route("/generate/<int:candidate_id>", methods=["POST"])
@jwt_required()
@role_required("Admin", "Compliance", "SUPER_ADMIN")
def generate_pdf_report(candidate_id):

    result = AIServiceConnector.generate_report(candidate_id)

    return jsonify(result), 200


@report_bp.route("/<int:bgv_id>", methods=["GET"])
@jwt_required()
@role_required("Admin", "Compliance", "SUPER_ADMIN")
def generate_report(bgv_id):

    data = ReportService.generate_report(bgv_id)

    return jsonify({"status": "success", "data": data}), 200


@report_bp.route("/download/<int:candidate_id>", methods=["GET"])
@jwt_required()
@role_required("Admin", "Compliance", "SUPER_ADMIN")
def download_pdf_report(candidate_id):

    try:
        token = request.headers.get("Authorization")

        response = AIServiceConnector.download_report(candidate_id, token)

        if response.status_code != 200:
            return jsonify(
                {"status": "failed", "message": "Report not found"}
            ), response.status_code

        report = ReportRepository.get_latest_report_by_candidate(candidate_id)

        from app.services.audit_service import AuditService

        AuditService.log_action(
            action="DOWNLOAD_REPORT",
            module_name="REPORTS",
            entity_type="candidate",
            entity_id=candidate_id,
            status="SUCCESS",
            remarks="Downloaded BGV report",
        )

        response = send_file(
            BytesIO(response.content),
            as_attachment=True,
            download_name=report["file_name"],
            mimetype="application/pdf",
        )

        response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"

        return response

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify({"status": "error", "message": str(e)}), 500


@report_bp.route("/view/<int:candidate_id>", methods=["GET"])
@jwt_required()
@role_required("Admin", "Compliance", "SUPER_ADMIN")
def view_report(candidate_id):

    try:
        report = ReportService.get_report_view(candidate_id)

        return jsonify({"status": "success", "data": report}), 200

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify({"status": "failed", "message": str(e)}), 500


from openpyxl import Workbook
from io import BytesIO
from flask import send_file


@report_bp.route("/export", methods=["GET"])
@jwt_required()
@role_required("Admin", "Compliance", "SUPER_ADMIN")
def export_reports():

    reports = ReportService.get_all_reports()

    wb = Workbook()
    ws = wb.active
    ws.title = "Reports"

    ws.append(
        [
            "Candidate ID",
            "Candidate Name",
            "Report Name",
            "Verification Status",
            "Generated At",
        ]
    )

    for report in reports:
        ws.append(
            [
                report.get("candidate_id"),
                report.get("candidate_name"),
                report.get("report_name"),
                report.get("verification_status"),
                report.get("generated_at"),
            ]
        )

    output = BytesIO()

    wb.save(output)

    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="Verification_Reports.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
