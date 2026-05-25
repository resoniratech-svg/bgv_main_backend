def success_response(
    message,
    data=None,
    status_code=200
):

    response = {
        "status": "success",
        "message": message,
        "data": data
    }

    return response, status_code


def error_response(
    message,
    status_code=400
):

    response = {
        "status": "error",
        "message": message
    }

    return response, status_code