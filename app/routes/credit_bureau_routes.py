from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from app.services.credit_bureau_service import (
    CreditBureauService
)

credit_bureau_bp = Blueprint(
    "credit_bureau",
    __name__
)


###############################################################
# VERIFY CREDIT BUREAU
###############################################################

@credit_bureau_bp.route("/verify", methods=["POST"])
@jwt_required()
def verify_credit_bureau():

    try:

        data = request.get_json()

        token = request.headers.get("Authorization")

        result = CreditBureauService.verify_credit_bureau(

            candidate_id=data.get("candidate_id"),

            bgv_id=data.get("bgv_id"),

            token=token

        )

        return jsonify(result), 200

    except Exception as error:

        return jsonify({

            "status": "error",

            "message": str(error)

        }), 500


###############################################################
# GET CREDIT BUREAU RESULT
###############################################################

@credit_bureau_bp.route("/result/<int:candidate_id>", methods=["GET"])
@jwt_required()
def get_credit_bureau_result(candidate_id):

    try:

        token = request.headers.get("Authorization")

        result = CreditBureauService.get_result(

            candidate_id,

            token

        )

        return jsonify({

            "status": "success",

            "data": result

        }), 200

    except Exception as error:

        return jsonify({

            "status": "error",

            "message": str(error)

        }), 500