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
        import traceback

        traceback.print_exc()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

        