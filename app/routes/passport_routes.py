from flask import Blueprint
from flask import request
from flask import jsonify

from flask_jwt_extended import (
    jwt_required
)

from app.services.passport_service import (
    PassportService
)

passport_bp = Blueprint(

    "passport",

    __name__
)


@passport_bp.route(
    "/verify",
    methods=["POST"]
)
@jwt_required()
def verify_passport():

    try:

        data = request.get_json()

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

        result = (

            PassportService
            .verify_passport(

                candidate_id,
                bgv_id,
                document_id,
                token

            )

        )

        return jsonify(
            result
        )

    except Exception as error:

        return jsonify({

            "status": "error",

            "message":
            str(error)

        }), 500