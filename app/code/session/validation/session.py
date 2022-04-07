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
