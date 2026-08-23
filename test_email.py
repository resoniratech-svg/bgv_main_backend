from app.services.email_service import (
    EmailService
)

EmailService.send_admin_alert(
    "BGV TEST",
    "Admin mail working"
)