"""Repository classes for persistence operations."""
# The repositories.py file contains the repository classes responsible for handling persistence operations related to users, cars, and bookings in the car rental system. 
from typing import Iterable, List, Optional
from database import DatabaseManager
from models import Booking, Car, User

# The UserRepository class provides methods for creating and retrieving user records from the database. It includes a create method to add new users and a find_by_username method to retrieve users based on their username. The CarRepository class offers methods for managing car inventory, including creating, updating, deleting, and retrieving car records. It also has methods to list all cars or only available cars. The BookingRepository class handles rental bookings, allowing for creating new bookings, updating booking status, and retrieving bookings by ID or status. Additionally, the format_car_rows function formats car data into a compact string representation for display in the CLI.
class UserRepository:
    """Persistence methods for users."""

    # The __init__ method initializes the UserRepository with a DatabaseManager instance, which is used for executing database operations.
    def __init__(self, database: DatabaseManager) -> None:
        self.database = database

    # The create method takes a User object as input, inserts it into the users table in the database, and returns the created User object with the assigned user_id.
    def create(self, user: User) -> User:
        cursor = self.database.execute(
            """
            INSERT INTO users (username, password_hash, full_name, email, phone, role)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user.username,
                user.password_hash,
                user.username,
                user.email,
                user.phone,
                user.role,
            ),
        )
        user.user_id = cursor.lastrowid
        return user

    # The find_by_username method retrieves a user record from the database based on the provided username. If a matching user is found, it returns a User object; otherwise, it returns None.
    def find_by_username(self, username: str) -> Optional[User]:
        row = self.database.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        return self._row_to_user(row) if row else None

    def list_all(self) -> List[User]:
        rows = self.database.execute(
            "SELECT * FROM users ORDER BY user_id"
        ).fetchall()
        return [self._row_to_user(row) for row in rows]

    def get_by_id(self, user_id: int) -> Optional[User]:
        row = self.database.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        return self._row_to_user(row) if row else None

    def update(self, user: User) -> None:
        self.database.execute(
            """
            UPDATE users
            SET username = ?, password_hash = ?, full_name = ?, email = ?, phone = ?, role = ?
            WHERE user_id = ?
            """,
            (
                user.username,
                user.password_hash,
                user.username,
                user.email,
                user.phone,
                user.role,
                user.user_id,
            ),
        )

    def delete(self, user_id: int) -> None:
        self.database.execute("DELETE FROM users WHERE user_id = ?", (user_id,))

    # The @staticmethod decorator indicates that the _row_to_user method is a static method that does not depend on the instance of the UserRepository class. 
    # It can be called without creating an instance of the class and is used to convert a database row into a User object.
    @staticmethod 
    #   The _row_to_user method is a helper function that converts a database row into a User object. 
    #   It takes a database row as input and returns a User object with the corresponding attributes populated from the row data.
    def _row_to_user(row) -> User:
        return User(
            user_id=row["user_id"],
            username=row["username"],
            password_hash=row["password_hash"],
            email=row["email"],
            phone=row["phone"],
            role=row["role"],
        )

#   The CarRepository class provides methods for managing car inventory, including creating, updating, deleting, and retrieving car records. 
#   It also has methods to list all cars or only available cars. The BookingRepository class handles rental bookings, allowing for creating new bookings, updating booking status, and retrieving bookings by ID or status. Additionally, the format_car_rows function formats car data into a compact string representation for display in the CLI.
class CarRepository:
    """Persistence methods for car inventory."""

    #   The __init__ method initializes the CarRepository with a DatabaseManager instance, which is used for executing database operations.
    def __init__(self, database: DatabaseManager) -> None:
        self.database = database

    # The create method takes a Car object as input, inserts it into the cars table in the database, and returns the created Car object with the assigned car_id.
    def create(self, car: Car) -> Car:
        cursor = self.database.execute(
            """
            INSERT INTO cars (
                make, model, year, mileage, available_now,
                minimum_rent_period, maximum_rent_period,
                daily_rate, category, eco_rating
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                car.make,
                car.model,
                car.year,
                car.mileage,
                int(car.available_now),
                car.minimum_rent_period,
                car.maximum_rent_period,
                car.daily_rate,
                car.category,
                car.eco_rating,
            ),
        )
        car.car_id = cursor.lastrowid
        return car

    #   The update method takes a Car object as input and updates the corresponding car record in the database based on the car_id. 
    #   It updates all attributes of the car in the database with the values from the provided Car object.
    def update(self, car: Car) -> None:
        self.database.execute(
            """
            UPDATE cars
            SET make = ?, model = ?, year = ?, mileage = ?, available_now = ?,
                minimum_rent_period = ?, maximum_rent_period = ?,
                daily_rate = ?, category = ?, eco_rating = ?
            WHERE car_id = ?
            """,
            (
                car.make,
                car.model,
                car.year,
                car.mileage,
                int(car.available_now),
                car.minimum_rent_period,
                car.maximum_rent_period,
                car.daily_rate,
                car.category,
                car.eco_rating,
                car.car_id,
            ),
        )

    # The delete method takes a car_id as input and deletes the corresponding car record from the database.
    def delete(self, car_id: int) -> None:
        self.database.execute("DELETE FROM cars WHERE car_id = ?", (car_id,))

    # The get_by_id method retrieves a car record from the database based on the provided car_id. If a matching car is found, it returns a Car object; otherwise, it returns None.
    def get_by_id(self, car_id: int) -> Optional[Car]:
        row = self.database.execute(
            "SELECT * FROM cars WHERE car_id = ?",
            (car_id,),
        ).fetchone()
        return self._row_to_car(row) if row else None

    # The list_all method retrieves all car records from the database, orders them by car_id, and returns a list of Car objects representing the entire car inventory.
    def list_all(self) -> List[Car]:
        rows = self.database.execute("SELECT * FROM cars ORDER BY car_id").fetchall()
        return [self._row_to_car(row) for row in rows]

    # The list_available method retrieves all car records from the database where the available_now attribute is set to 1 (indicating that the car is currently available for rent), orders them by car_id, and returns a list of Car objects representing the available cars in the inventory.
    def list_available(self) -> List[Car]:
        rows = self.database.execute(
            "SELECT * FROM cars WHERE available_now = 1 ORDER BY car_id"
        ).fetchall()
        return [self._row_to_car(row) for row in rows]

    # The @staticmethod decorator indicates that the _row_to_car method is a static method that does not depend on the instance of the CarRepository class. 
    # It can be called without creating an instance of the class and is used to convert a database row into a Car object.
    @staticmethod
    def _row_to_car(row) -> Car:
        return Car(
            car_id=row["car_id"],
            make=row["make"],
            model=row["model"],
            year=row["year"],
            mileage=row["mileage"],
            available_now=bool(row["available_now"]),
            minimum_rent_period=row["minimum_rent_period"],
            maximum_rent_period=row["maximum_rent_period"],
            daily_rate=row["daily_rate"],
            category=row["category"],
            eco_rating=row["eco_rating"],
        )

#   The BookingRepository class handles rental bookings, allowing for creating new bookings, updating booking status, and retrieving bookings by ID or status. 
#   Additionally, the format_car_rows function formats car data into a compact string representation for display in the CLI.
class BookingRepository:
    """Persistence methods for rental bookings."""

    # The __init__ method initializes the BookingRepository with a DatabaseManager instance, which is used for executing database operations.
    def __init__(self, database: DatabaseManager) -> None:
        self.database = database

    # The create method takes a Booking object as input, inserts it into the bookings table in the database, and returns the created Booking object with the assigned booking_id.
    def create(self, booking: Booking) -> Booking:
        cursor = self.database.execute(
            """
            INSERT INTO bookings (
                user_id, car_id, start_date, end_date, pickup_location,
                extras, total_fee, status, trip_type, insurance_selected
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                booking.user_id,
                booking.car_id,
                booking.start_date,
                booking.end_date,
                booking.pickup_location,
                "none",
                booking.total_fee,
                booking.status,
                "standard",
                int(booking.insurance_selected),
            ),
        )
        booking.booking_id = cursor.lastrowid
        return booking

    # The delete method removes a booking record from the database by booking ID.
    def delete(self, booking_id: int) -> None:
        self.database.execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,))

    # The update_status method takes a booking_id and a status as input and updates the status of the corresponding booking record in the database.
    def update_status(self, booking_id: int, status: str) -> None:
        self.database.execute(
            "UPDATE bookings SET status = ? WHERE booking_id = ?",
            (status, booking_id),
        )

    # The get_by_id method retrieves a booking record from the database based on the provided booking_id. If a matching booking is found, it returns a Booking object; otherwise, it returns None.
    def get_by_id(self, booking_id: int) -> Optional[Booking]:
        row = self.database.execute(
            "SELECT * FROM bookings WHERE booking_id = ?",
            (booking_id,),
        ).fetchone()
        return self._row_to_booking(row) if row else None

    #   The list_by_status method retrieves all booking records from the database that match the provided status, orders them by booking_id, and returns a list of Booking objects representing the bookings with the specified status.
    def list_by_status(self, status: str) -> List[Booking]:
        rows = self.database.execute(
            "SELECT * FROM bookings WHERE status = ? ORDER BY booking_id",
            (status,),
        ).fetchall()
        return [self._row_to_booking(row) for row in rows]

    # The list_by_user method retrieves all bookings created by a specific user and returns them ordered by booking ID.
    def list_by_user(self, user_id: int) -> List[Booking]:
        rows = self.database.execute(
            "SELECT * FROM bookings WHERE user_id = ? ORDER BY booking_id",
            (user_id,),
        ).fetchall()
        return [self._row_to_booking(row) for row in rows]

    #   The list_all method retrieves all booking records from the database, orders them by booking_id, and returns a list of Booking objects representing all rental bookings in the system.
    def list_all(self) -> List[Booking]:
        rows = self.database.execute("SELECT * FROM bookings ORDER BY booking_id").fetchall()
        return [self._row_to_booking(row) for row in rows]

    #   The @staticmethod decorator indicates that the _row_to_booking method is a static method that does not depend on the instance of the BookingRepository class.
    @staticmethod
    #   The _row_to_booking method is a helper function that converts a database row into a Booking object. 
    #   It takes a database row as input and returns a Booking object with the corresponding attributes populated from the row data.
    def _row_to_booking(row) -> Booking:
        return Booking(
            booking_id=row["booking_id"],
            user_id=row["user_id"],
            car_id=row["car_id"],
            start_date=row["start_date"],
            end_date=row["end_date"],
            pickup_location=row["pickup_location"],
            total_fee=row["total_fee"],
            status=row["status"],
            insurance_selected=bool(row["insurance_selected"]),
        )

#   The format_car_rows function formats car data into a compact string representation for display in the CLI. 
#   It takes an iterable of Car objects as input and returns a list of formatted strings, where each string contains the car's ID, year, make, model, daily rate, rental period, and availability status.    
def format_car_rows(cars: Iterable[Car]) -> List[str]:
    """Create compact display rows for CLI output."""

    return [
        (
            f"[{car.car_id}] {car.year} {car.make} {car.model} | "
            f"mileage {car.mileage} | "
            f"rate ${car.daily_rate:.2f}/day | "
            f"rent {car.minimum_rent_period}-{car.maximum_rent_period} days | "
            f"available {'yes' if car.available_now else 'no'}"
        )
        for car in cars
    ]
