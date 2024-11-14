import random
import database_system.structure
import database_system.core
from faker import Faker
from datetime import datetime, timezone


class DummyProperty:
    def __init__(self, locale="en_US"):
        self.fake = Faker(locale)
        self.property_id = None
        self.user_id = None
        self.address = None
        self.postcode = None
        self.city = None
        self.num_rooms = None
        self.created_at = None

    def populate_dummy_property(self, user_id):
        self.user_id = user_id
        self.address = self.fake.address()
        self.postcode = self.fake.postcode()
        self.city = self.fake.city()
        self.num_rooms = random.randint(1, 10)
        self.created_at = datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "created_by": self.user_id,
            "address": self.address,
            "postcode": self.postcode,
            "city": self.city,
            "num_rooms": self.num_rooms,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def write_dummy_property(self, conn):
        try:
            current_dummy_property_dict = self.to_dict()
            property_table_structure = database_system.structure.get_table_properties()
            schema_name = property_table_structure["schema_name"]
            table_name = property_table_structure["table_name"]
            self.property_id = database_system.core.basic_write_dict(
                conn, schema_name, table_name, current_dummy_property_dict
            )
            return self.property_id
        except Exception as e:
            print(f"An error occurred while writing the property to the database: {e}")
            return None

    def __str__(self):
        created_at_str = self.created_at.strftime("%Y-%m-%d %H:%M:%S %Z") if self.created_at else "Not set"
        return (f"DUMMY PROPERTY\n"
                f"Property ID: {self.property_id}\n"
                f"User ID: {self.user_id}\n"
                f"Address: {self.address}\n"
                f"Postcode: {self.postcode}\n"
                f"City: {self.city}\n"
                f"Number of Rooms: {self.num_rooms}\n"
                f"Created At: {created_at_str}")
