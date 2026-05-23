class FaceMatchService:
    @staticmethod
    def verify(data):
        return {
            "status":"success",
            "verification_status":"Verified",
            "module":"FaceMatch",
            "data":data
        }
