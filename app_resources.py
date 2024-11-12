from pydoc import describe

import database_system.core
from helpers import query_helpers
from flask_restful import Resource, abort


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