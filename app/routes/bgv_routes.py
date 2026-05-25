from flask import Blueprint, request, jsonify

from app.services.bgv_service import BGVService


bgv_bp = Blueprint(
    "bgv_bp",
    __name__
)


@bgv_bp.route("/create", methods=["POST"])
def create_bgv_request():

    try:

        data = request.get_json()

        result = BGVService.create_bgv_request(data)

        if result["status"] == "error":

            return jsonify(result), 400

        return jsonify(result), 201

    except Exception as e:

        error_message = str(e)

        if "foreign key constraint fails" in error_message.lower():

            return jsonify({
                "status": "error",
                "message": "Invalid candidate_id"
            }), 400

        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500