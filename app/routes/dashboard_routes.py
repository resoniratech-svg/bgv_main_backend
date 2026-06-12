from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.dashboard.dashboard_service import DashboardService
from app.utils.rbac import role_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/summary", methods=["GET"])
@jwt_required()
@role_required("SUPER_ADMIN")
def summary():
    data = DashboardService.get_summary()

    return jsonify({
        "status": "success",
        "data": data
    }), 200


@dashboard_bp.route("/candidate/<int:candidate_id>", methods=["GET"])
@jwt_required()
def candidate_history(candidate_id):

    data = DashboardService.get_candidate_history(candidate_id)

    return jsonify({
        "status": "success",
        "data": data
    }), 200