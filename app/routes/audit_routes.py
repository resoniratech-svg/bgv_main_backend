from flask import Blueprint, jsonify
from sqlalchemy import func
from app.models.audit_log import AuditLog
from app.models.user import User
from app.repositories.candidate_repository import CandidateRepository

audit_bp = Blueprint("audit", __name__)


# ---------------------------------------------------------
# Get All Logs
# ---------------------------------------------------------
@audit_bp.route("/logs", methods=["GET"])
def get_logs():
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).all()
    print("TOTAL LOGS:", len(logs))
    response_data = []

    for log in logs:
        user_name = "System"
        candidate_name = None
        affected_name = None
        affected_id = None
        affected_user = None
        if log.user_id:
            user = User.query.get(log.user_id)

            if user:
                user_name = user.username

        if log.entity_type == "user":
            affected_id = log.entity_id

            # -----------------------------
            # DELETE USER
            # -----------------------------
            if log.action == "DELETE_USER":
                if log.old_values:
                    affected_name = log.old_values.get(
                        "username"
                    ) or log.old_values.get("full_name")

            # -----------------------------
            # UPDATE USER
            # -----------------------------
            elif log.action == "UPDATE_USER":
                if log.new_values:
                    affected_name = log.new_values.get(
                        "username"
                    ) or log.new_values.get("full_name")

                if not affected_name and log.old_values:
                    affected_name = log.old_values.get(
                        "username"
                    ) or log.old_values.get("full_name")

                if not affected_name:
                    affected_user = User.query.get(log.entity_id)

                    if affected_user:
                        affected_name = affected_user.username

            # -----------------------------
            # USER STATUS CHANGED
            # -----------------------------
            elif log.action == "USER_STATUS_CHANGED":
                if log.new_values:
                    affected_name = log.new_values.get(
                        "username"
                    ) or log.new_values.get("full_name")

                if not affected_name and log.old_values:
                    affected_name = log.old_values.get(
                        "username"
                    ) or log.old_values.get("full_name")

                if not affected_name:
                    affected_user = User.query.get(log.entity_id)

                    if affected_user:
                        affected_name = affected_user.username

            # -----------------------------
            # OTHER USER EVENTS
            # -----------------------------
            else:
                affected_user = User.query.get(log.entity_id)

                if affected_user:
                    affected_name = affected_user.username

        if log.entity_type == "candidate" and log.entity_id:
            candidate = CandidateRepository.get_candidate_by_id(log.entity_id)

            if candidate:
                candidate_name = f"{candidate['first_name']} {candidate['last_name']}"
        print(log.id, log.action, log.entity_type)
        response_data.append(
            {
                "id": log.id,
                "event": log.action,
                "module": log.module_name,
                "user_name": user_name,
                "candidate_name": candidate_name,
                "candidate_id": log.entity_id,
                "affected_user_name": affected_name,
                "affected_user_id": affected_id,
                "status": log.status,
                "created_at": log.created_at.isoformat(),
                "changes": log.changes,
                "old_values": log.old_values,
                "new_values": log.new_values,
                "remarks": log.remarks,
                "entity_type": log.entity_type,
            }
        )

    return jsonify({"success": True, "data": response_data}), 200


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------
@audit_bp.route("/stats", methods=["GET"])
def get_stats():
    total = AuditLog.query.count()
    success = AuditLog.query.filter(func.upper(AuditLog.status) == "SUCCESS").count()
    warning = AuditLog.query.filter(func.upper(AuditLog.status) == "WARNING").count()
    critical = AuditLog.query.filter(func.upper(AuditLog.status) == "CRITICAL").count()

    return jsonify(
        {
            "success": True,
            "data": {
                "total": total,
                "success": success,
                "warning": warning,
                "critical": critical,
            },
        }
    ), 200


from flask import send_file
from openpyxl import Workbook
from io import BytesIO


@audit_bp.route("/export", methods=["GET"])
def export_audit_logs():

    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Audit Logs"

    ws.append(
        [
            "ID",
            "Event",
            "Module",
            "Performed By",
            "Candidate",
            "Status",
            "Remarks",
            "Date & Time",
        ]
    )

    for log in logs:
        user_name = "System"

        if log.user_id:
            user = User.query.get(log.user_id)
            if user:
                user_name = user.username

        candidate_name = ""

        if log.entity_type == "candidate":
            candidate = CandidateRepository.get_candidate_by_id(log.entity_id)

            if candidate:
                candidate_name = candidate["first_name"] + " " + candidate["last_name"]

        ws.append(
            [
                log.id,
                log.action,
                log.module_name,
                user_name,
                candidate_name,
                log.status,
                log.remarks,
                log.created_at.strftime("%d-%m-%Y %I:%M:%S %p"),
            ]
        )

    output = BytesIO()

    wb.save(output)

    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="Audit_Logs.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
