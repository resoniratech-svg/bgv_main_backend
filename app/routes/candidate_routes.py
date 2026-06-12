from flask import Blueprint, request, jsonify
from flask import send_file
from app.services.candidate_service import CandidateService
import os
from werkzeug.utils import secure_filename
from config import Config

candidate_bp = Blueprint(
    "candidate_bp",
    __name__
)


@candidate_bp.route(
    "/candidates/create",
    methods=["POST"]
)

def create_candidate():

    try:

        data = request.get_json()

        result = CandidateService.create_candidate(data)

        if result["status"] == "error":

            return jsonify(result), 400

        return jsonify(result), 201

    except Exception as e:
        error_message = str(e)
        if "Duplicate entry" in error_message:
            return jsonify({
                "status": "error",
                "message": "Candidate email already exists"
            }), 400
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500


# @candidate_bp.route("/candidates", methods=["GET"])
# def get_candidates():

#     candidates = CandidateService.get_all_candidates()

#     return jsonify(candidates), 200

@candidate_bp.route("/candidates", methods=["GET"])
def get_candidates():

    try:

        candidates = CandidateService.get_all_candidates()

        #print(candidates)

        return jsonify(candidates), 200

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    

@candidate_bp.route(
    "/candidates/<int:candidate_id>",
    methods=["GET"]
)
def get_candidate(candidate_id):

    try:

        candidate = (
            CandidateService.get_candidate_by_id(
                candidate_id
            )
        )

        return jsonify(candidate), 200

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
@candidate_bp.route(
    "/candidates/<int:candidate_id>/documents",
    methods=["GET"]
)
def get_candidate_documents(candidate_id):

    try:

        from app.services.document_service import (
            DocumentService
        )

        result = (
            DocumentService.get_candidate_documents(
                candidate_id
            )
        )

        return jsonify(result), 200

    except Exception as e:

        import traceback

        traceback.print_exc()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@candidate_bp.route(
    "/candidates/<int:candidate_id>/status",
    methods=["PUT"]
)
def update_candidate_status(candidate_id):

    try:

        data = request.get_json()

        result = CandidateService.update_candidate_status(
            candidate_id,
            data
        )

        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
@candidate_bp.route(
    "/candidates/<int:candidate_id>",
    methods=["PUT"]
)
def update_candidate(candidate_id):

    try:

        data = request.get_json()

        result = CandidateService.update_candidate(
            candidate_id,
            data
        )

        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@candidate_bp.route(
    "/candidates/<int:candidate_id>",
    methods=["DELETE"]
)
def delete_candidate(candidate_id):

    try:

        result = CandidateService.delete_candidate(
            candidate_id
        )

        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@candidate_bp.route(
    "/candidate/submit-documents",
    methods=["POST"]
)
def submit_documents():

    try:

        data = request.get_json()

        candidate_id = data.get(
            "candidate_id"
        )

        CandidateService.update_candidate_status(
            candidate_id,
            {
                "status": "DOCUMENTS_SUBMITTED"
            }
        )

        return jsonify({
            "status": "success",
            "message": "Documents submitted successfully"
        }), 200

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

