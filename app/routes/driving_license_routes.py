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


# =====================================================
# VERIFY DRIVING LICENSE
# =====================================================

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

        ########################################
        # VALIDATIONS
        ########################################

        if not candidate_id:

            return jsonify({

                "status": "error",

                "message": "candidate_id is required"

            }), 400

        if not bgv_id:

            return jsonify({

                "status": "error",

                "message": "bgv_id is required"

            }), 400

        if not front_document_id:

            return jsonify({

                "status": "error",

                "message": "front_document_id is required"

            }), 400

        if not back_document_id:

            return jsonify({

                "status": "error",

                "message": "back_document_id is required"

            }), 400

        ########################################
        # VERIFY
        ########################################

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

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# =====================================================
# GET RESULT
# =====================================================

@driving_license_bp.route(

    "/result/<int:candidate_id>",

    methods=["GET"]

)
@jwt_required()
def get_result(

    candidate_id

):

    try:

        token = request.headers.get(

            "Authorization"

        )

        result = (

            DrivingLicenseService

            .get_result(

                candidate_id,

                token

            )

        )

        return jsonify(

            result

        )

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500