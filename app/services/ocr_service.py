class OCRService:
    @staticmethod
    def verify(data):
        return {
            "status":"success",
            "verification_status":"Verified",
            "module":"OCR",
            "data":data
        }
