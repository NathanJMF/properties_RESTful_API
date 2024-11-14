import config_loader
import psycopg2
from psycopg2 import sql, extras


def get_connection():
    app_config = config_loader.Config()
    new_connection = psycopg2.connect(
        database=app_config.db_name,
        user=app_config.db_user,
        password=app_config.db_password,
        host=app_config.db_host,
        port=app_config.db_port
    )
    return new_connection


def basic_lookup(conn, query, values=None, show_query=False):
    try:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            # Execute the query, passing values if provided
            cursor.execute(query, values or ())
            if show_query:
                print(cursor.query)
            result = cursor.fetchall()
        # Return an empty list if no results are found for consistency
        return result if result else []
    except psycopg2.Error as e:
        print("Error executing lookup:", e)
        # Rollback any transaction if an error occurs
        conn.rollback()
        return None


def basic_write_dict(conn, schema_name, table_name, data_dict, primary_key_column=None, return_id=False):
    # Prepare the columns and placeholders for the SQL statement
    columns = sql.SQL(', ').join(map(sql.Identifier, data_dict.keys()))
    values = sql.SQL(', ').join(sql.Placeholder() * len(data_dict))

    # Prepare the INSERT statement
    query = sql.SQL("INSERT INTO {}.{} ({}) VALUES ({})").format(
        sql.Identifier(schema_name),
        sql.Identifier(table_name),
        columns,
        values
    )
    # If return_id is requested, add RETURNING clause for primary key
    if return_id and primary_key_column:
        query += sql.SQL(" RETURNING {}").format(sql.Identifier(primary_key_column))
    try:
        with conn.cursor() as cursor:
            # Execute the query with data values
            cursor.execute(query, list(data_dict.values()))
            if return_id and primary_key_column:
                # Fetch and return the ID of the inserted row if requested
                inserted_id = cursor.fetchone()[0]
                conn.commit()  # Commit the transaction
                print("Data inserted successfully, ID:", inserted_id)
                return inserted_id
            else:
                # Commit the transaction for a simple insert
                conn.commit()
                print("Data inserted successfully.")
    except psycopg2.Error as e:
        print("Error executing write:", e)
        conn.rollback()
        return None


def basic_delete_entry(conn, schema_name, table_name, primary_key_column, entry_id):
    # Prepare the DELETE statement
    delete_query = sql.SQL("DELETE FROM {}.{} WHERE {} = %s;").format(
        sql.Identifier(schema_name),
        sql.Identifier(table_name),
        sql.Identifier(primary_key_column)
    )
    try:
        with conn.cursor() as cursor:
            # Execute the delete query
            cursor.execute(delete_query, (entry_id,))
            # Check if any row was deleted
            if cursor.rowcount == 0:
                # No record was deleted, likely because it didn't exist
                return False
            conn.commit()
            return True
    except psycopg2.Error as e:
        # Rollback the transaction if there's an error
        print("Error executing delete:", e)
        conn.rollback()
        return False


def create_schema(conn, schema_name):
    create_schema_query = sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema_name))
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_schema_query)
            conn.commit()
            print(f"Schema '{schema_name}' has been created or already exists.")
    except psycopg2.Error as e:
        print("Error creating schema:", e)
        conn.rollback()


def create_minimal_table(conn, schema_name, table_name, primary_key_column_name):
    create_table_query = sql.SQL(
        "CREATE TABLE IF NOT EXISTS {}.{} ({} SERIAL PRIMARY KEY);"
    ).format(
        sql.Identifier(schema_name),
        sql.Identifier(table_name),
        sql.Identifier(primary_key_column_name)
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_query)
            print(
                f"Table '{table_name}' created in schema '{schema_name}' with primary key '{primary_key_column_name}'.")
            conn.commit()
    except psycopg2.Error as e:
        print("Error creating table:", e)
        conn.rollback()


def add_columns_to_table(conn, schema_name, table_name, columns):
    check_column_exists_query = sql.SQL(
        "SELECT EXISTS ("
        "SELECT 1 "
        "FROM information_schema.columns "
        "WHERE table_schema = %s AND table_name = %s AND column_name = %s);"
    )
    add_column_query = sql.SQL("ALTER TABLE {}.{} ADD COLUMN {} {};")

    try:
        with conn.cursor() as cursor:
            for column, data_type in columns.items():
                cursor.execute(check_column_exists_query, (schema_name, table_name, column))
                column_exists = cursor.fetchone()[0]

                if not column_exists:
                    cursor.execute(
                        add_column_query.format(
                            sql.Identifier(schema_name),
                            sql.Identifier(table_name),
                            sql.Identifier(column),
                            sql.SQL(data_type)
                        )
                    )
                    print(f"Added column '{column}' of type '{data_type}' to '{table_name}' in schema '{schema_name}'.")
            conn.commit()
    except psycopg2.Error as e:
        print("Error adding columns:", e)
        conn.rollback()


def add_foreign_keys_to_table(conn, schema_name, table_name, foreign_keys):
    if not foreign_keys:
        return

    alter_column_null_status_query = sql.SQL("ALTER TABLE {}.{} ALTER COLUMN {} DROP NOT NULL;")
    check_foreign_key_exists_query = "SELECT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = %s);"
    add_foreign_key_base_query = sql.SQL("ALTER TABLE {}.{} ADD CONSTRAINT {} FOREIGN KEY ({}) REFERENCES {}({});")

    try:
        with conn.cursor() as cursor:
            for fk in foreign_keys:
                fk_column = fk['foreign_key_column']
                ref_schema = fk['reference_schema']
                ref_table = fk['reference_table']
                ref_column = fk['reference_column']
                is_nullable = fk['is_nullable']

                # Adjust column nullability if specified
                if is_nullable:
                    cursor.execute(
                        alter_column_null_status_query.format(
                            sql.Identifier(schema_name),
                            sql.Identifier(table_name),
                            sql.Identifier(fk_column)
                        )
                    )
                    print(f"Column '{fk_column}' in '{table_name}' set to nullable as specified for foreign key.")

                # Foreign key name
                fk_name = f"fk_{schema_name}_{table_name}_{fk_column}_{ref_table}"

                # Check if the foreign key constraint already exists
                cursor.execute(check_foreign_key_exists_query, (fk_name,))
                fk_exists = cursor.fetchone()[0]

                if not fk_exists:
                    # Add foreign key if it doesn't exist
                    add_fk_query = add_foreign_key_base_query.format(
                        sql.Identifier(schema_name),
                        sql.Identifier(table_name),
                        sql.Identifier(fk_name),
                        sql.Identifier(fk_column),
                        sql.SQL("{}.{}").format(sql.Identifier(ref_schema), sql.Identifier(ref_table)),
                        sql.Identifier(ref_column)
                    )
                    cursor.execute(add_fk_query)
                    print(
                        f"Foreign key '{fk_name}' added to '{table_name}' referencing '{ref_table}({ref_column})'. Nullable: {is_nullable}")
            conn.commit()
    except psycopg2.Error as e:
        print("Error adding foreign keys:", e)
        conn.rollback()
