from flask import Blueprint

from flask import jsonify

from flask import request



from app.services.verifications.face_match_verification_service import (

    FaceMatchVerificationService

)



face_match_bp=Blueprint(

    "face_match",

    __name__

)



# ====================================

# VERIFY

# ====================================


@face_match_bp.route(

    "/face-match/verify",

    methods=["POST"]

)

def verify():


    token=request.headers.get(

        "Authorization"

    )



    data=request.json



    result=(


        FaceMatchVerificationService


        .verify(


            candidate_id=


            data["candidate_id"],


            bgv_id=


            data["bgv_id"],


            document_id=


            data["document_id"],


            token=


            token

        )

    )



    return jsonify(result)





# ====================================

# GET RESULT

# ====================================


@face_match_bp.route(

    "/face-match/result/<int:candidate_id>",

    methods=["GET"]

)

def get_result(

        candidate_id

):



    token=request.headers.get(

        "Authorization"

    )



    result=(


        FaceMatchVerificationService


        .get_result(


            candidate_id,


            token

        )

    )



    return jsonify(


        result

    )
