class EducationService:
    @staticmethod
    def verify(data):
        return {
            "status":"success",
            "verification_status":"Verified",
            "module":"Education",
            "data":data
        }
