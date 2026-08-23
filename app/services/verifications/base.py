class BaseVerificationService:
    def execute(self, data):
        raise NotImplementedError("Subclasses must implement execute()")