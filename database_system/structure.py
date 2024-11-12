def get_required_schema_names():
    required_schema_names = [
        get_schema_name_public()
    ]
    return required_schema_names


def get_required_tables():
    required_tables = [
        get_table_users(),
        get_table_properties()
    ]
    return required_tables


def get_schema_name_public():
    return "public"


def get_table_users():
    users_table = {
        "schema_name": get_schema_name_public(),
        "table_name": "users",
        "primary_key": "user_id",
        "columns": {
            "user_id": "SERIAL PRIMARY KEY",
            "username": "VARCHAR(50) NOT NULL UNIQUE",
            "password_hash": "TEXT NOT NULL",
            "email": "VARCHAR(100) NOT NULL UNIQUE",
            "is_admin": "BOOLEAN DEFAULT FALSE",
            "created_at": "TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
        },
        "foreign_keys": None
    }
    return users_table


def get_table_properties():
    properties_table = {
        "schema_name": get_schema_name_public(),
        "table_name": "properties",
        "primary_key": "property_id",
        "columns": {
            "property_id": "SERIAL PRIMARY KEY",
            "address": "TEXT NOT NULL",
            "postcode": "VARCHAR(20) NOT NULL",
            "city": "VARCHAR(50) NOT NULL",
            "num_rooms": "INTEGER NOT NULL CHECK (num_rooms > 0)",
            "created_by": "INTEGER NOT NULL",
            "created_at": "TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
        },
        "foreign_keys": [
            {
                "foreign_key_column": "created_by",
                "reference_schema": get_schema_name_public(),
                "reference_table": "users",
                "reference_column": "user_id",
                "is_nullable": False
            }
        ]
    }
    return properties_table
