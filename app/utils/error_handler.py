import traceback
from flask import jsonify
from marshmallow import ValidationError


def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({
            "status": "error",
            "errors": e.messages
        }), 400

    @app.errorhandler(Exception)
    def handle_exception(e):
        traceback.print_exc()  # 🔥 PRINT REAL ERROR IN TERMINAL
        return jsonify({
            "status": "error",
            "message": str(e)   # 🔥 SHOW REAL ERROR
        }), 500