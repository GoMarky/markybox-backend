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

SETTINGS_USER_APPLY_SCHEMA = {
    "type": "object",
    "properties": {
        "sessionId": {
            "type": "number"
        }
    }
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
        "sessionId",
    ],
    "additionalProperties": False
}
