import database_system.core
from helpers import query_helpers
from flask_restful import Resource


class Property(Resource):
    def get(self):
        conn = database_system.core.get_connection()
        all_properties = query_helpers.get_all_properties(conn)
        conn.close()
        return all_properties