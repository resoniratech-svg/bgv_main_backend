from app.models.consent_record import ConsentRecord
from app.utils.exceptions import FraudException


class ConsentService:

    @staticmethod
    def validate_consent(candidate_id):
        consent = ConsentRecord.query.filter_by(
            candidate_id=candidate_id,
            consent_status=True
        ).first()

        if not consent:
            raise FraudException(
                "Consent not provided for this candidate",
                403
            )

        return True
