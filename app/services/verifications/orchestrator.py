import logging

from app.services.verifications.employment_service import EmploymentVerificationService
# Later:
# from app.services.verifications.education_service import EducationVerificationService
# from app.services.verifications.id_service import IDVerificationService
# from app.services.verifications.address_service import AddressVerificationService

logger = logging.getLogger(__name__)


class VerificationOrchestrator:
    """
    Central Orchestrator for all verification modules.
    Responsible for:
    - Routing to correct module
    - Validating response structure
    - Logging execution
    - Raising controlled errors
    """

    # Central Module Registry
    MODULE_MAP = {
        "Employment": EmploymentVerificationService,
        # "Education": EducationVerificationService,
        # "ID": IDVerificationService,
        # "Address": AddressVerificationService,
    }

    REQUIRED_RESPONSE_KEYS = {
        "verification_type",
        "status",
        "module_score",
        "remarks",
    }

    @classmethod
    def execute_module(cls, verification_type: str, data: dict) -> dict:
        """
        Executes a verification module based on verification_type.
        """

        if not verification_type:
            raise ValueError("verification_type is required")

        if not isinstance(data, dict):
            raise ValueError("data must be a dictionary")

        # Normalize input
        verification_type = verification_type.strip()

        service_class = cls.MODULE_MAP.get(verification_type)

        if not service_class:
            logger.warning(f"Unsupported verification type: {verification_type}")
            raise ValueError(f"Unsupported verification type: {verification_type}")

        try:
            logger.info(f"Executing {verification_type} verification module")

            service = service_class()
            result = service.execute(data)

            if not isinstance(result, dict):
                raise ValueError("Verification module must return a dictionary")

            if not cls.REQUIRED_RESPONSE_KEYS.issubset(result.keys()):
                missing_keys = cls.REQUIRED_RESPONSE_KEYS - result.keys()
                raise ValueError(
                    f"Verification module response missing keys: {missing_keys}"
                )

            logger.info(
                f"{verification_type} module executed successfully "
                f"with score {result.get('module_score')}"
            )

            return result

        except Exception as e:
            logger.error(
                f"Error executing verification module {verification_type}: {str(e)}",
                exc_info=True,
            )
            raise