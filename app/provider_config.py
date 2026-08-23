import os


SUREPASS = {

    "base_url": os.getenv(
        "SUREPASS_BASE_URL"
    ),

    "api_key": os.getenv(
        "SUREPASS_API_KEY"
    )
}


DIDIT = {

    "base_url": os.getenv(
        "DIDIT_BASE_URL"
    ),

    "api_key": os.getenv(
        "DIDIT_API_KEY"
    )
}