class ResumeService:
    @staticmethod
    def verify(data):
        return {
            "status":"success",
            "verification_status":"Verified",
            "module":"Resume",
            "data":data
        }
