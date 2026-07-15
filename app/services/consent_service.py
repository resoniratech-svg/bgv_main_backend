from app.services.ai_service_connector import (
    AIServiceConnector
)


class ConsentService:

    ########################################################
    # SAVE CANDIDATE CONSENT
    ########################################################

    @staticmethod
    def save_candidate_consent(

        candidate_id,
        bgv_id,
        verification_type,
        consent_status,
        consent_text,
        consent_version,
        consent_source,
        token

    ):

        return (

            AIServiceConnector
            .save_candidate_consent(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                verification_type=verification_type,

                consent_status=consent_status,

                consent_text=consent_text,

                consent_version=consent_version,

                consent_source=consent_source,

                token=token

            )

        )

    ########################################################
    # GET CANDIDATE CONSENT
    ########################################################

    @staticmethod
    def get_candidate_consent(

        candidate_id,
        bgv_id,
        verification_type,
        token

    ):

        return (

            AIServiceConnector
            .get_candidate_consent(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                verification_type=verification_type,

                token=token

            )

        )