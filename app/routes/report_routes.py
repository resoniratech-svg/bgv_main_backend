from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.reporting.report_service import ReportService
from app.utils.rbac import role_required


report_bp = Blueprint("report", __name__)


@report_bp.route("/<int:bgv_id>", methods=["GET"])
@jwt_required()
@role_required("Admin", "Compliance")
def generate_report(bgv_id):

    data = ReportService.generate_report(bgv_id)

    return jsonify({
        "status": "success",
        "data": data
    }), 200