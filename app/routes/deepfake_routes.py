from flask import (

    Blueprint,

    request,

    jsonify

)


from flask_jwt_extended import (

    jwt_required,

    get_jwt_identity

)


from app.services.deepfake_service import (

    DeepfakeService

)



deepfake_bp = Blueprint(


    "deepfake",


    __name__

)



#######################################
# VERIFY
#######################################


@deepfake_bp.route(

    "/verify",

    methods=["POST"]

)

@jwt_required()

def verify_deepfake():


    data=request.json


    response=(


        DeepfakeService

        .verify_deepfake(


            candidate_id=

            data["candidate_id"],


            bgv_id=

            data["bgv_id"],


            document_id=

            data["document_id"],


            token=

            request.headers.get(

                "Authorization"

            )

        )

    )



    return jsonify(response)






#######################################
# GET RESULT
#######################################



@deepfake_bp.route(

    "/result/<int:candidate_id>",

    methods=["GET"]

)

@jwt_required()

def get_result(

        candidate_id

):


    response=(


        DeepfakeService

        .get_result(


            candidate_id,


            request.headers.get(

                "Authorization"

            )

        )

    )


    return jsonify(response)
