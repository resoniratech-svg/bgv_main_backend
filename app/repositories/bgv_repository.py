from app.models.bgv_request import BGVRequest
from app.extensions import db


class BGVRepository:

    @staticmethod
    def create(data):
        bgv = BGVRequest(
            candidate_name=data["candidate_name"],
            email=data["email"],
            phone=data["phone"],
            verification_type=data["verification_type"],
        )

        db.session.add(bgv)
        db.session.flush()
        return bgv

    @staticmethod
    def get_active_by_id(bgv_id):
        return BGVRequest.query.filter_by(id=bgv_id, is_deleted=False).first()

    @staticmethod
    def get_all_active():
        return BGVRequest.query.filter_by(is_deleted=False).all()

    @staticmethod
    def update(bgv, data):
        for key, value in data.items():
            setattr(bgv, key, value)
        return bgv

    @staticmethod
    def soft_delete(bgv):
        bgv.is_deleted = True