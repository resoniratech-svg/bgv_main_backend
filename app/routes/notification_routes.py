from flask import Blueprint, jsonify

from app.services.notification_service import NotificationService

notification_bp = Blueprint(
    "notification",
    __name__,
)


@notification_bp.route("/", methods=["GET"])
def get_notifications():

    notifications = NotificationService.get_notifications()

    return jsonify(
        {
            "status": "success",
            "data": notifications,
        }
    )


@notification_bp.route("/<int:notification_id>/read", methods=["PATCH"])
def mark_as_read(notification_id):

    NotificationService.mark_as_read(notification_id)

    return jsonify(
        {
            "status": "success",
            "message": "Notification marked as read.",
        }
    )


@notification_bp.route("/read-all", methods=["PATCH"])
def mark_all_as_read():

    NotificationService.mark_all_as_read()

    return jsonify(
        {
            "status": "success",
            "message": "All notifications marked as read.",
        }
    )
