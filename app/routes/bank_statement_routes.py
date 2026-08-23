from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.bank_statement_service import BankStatementService

bank_statement_bp = Blueprint("bank_statement", __name__)
###############################################################
# SAVE BANK STATEMENT DETAILS
###############################################################


@bank_statement_bp.route("/details", methods=["POST"])
@jwt_required()
def save_bank_statement_details():

    try:
        data = request.get_json()

        if not data:
            return jsonify(
                {
                    "status": "error",
                    "message": "Request body is required",
                }
            ), 400

        candidate_id = data.get("candidate_id")
        bank_name = data.get("bank_name")
        bank_statement_password = data.get("bank_statement_password")

        if not candidate_id:
            return jsonify(
                {
                    "status": "error",
                    "message": "candidate_id is required",
                }
            ), 400

        if not bank_name or not bank_name.strip():
            return jsonify(
                {
                    "status": "error",
                    "message": "bank_name is required",
                }
            ), 400

        if not bank_statement_password or not bank_statement_password.strip():
            return jsonify(
                {
                    "status": "error",
                    "message": "bank_statement_password is required",
                }
            ), 400

        result = BankStatementService.save_bank_statement_details(
            candidate_id=candidate_id,
            bank_name=bank_name,
            bank_statement_password=bank_statement_password,
        )

        if not result.get("success"):
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as error:
        import traceback

        traceback.print_exc()

        return jsonify(
            {
                "status": "error",
                "message": str(error),
            }
        ), 500


###############################################################
# UPLOAD BANK STATEMENT
###############################################################


@bank_statement_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_bank_statement():

    try:
        data = request.get_json()

        token = request.headers.get("Authorization")

        result = BankStatementService.upload_bank_statement(
            candidate_id=data.get("candidate_id"),
            bgv_id=data.get("bgv_id"),
            document_id=data.get("document_id"),
            token=token,
        )

        return jsonify(result), 200

    except Exception as error:
        return jsonify({"status": "error", "message": str(error)}), 500


###############################################################
# GET BANK STATEMENT RESULT
###############################################################


@bank_statement_bp.route("/result/<int:candidate_id>", methods=["GET"])
@jwt_required()
def get_bank_statement_result(candidate_id):

    try:
        token = request.headers.get("Authorization")

        bgv_id = request.args.get("bgv_id")

        if not bgv_id:
            return jsonify({"status": "error", "message": "bgv_id is required."}), 400

        result = BankStatementService.get_result(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            token=token,
        )

        return jsonify({"status": "success", "data": result}), 200

    except Exception as error:
        return jsonify({"status": "error", "message": str(error)}), 500


###############################################################
# SAVE BANK STATEMENT DECISION
###############################################################


@bank_statement_bp.route("/decision", methods=["POST"])
@jwt_required()
def save_bank_statement_decision():

    try:
        data = request.get_json()

        # =================================================
        # REQUEST BODY VALIDATION
        # =================================================

        if not data:
            return jsonify(
                {
                    "status": "error",
                    "message": "Request body is required",
                }
            ), 400

        # =================================================
        # SAVE DECISION
        # =================================================

        result = BankStatementService.save_decision(data)

        return jsonify(result), 200

    except Exception as error:
        import traceback

        traceback.print_exc()

        return jsonify(
            {
                "status": "error",
                "message": str(error),
            }
        ), 500
