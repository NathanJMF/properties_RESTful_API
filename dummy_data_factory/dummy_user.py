import hashlib
import random
import database_system.structure
import database_system.core
from faker import Faker
from datetime import datetime, timezone


class DummyUser:
    def __init__(self, locale="en_US"):
        self.fake = Faker(locale)
        self.user_id = None
        self.username = None
        self.password_hash = None
        self.email = None
        self.is_admin = False
        self.created_at = None

    def populate_dummy_user(self):
        self.generate_dummy_username()
        self.generate_dummy_password()
        self.generate_dummy_email()
        self.generate_dummy_is_admin()
        self.created_at = datetime.now(timezone.utc)

    def generate_dummy_username(self):
        self.username = f"{self.fake.word().capitalize()} {self.fake.word().capitalize()}"

    def generate_dummy_password(self):
        self.password_hash = hashlib.sha256(f"{self.fake.password(length=10, 
                                                                  special_chars=True, 
                                                                  digits=True, 
                                                                  upper_case=True, 
                                                                  lower_case=True)}".encode()).hexdigest()

    def generate_dummy_email(self):
        self.email = f"{self.fake.word().lower()}@{self.fake.word().lower()}.com"

    def generate_dummy_is_admin(self):
        self.is_admin = random.choice([True, False])

    def get_user_id(self):
        return self.user_id

    def __str__(self):
        admin_status = "Admin" if self.is_admin else "User"
        created_at_str = self.created_at.strftime("%Y-%m-%d %H:%M:%S %Z") if self.created_at else "Not set"
        return (f"DUMMY USER\n"
                f"User ID: {self.user_id}\n"
                f"Username: {self.username}\n"
                f"Email: {self.email}\n"
                f"Password Hash: {self.password_hash}\n"
                f"Status: {admin_status}\n"
                f"Created At: {created_at_str}")

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "is_admin": self.is_admin,
            "created_at": self.created_at
        }

    def write_dummy_user(self, conn):
        try:
            current_dummy_user_dict = self.to_dict()
            user_table_structure = database_system.structure.get_table_users()
            primary_key_column = user_table_structure["primary_key"]
            schema_name = user_table_structure["schema_name"]
            table_name = user_table_structure["table_name"]
            self.user_id = database_system.core.basic_write_dict(conn, schema_name, table_name, current_dummy_user_dict,
                                                                 primary_key_column=primary_key_column, return_id=True)
            return self.user_id
        except Exception as e:
            print(f"An error occurred while writing to the database: {e}")
            return None
