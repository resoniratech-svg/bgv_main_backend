from flask import Blueprint, request, jsonify

from app.services.didit_service import (
    DiditService
)

didit_bp = Blueprint(
    "didit_bp",
    __name__
)


@didit_bp.route(
    "/didit/create-session",
    methods=["POST"]
)
def create_session():

    try:

        data = request.json

        workflow_id = data.get(
            "workflow_id"
        )

        candidate_id = data.get(
            "candidate_id"
        )

        callback_url = data.get(
            "callback_url"
        )

        result = (
            DiditService.create_verification_session(

                workflow_id=workflow_id,

                candidate_id=candidate_id,

                callback_url=callback_url
            )
        )

        return jsonify(result), 200

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)
        }), 500