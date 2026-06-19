from flask import Blueprint

from flask import request

from flask import jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt
)

from app.services.pan_service import (
    PanService
)

pan_bp = Blueprint(

    "pan",

    __name__
)


@pan_bp.route(

    "/verify",

    methods=["POST"]
)
@jwt_required()
def verify_pan():

    try:

        data = request.get_json()

        token = request.headers.get(
            "Authorization"
        )

        result = (
            PanService
            .verify_pan(

                data=data,

                token=token
            )
        )

        if result.get(
            "status"
        ) == "error":

            return jsonify(
                result
            ), 400

        return jsonify(
            result
        ), 200

    except Exception as error:

        return jsonify({

            "status": "error",

            "message": str(
                error
            )
        }), 500