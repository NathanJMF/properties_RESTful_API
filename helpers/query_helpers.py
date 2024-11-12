import database_system.structure
import database_system.core


def get_all_properties(conn):
    property_table_structure = database_system.structure.get_table_properties()
    schema_name = property_table_structure["schema_name"]
    table_name = property_table_structure["table_name"]
    # Cast the column 'created_at' to a string as datetime objects can't be automatically JSON serialized by Flask
    query = (f"SELECT *,"
             f"TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS') AS created_at "
             f"FROM "
             f"{schema_name}.{table_name};")
    all_properties = database_system.core.basic_lookup(conn, query)
    return all_properties


def get_property_by_id(conn, property_id):
    property_table_structure = database_system.structure.get_table_properties()
    schema_name = property_table_structure["schema_name"]
    table_name = property_table_structure["table_name"]
    # Cast the column 'created_at' to a string as datetime objects can't be automatically JSON serialized by Flask
    query = (f"SELECT *,"
             f"TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS') AS created_at "
             f"FROM "
             f"{schema_name}.{table_name} "
             f"WHERE "
             f"property_id = %s;")
    values = [property_id,]
    current_property = database_system.core.basic_lookup(conn, query, values)
    return current_property