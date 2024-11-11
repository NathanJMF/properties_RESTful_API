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
