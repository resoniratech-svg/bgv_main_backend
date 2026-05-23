class PanService:
    @staticmethod
    def verify(data):
        return {
            "status":"success",
            "verification_status":"Verified",
            "module":"Pan",
            "data":data
        }
