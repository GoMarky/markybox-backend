CREATE_NOTE_SCHEMA = {
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

UPDATE_NOTE_SCHEMA = {
    "type": "object",
    "properties": {

    },
    "required": [

    ],
    "additionalProperties": False
}

DELETE_NOTE_SCHEMA = {
    "type": "object",
    "properties": {
    },
    "required": [
    ],
    "additionalProperties": False
}
