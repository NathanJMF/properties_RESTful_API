import database_system.core
from helpers import query_helpers
from flask import request
from flask_restful import Resource, abort
from app_request_parsers import get_property_request_parser


class Property(Resource):
    def get(self, property_id=None):
        conn = database_system.core.get_connection()
        if property_id is None:
            all_properties = query_helpers.get_all_properties(conn)
            conn.close()
            return all_properties, 200
        try:
            property_id = int(property_id)
        except ValueError:
            abort(400, description="Property ID must be an integer!")
        current_property = query_helpers.get_property_by_id(conn, property_id)
        conn.close()
        if not current_property:
            abort(404, description="Property could not be found!")
        return current_property[0], 200

    def post(self):
        property_argument_parser = get_property_request_parser()
        request_data = property_argument_parser.parse_args()

        conn = database_system.core.get_connection()
        new_property_id = query_helpers.write_new_property(conn, request_data)
        conn.close()

        if new_property_id is None:
            abort(500, description="Error creating property!")

        return {"description": "Property created", "property_id": new_property_id}, 201

    def delete(self, property_id=None):
        # Leave if there is no property to delete
        if property_id is None:
            abort(400, description="No property ID provided!")

        # Pull user_id out of request headers ensuring it is present and an integer
        user_id = request.headers.get("user_id")
        if user_id is None:
            abort(400, description="No user ID provided!")
        try:
            user_id = int(user_id)
        except ValueError:
            abort(400, description="Invalid user ID provided! User ID must be an integer.")

        conn = database_system.core.get_connection()

        # Query DB for property, handle property not found
        current_property = query_helpers.get_property_by_id(conn, property_id)
        if not current_property:
            conn.close()
            abort(404, description="Property could not be found!")
        current_property = current_property[0]

        # Check property created_by matches user_id
        if current_property["created_by"] != user_id:
            conn.close()
            abort(403, description="You do not have the rights to delete this property!")

        # Attempt to delete the property and close database connection
        property_deleted_flag = query_helpers.delete_property_by_id(conn, property_id)
        conn.close()
        if not property_deleted_flag:
            abort(500, description="Failed to delete the property!")

        return {"description": "Property deleted successfully"}, 200
