from database_system.core import get_connection
from dummy_data_factory.dummy_property import DummyProperty
from dummy_data_factory.dummy_user import DummyUser


def main():
    number_of_users_to_create = 5
    number_of_properties_per_user = 3
    conn = get_connection()
    for _ in range(0, number_of_users_to_create + 1):
        current_user_id = create_dummy_user(conn)
        create_dummy_properties(conn, current_user_id, number_of_properties_per_user)
    conn.close()


def create_dummy_user(conn):
    dummy_user = DummyUser()
    dummy_user.populate_dummy_user()
    dummy_user_id = dummy_user.write_dummy_user(conn)
    print(f"\nCreated:\n{dummy_user}")
    return dummy_user_id


def create_dummy_property(conn, dummy_user_id):
    dummy_property = DummyProperty()
    dummy_property.populate_dummy_property(dummy_user_id)
    _ = dummy_property.write_dummy_property(conn)
    print(f"\nCreated:\n{dummy_property}")


def create_dummy_properties(conn, dummy_user_id, number_of_properties_per_user):
    for _ in range(0, number_of_properties_per_user + 1):
        create_dummy_property(conn, dummy_user_id)


if __name__ == '__main__':
    main()
