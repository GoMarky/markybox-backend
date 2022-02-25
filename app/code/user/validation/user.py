CREATE_USER_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 2
        },
        "email": {
            "type": "string",
            "minLength": 7
        },
        "password": {
            "type": "string"
        }
    },
    "required": [
        "name",
        "email",
        "password"
    ],
    "additionalProperties": False
}


DELETE_USER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "number",
        },
    },
    "required": [
        "id",
    ],
    "additionalProperties": False
}
