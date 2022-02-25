CREATE_SESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "removeable": {
            "type": "boolean",
        },
        "author": {
            "type": "string",
        }
    },
    "required": [
        "author",
        "removeable"
    ],
    "additionalProperties": False
}

DELETE_SESSION_SCHEMA = {
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
