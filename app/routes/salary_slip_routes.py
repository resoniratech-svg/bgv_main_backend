from flask import Blueprint
from flask import request
from flask import jsonify

from flask_jwt_extended import (
    jwt_required
)

from app.services.salary_slip_service import (
    SalarySlipService
)


salary_slip_bp = Blueprint(

    "salary_slip",

    __name__

)


###############################################################
# SALARY SLIP OCR
###############################################################

@salary_slip_bp.route(

    "/ocr",

    methods=["POST"]

)
@jwt_required()
def verify_salary_slip():

    try:

        ###################################################
        # REQUEST
        ###################################################

        data = request.get_json()

        if not data:

            return jsonify({

                "status": "error",

                "message": "Request body is required."

            }), 400

        ###################################################
        # INPUTS
        ###################################################

        candidate_id = data.get(

            "candidate_id"

        )

        bgv_id = data.get(

            "bgv_id"

        )

        document_id = data.get(

            "document_id"

        )

        token = request.headers.get(

            "Authorization"

        )

        ###################################################
        # OCR
        ###################################################

        result = (

            SalarySlipService
            .verify_salary_slip(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                document_id=document_id,

                token=token

            )

        )

        return jsonify(

            result

        ), 200

    except Exception as error:

        print("=" * 80)
        print("SALARY SLIP OCR ERROR")
        print(error)
        print("=" * 80)

        return jsonify({

            "status": "error",

            "message": str(error)

        }), 500


###############################################################
# GET SALARY SLIP OCR RESULT
###############################################################

@salary_slip_bp.route(

    "/result/<int:candidate_id>",

    methods=["GET"]

)
@jwt_required()
def get_salary_slip_result(

        candidate_id

):

    try:

        token = request.headers.get(

            "Authorization"

        )

        result = (

            SalarySlipService
            .get_result(

                candidate_id,

                token

            )

        )

        return jsonify(

            result

        ), 200

    except Exception as error:

        print("=" * 80)
        print("SALARY SLIP RESULT ERROR")
        print(error)
        print("=" * 80)

        return jsonify({

            "status": "error",

            "message": str(error)

        }), 500