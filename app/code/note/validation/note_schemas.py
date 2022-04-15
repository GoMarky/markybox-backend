CREATE_NOTE_SCHEMA = {
    "type": "object",
    "properties": {
        "sessionId": {
            "type": "string"
        },
        "data": {
            "type": "string"
        },
        "title": {
            "type": "string"
        }
    },
    "required": [
        "sessionId"
    ],
    "additionalProperties": False
}

UPDATE_NOTE_SCHEMA = {
    "type": "object",
    "properties": {
        "sessionId": {
            "type": "string"
        },
        "noteId": {
            "type": "string"
        },
        "data": {
            "type": "string"
        }
    },
    "required": [
        "sessionId",
        "noteId",
        "data"
    ],
    "additionalProperties": False
}

DELETE_NOTE_SCHEMA = {
    "type": "object",
    "properties": {
        "sessionId": {
            "type": "string"
        },
        "noteId": {
            "type": "string"
        }
    },
    "required": [
        "sessionId",
        "noteId",
    ],
    "additionalProperties": False
}
