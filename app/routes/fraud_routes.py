from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.fraud_service import FraudService

fraud_bp = Blueprint("fraud", __name__)


@fraud_bp.route("/cases", methods=["GET"])
def get_fraud_cases():

    data = FraudService.get_fraud_cases()

    return jsonify({"status": "success", "data": data}), 200


@fraud_bp.route("/cases/<int:candidate_id>", methods=["GET"])
def get_case(candidate_id):

    data = FraudService.get_case(candidate_id)

    return jsonify({"status": "success", "data": data})


@fraud_bp.route("/approve/<int:candidate_id>", methods=["PUT"])
def approve_case(candidate_id):

    data = request.get_json()

    module = data.get("module")

    FraudService.approve_case(candidate_id, module)

    return jsonify({"status": "success"})


@fraud_bp.route("/reject/<int:candidate_id>", methods=["PUT"])
def reject_case(candidate_id):

    data = request.get_json()

    module = data.get("module")

    FraudService.reject_case(candidate_id, module)

    return jsonify({"status": "success"})


@fraud_bp.route("/reverify/<int:candidate_id>", methods=["PUT"])
def reverify(candidate_id):

    data = request.get_json()

    module = data.get("module")

    FraudService.request_reverification(candidate_id, module)

    return jsonify({"status": "success"})
