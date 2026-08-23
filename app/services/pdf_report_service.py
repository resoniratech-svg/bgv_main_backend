from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

import os


class PDFReportService:

    REPORT_FOLDER = "generated_reports"

    @staticmethod
    def generate_sample_report():

        os.makedirs(
            PDFReportService.REPORT_FOLDER,
            exist_ok=True
        )

        file_path = os.path.join(

            PDFReportService.REPORT_FOLDER,

            "sample_bgv_report.pdf"
        )

        document = SimpleDocTemplate(
            file_path
        )

        styles = getSampleStyleSheet()

        elements = []

        title = Paragraph(

            "BGV Verification Report",

            styles["Title"]
        )

        elements.append(title)

        elements.append(
            Spacer(1, 20)
        )

        candidate_info = Paragraph(

            "Candidate: John Doe",

            styles["BodyText"]
        )

        elements.append(
            candidate_info
        )

        document.build(elements)

        return {
            "status": "success",
            "file_path": file_path
        }