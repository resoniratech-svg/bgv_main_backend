from flask import Blueprint
from flask import request
from flask import jsonify

from flask_jwt_extended import (
    jwt_required
)

from app.services.driving_license_service import (
    DrivingLicenseService
)

driving_license_bp = Blueprint(

    "driving_license",

    __name__
)


@driving_license_bp.route(
    "/verify",
    methods=["POST"]
)
@jwt_required()
def verify_driving_license():

    try:

        data = request.get_json()

        candidate_id = data.get(
            "candidate_id"
        )

        bgv_id = data.get(
            "bgv_id"
        )

        front_document_id = data.get(
            "front_document_id"
        )

        back_document_id = data.get(
            "back_document_id"
        )

        token = request.headers.get(
            "Authorization"
        )

        result = (

            DrivingLicenseService
            .verify_driving_license(

                candidate_id=
                candidate_id,

                bgv_id=
                bgv_id,

                front_document_id=
                front_document_id,

                back_document_id=
                back_document_id,

                token=
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