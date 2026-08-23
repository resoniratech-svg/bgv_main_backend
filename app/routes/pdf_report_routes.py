from flask import Blueprint, jsonify

from app.services.pdf_report_service import (
    PDFReportService
)

pdf_report_bp = Blueprint(
    "pdf_report_bp",
    __name__
)


@pdf_report_bp.route(
    "/reports/generate-sample",
    methods=["GET"]
)
def generate_sample_report():

    try:

        result = (
            PDFReportService.generate_sample_report()
        )

        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500