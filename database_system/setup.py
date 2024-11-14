from database_system import structure, core


def setup_api_database(conn):
    setup_required_schemas(conn)
    setup_required_tables(conn)


def setup_required_schemas(conn):
    required_schema_names = structure.get_required_schema_names()
    for current_schema_name in required_schema_names:
        core.create_schema(conn, current_schema_name)


def setup_required_tables(conn):
    required_tables = structure.get_required_tables()
    for current_table in required_tables:
        setup_new_table(conn, current_table)


def setup_new_table(conn, current_table):
    # Create minimal table with the primary key
    print(f"Creating table {current_table['table_name']} in schema {current_table['schema_name']} with primary key "
          f"{current_table['primary_key']}.")
    core.create_minimal_table(conn, current_table["schema_name"], current_table["table_name"],
                         current_table["primary_key"])

    # Add additional columns
    if current_table["columns"]:
        print(f"Adding columns to table {current_table['table_name']} in schema {current_table['schema_name']}.")
        core.add_columns_to_table(conn, current_table["schema_name"], current_table["table_name"],
                             current_table["columns"])

    # Add foreign key constraints if any
    if current_table.get("foreign_keys"):
        print(f"Adding foreign keys to table {current_table['table_name']} in schema {current_table['schema_name']}.")
        core.add_foreign_keys_to_table(conn, current_table["schema_name"], current_table["table_name"],
                                  current_table["foreign_keys"])
