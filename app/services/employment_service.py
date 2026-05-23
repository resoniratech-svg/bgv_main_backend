class EmploymentService:
    @staticmethod
    def verify(data):
        return {
            "status":"success",
            "verification_status":"Verified",
            "module":"Employment",
            "data":data
        }
