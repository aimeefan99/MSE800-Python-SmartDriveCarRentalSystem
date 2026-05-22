"""Bootstrap helpers for schema creation and seed data."""
# The bootstrap.py file contains helper functions for initializing the database schema and seeding starter data for the car rental system. It defines the SQL schema for the users, cars, and bookings tables, and includes a function to create these tables and insert default data such as an admin user and a set of cars into the database. This setup ensures that the application has the necessary structure and initial data to function correctly when first launched.
import hashlib
from typing import List, Set, Tuple
from database import DatabaseManager
from models import Car, User
from repositories import CarRepository, UserRepository

# The SCHEMA variable contains the SQL commands to create the necessary tables for the car rental system, including users, cars, and bookings. 
# Each table is defined with appropriate columns, data types, constraints, and relationships to ensure data integrity and support the application's functionality.
SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL DEFAULT '',
    phone TEXT NOT NULL DEFAULT '',
    role TEXT NOT NULL CHECK(role IN ('admin', 'customer'))
);


CREATE TABLE IF NOT EXISTS cars (
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    mileage INTEGER NOT NULL,
    available_now INTEGER NOT NULL CHECK(available_now IN (0, 1)),
    minimum_rent_period INTEGER NOT NULL,
    maximum_rent_period INTEGER NOT NULL,
    daily_rate REAL NOT NULL,
    category TEXT NOT NULL,
    eco_rating INTEGER NOT NULL CHECK(eco_rating BETWEEN 1 AND 5)
);

CREATE TABLE IF NOT EXISTS bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    car_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    pickup_location TEXT NOT NULL,
    extras TEXT NOT NULL,
    total_fee REAL NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('pending', 'approved', 'paid', 'rejected')),
    trip_type TEXT NOT NULL,
    insurance_selected INTEGER NOT NULL CHECK(insurance_selected IN (0, 1)),
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (car_id) REFERENCES cars (car_id)
);
"""

# The DEFAULT_ADMIN_HASH variable stores the SHA-256 hash of the default admin password ("admin123"), which is used to create a default admin user in the database if one does not already exist.
DEFAULT_ADMIN_HASH = hashlib.sha256("admin123".encode()).hexdigest()
DEFAULT_ADMIN_EMAIL = "admin@gmail.com"
DEFAULT_ADMIN_PHONE = "0211234567"

# The _default_seed_cars function returns a list of Car objects representing a diverse starter fleet for the car rental system. 
# This function is used to seed the database with a predefined set of cars that cover various categories and features, providing a good starting point for testing and using the application without needing to manually add cars after initialization.
def _default_seed_cars() -> List[Car]:
    """Return a diverse starter fleet for standard and smart booking flows."""

    return [
        Car(None, "Suzuki", "Swift", 2021, 36000, True, 1, 5, 58.0, "Compact", 4),
        Car(None, "Toyota", "Corolla Hybrid", 2023, 18000, True, 1, 12, 76.0, "Hybrid", 5),
        Car(None, "Mazda", "3", 2024, 12000, True, 1, 10, 88.0, "Sedan", 4),
        Car(None, "Mitsubishi", "Outlander", 2022, 27000, True, 2, 18, 102.0, "SUV", 4),
        Car(None, "Hyundai", "Tucson", 2024, 11000, True, 2, 21, 112.0, "SUV", 4),
        Car(None, "Tesla", "Model 3", 2024, 9000, True, 1, 7, 124.0, "Sedan", 5),
        Car(None, "Skoda", "Superb", 2025, 6000, True, 1, 14, 128.0, "Sedan", 4),
        Car(None, "Kia", "Carnival", 2023, 15000, True, 2, 14, 138.0, "Van", 3),
        Car(None, "Toyota", "RAV4 Hybrid", 2025, 7000, True, 3, 28, 145.0, "SUV", 5),
        Car(None, "Mercedes-Benz", "C200", 2025, 5000, True, 1, 14, 165.0, "Sedan", 4),
    ]

# The _car_signature function generates a unique signature for a car based on its make, model, and year. This is used to identify cars in the database and ensure that the default seed cars are added without creating duplicates.
def _car_signature(car: Car) -> Tuple[str, str, int]:
    """Use make/model/year as a stable identity for starter cars."""

    return (car.make, car.model, car.year)

# The _ensure_user_contact_columns function checks if the email and phone columns exist in the users table of the database. If they are missing (which can happen with older databases created before these fields were added), it alters the table to add these columns with default values. This ensures that the application can work with older databases without requiring a reset.
def _ensure_user_contact_columns(database: DatabaseManager) -> None:
    """Add email and phone columns when opening an older database."""

    # Older databases were created before contact fields were added,
    # so we patch the schema in place instead of forcing a reset.
    rows = database.execute("PRAGMA table_info(users)").fetchall()
    existing_columns = {row["name"] for row in rows}

    if "email" not in existing_columns:
        database.execute(
            "ALTER TABLE users ADD COLUMN email TEXT NOT NULL DEFAULT ''"
        )
    if "phone" not in existing_columns:
        database.execute(
            "ALTER TABLE users ADD COLUMN phone TEXT NOT NULL DEFAULT ''"
        )


def _ensure_booking_status_support(database: DatabaseManager) -> None:
    """Allow the booking table to store the newer paid status."""

    row = database.execute(
        "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'bookings'"
    ).fetchone()
    if row is None:
        return

    create_sql = row["sql"] or ""
    if "'paid'" in create_sql:
        return

    database.executescript(
        """
        ALTER TABLE bookings RENAME TO bookings_old;

        CREATE TABLE bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            car_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            pickup_location TEXT NOT NULL,
            extras TEXT NOT NULL,
            total_fee REAL NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('pending', 'approved', 'paid', 'rejected')),
            trip_type TEXT NOT NULL,
            insurance_selected INTEGER NOT NULL CHECK(insurance_selected IN (0, 1)),
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (car_id) REFERENCES cars (car_id)
        );

        INSERT INTO bookings (
            booking_id, user_id, car_id, start_date, end_date, pickup_location,
            extras, total_fee, status, trip_type, insurance_selected
        )
        SELECT
            booking_id, user_id, car_id, start_date, end_date, pickup_location,
            extras, total_fee, status, trip_type, insurance_selected
        FROM bookings_old;

        DROP TABLE bookings_old;
        """
    )

# The initialize_database function takes a DatabaseManager instance as an argument and executes the SQL schema to create the necessary tables. 
def initialize_database(database: DatabaseManager) -> None:
    """Create tables and seed starter data once."""
    # The function first executes the SCHEMA SQL script to create the necessary tables in the database.
    database.executescript(SCHEMA)
    _ensure_user_contact_columns(database)
    _ensure_booking_status_support(database)

    # The function first executes the SCHEMA SQL script to create the necessary tables in the database.
    users = UserRepository(database)
    cars = CarRepository(database)
    admin_user = users.find_by_username("admin")

    # The function checks if an admin user already exists in the database; 
    # if not, it creates a default admin user with a predefined username and password hash. 
    # If the admin user exists but has a different password hash, it updates the password hash to ensure that the default credentials are in place.
    if admin_user is None:
        users.create(
            User(
                user_id=None,
                username="admin",
                password_hash=DEFAULT_ADMIN_HASH,
                email=DEFAULT_ADMIN_EMAIL,
                phone=DEFAULT_ADMIN_PHONE,
                role="admin",
            )
        )
    elif admin_user.password_hash != DEFAULT_ADMIN_HASH:
        database.execute(
            "UPDATE users SET password_hash = ? WHERE username = ?",
            (DEFAULT_ADMIN_HASH, "admin"),
        )

    # Keep the default admin account usable even when the database
    # was created before contact details were introduced.
    database.execute(
        """
        UPDATE users
        SET email = ?, phone = ?
        WHERE username = ? AND (email = '' OR phone = '')
        """,
        (DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PHONE, "admin"),
    )

    # The function then ensures that the starter fleet exists. It adds any missing
    # default cars without clearing user data or existing bookings.
    existing_signatures: Set[Tuple[str, str, int]] = {
        _car_signature(car) for car in cars.list_all()
    }
    for car in _default_seed_cars():
        if _car_signature(car) not in existing_signatures:
            cars.create(car)
