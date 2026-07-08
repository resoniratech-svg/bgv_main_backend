from flask import Blueprint
from flask import request
from flask import jsonify

from flask_jwt_extended import (
    jwt_required
)

from app.services.ccrv_service import (
    CCRVService
)


ccrv_bp = Blueprint(

    "ccrv",

    __name__

)


# ======================================================
# VERIFY CCRV
# ======================================================

@ccrv_bp.route(

    "/verify",

    methods=["POST"]

)
@jwt_required()
def verify_ccrv():

    try:

        data = request.get_json()

        candidate_id = data.get(

            "candidate_id"

        )

        bgv_id = data.get(

            "bgv_id"

        )

        token = request.headers.get(

            "Authorization"

        )

        result = (

            CCRVService

            .verify_ccrv(

                candidate_id,

                bgv_id,

                token

            )

        )

        return jsonify(result)

    except Exception as e:

        return jsonify(

            {

                "status": "error",

                "message": str(e)

            }

        ), 500


# ======================================================
# GET CCRV RESULT
# ======================================================

@ccrv_bp.route(

    "/result/<int:candidate_id>",

    methods=["GET"]

)
@jwt_required()
def get_ccrv_result(

        candidate_id

):

    try:

        token = request.headers.get(

            "Authorization"

        )

        result = (

            CCRVService

            .get_result(

                candidate_id,

                token

            )

        )

        return jsonify(result)

    except Exception as e:

        return jsonify(

            {

                "status": "error",

                "message": str(e)

            }

        ), 500