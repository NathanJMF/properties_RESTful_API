from database_system.core import get_connection
from database_system.setup import setup_api_database


def main():
    conn = get_connection()
    setup_api_database(conn)
    conn.close()


if __name__ == '__main__':
    main()
