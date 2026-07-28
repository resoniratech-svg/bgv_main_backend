from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.bank_statement_service import (
    BankStatementService
)

bank_statement_bp = Blueprint(

    "bank_statement",

    __name__

)

###############################################################
# UPLOAD BANK STATEMENT
###############################################################

@bank_statement_bp.route(

    "/upload",

    methods=["POST"]

)
@jwt_required()
def upload_bank_statement():

    try:

        data = request.get_json()

        token = request.headers.get(

            "Authorization"

        )

        result = (

            BankStatementService
            .upload_bank_statement(

                candidate_id=data.get(

                    "candidate_id"

                ),

                bgv_id=data.get(

                    "bgv_id"

                ),
                document_id=data.get("document_id"),

                token=token

            )

        )

        return jsonify(

            result

        ), 200

    except Exception as error:

        return jsonify({

            "status": "error",

            "message": str(error)

        }), 500


###############################################################
# GET BANK STATEMENT RESULT
###############################################################

@bank_statement_bp.route(

    "/result/<int:candidate_id>",

    methods=["GET"]

)
@jwt_required()
def get_bank_statement_result(

        candidate_id

):

    try:

        token = request.headers.get(

            "Authorization"

        )

        result = (

            BankStatementService
            .get_result(

                candidate_id,

                token

            )

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