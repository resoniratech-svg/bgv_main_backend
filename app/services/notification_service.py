from app.repositories.notification_repository import NotificationRepository


class NotificationService:
    @staticmethod
    def create_notification(
        candidate_id=None,
        bgv_id=None,
        title="",
        description="",
        notification_type="Info",
    ):

        data = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "title": title,
            "description": description,
            "type": notification_type,
        }

        return NotificationRepository.create_notification(data)

    @staticmethod
    def get_notifications():

        return NotificationRepository.get_notifications()

    @staticmethod
    def mark_as_read(notification_id):

        return NotificationRepository.mark_as_read(notification_id)

    @staticmethod
    def mark_all_as_read():

        return NotificationRepository.mark_all_as_read()
