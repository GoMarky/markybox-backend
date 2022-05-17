CREATE_SESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
        },
        "password": {
            "type": "string",
        }
    },
    "required": [
        "email",
        "password"
    ],
    "additionalProperties": False
}

REGISTER_USER_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
        },
        "password": {
            "type": "string",
        },
        "userName": {
            "type": "string",
        }
    },
    "required": [
        "email",
        "password",
        "userName"
    ],
    "additionalProperties": False
}

DELETE_SESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "sessionId": {
            "type": "number",
        },
    },
    "required": [
        "id",
    ],
    "additionalProperties": False
}
