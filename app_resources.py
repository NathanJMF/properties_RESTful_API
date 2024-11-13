import database_system.core
from helpers import query_helpers
from flask_restful import Resource, abort
from app_request_parsers import get_property_request_parser


class Property(Resource):
    def get(self, property_id=None):
        conn = database_system.core.get_connection()
        if property_id is None:
            all_properties = query_helpers.get_all_properties(conn)
            conn.close()
            return all_properties
        current_property = query_helpers.get_property_by_id(conn, property_id)
        conn.close()
        if not current_property:
            abort(404, description="Property could not be found!")
        return current_property[0]

    def post(self):
        property_argument_parser = get_property_request_parser()
        request_data = property_argument_parser.parse_args()

        conn = database_system.core.get_connection()
        new_property_id = query_helpers.write_new_property(conn, request_data)
        conn.close()

        if new_property_id is None:
            abort(500, description="Error creating property!")

        return {"message": "Property created", "property_id": new_property_id}, 201
