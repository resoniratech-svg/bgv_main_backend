from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.services.fraud_service import FraudService

fraud_bp = Blueprint("fraud", __name__)

@fraud_bp.route("/cases", methods=["GET"])
# @jwt_required()
def get_fraud_cases():

    data = FraudService.get_fraud_cases()

    return jsonify({
        "status": "success",
        "data": data
    }), 200