"""Command-line interface for the car rental system."""
# The cli.py file implements the command-line interface (CLI) for the car rental system, providing an interactive menu-driven application for users to register, log in, manage cars, and create bookings. 
# It defines a Session dataclass to track the current logged-in user and a CarRentalCLI class that contains methods for displaying menus and handling user input based on their role (guest, admin, or customer). 
# The CLI interacts with various services and repositories to perform the necessary operations for managing users, cars, and bookings in the system.
from dataclasses import dataclass
from datetime import date
from getpass import getpass
from pathlib import Path
from typing import Optional
from bootstrap import initialize_database
from database import DatabaseManager
from decorators import admin_only
from repositories import BookingRepository, CarRepository, UserRepository, format_car_rows
from services import AuthService, BookingService, CarService

#  Added dataclass decorator to Session for better structure and readability
@dataclass 
# Session class to track the current logged-in user, including their ID, username, and role (admin or customer)
class Session:
    """Tracks the current logged-in user."""

    user_id: int
    username: str
    role: str

# CarRentalCLI class implements the command-line interface for the car rental system, providing interactive menus for guests, admins, and customers to perform various actions such as registering, logging in, managing cars, and creating bookings.
class CarRentalCLI:
    """Interactive menu-driven application."""

    PICKUP_LOCATIONS = [
        "Auckland CBD",
        "Auckland Airport",
        "North Shore",
    ]

    # The constructor initializes the database connection, repositories, and services needed for the CLI to function. It also sets up a variable to track the current user session.
    def __init__(self, db_path: Path) -> None:
        # Initialize the database connection and set up repositories for users, cars, and bookings
        database = DatabaseManager(db_path)
        initialize_database(database)

        # Create repositories for users, cars, and bookings to interact with the database
        user_repository = UserRepository(database)
        car_repository = CarRepository(database)
        booking_repository = BookingRepository(database)

        # Initialize services for authentication, car management, and booking management
        self.auth_service = AuthService(user_repository)
        self.car_service = CarService(car_repository)
        self.booking_service = BookingService(booking_repository, car_repository)
        self.current_session: Optional[Session] = None

    # The run method starts the CLI application, displaying a welcome message and entering a loop that shows different menus based on whether the user is logged in and their role (admin or customer).
    def run(self) -> None:
        print("Welcome to the SmartDrive Car Rental System")
        while True:
            if self.current_session is None:
                if not self._guest_menu():
                    break
            elif self.current_session.role == "admin":
                self._admin_menu()
            else:
                self._customer_menu()

    # The _guest_menu method displays options for guests to register, log in, or exit the application. It handles user input and calls the appropriate methods based on the user's choice.
    def _guest_menu(self) -> bool:
        print("\nGuest Menu")
        print("1. Register customer")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        # Based on the user's choice, the method calls the corresponding function to register a new customer, log in an existing user, or exit the application. It also handles invalid input by displaying an error message.
        if choice == "1":
            self._register_customer()
        elif choice == "2":
            self._login()
        elif choice == "3":
            print("Goodbye.")
            return False
        else:
            print("Invalid choice.")
        return True

    # The _register_customer method prompts the user for a username and password, then attempts to register a new customer account using the AuthService. It handles any errors that may occur during registration and provides feedback to the user.
    def _register_customer(self) -> None:
        print("\nCustomer Registration")
        username = input("Username: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone: ").strip()
        password = getpass("Password: ").strip()
        try:
            self.auth_service.register_user(username, password, email, phone, "customer")
            print("Customer account created successfully.")
        except ValueError as error:
            print(error)

    # The _login method prompts the user for their username and password, then attempts to log in using the AuthService. If successful, it creates a new Session object to track the logged-in user and provides a welcome message. If login fails, it displays an error message.
    def _login(self) -> None:
        print("\nLogin")
        username = input("Username: ").strip()
        password = getpass("Password: ").strip()
        try:
            user = self.auth_service.login(username, password)
            self.current_session = Session(user.user_id or 0, user.username, user.role)
            print(f"Welcome, {user.username} ({user.role}).")
        except ValueError as error:
            print(error)

    # The _admin_menu method displays options for admin users to manage cars and bookings. It handles user input and calls the appropriate methods based on the admin's choice, such as viewing all cars, adding a new car, updating or deleting existing cars, reviewing pending bookings, and viewing all bookings.
    def _admin_menu(self) -> None:
        print("\nAdmin Menu")
        print("1. Manage cars")
        print("2. Manage bookings")
        print("3. Manage users")
        print("4. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            self._manage_cars_menu()
        elif choice == "2":
            self._manage_bookings_menu()
        elif choice == "3":
            self._manage_users_menu()
        elif choice == "4":
            self.current_session = None
            print("Logged out.")
        else:
            print("Invalid choice.")

    # The _manage_cars_menu method provides options for admin users to manage the car inventory. It allows admins to view all cars, add new cars, update existing cars, delete cars, or go back to the previous menu. The method handles user input and calls the appropriate functions based on the admin's choice.
    def _manage_cars_menu(self) -> None:
        while True:
            print("\nManage Cars")
            print("1. View all cars")
            print("2. Add a car")
            print("3. Update a car")
            print("4. Delete a car")
            print("5. Back")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self._display_cars(self.car_service.list_all_cars())
            elif choice == "2":
                self._add_car()
            elif choice == "3":
                self._update_car()
            elif choice == "4":
                self._delete_car()
            elif choice == "5":
                return
            else:
                print("Invalid choice.")

    # The _manage_bookings_menu method provides options for admin users to manage bookings. It allows admins to view all bookings, review pending bookings, or go back to the previous menu. The method handles user input and calls the appropriate functions based on the admin's choice, such as listing all bookings or reviewing pending bookings for approval.
    def _manage_bookings_menu(self) -> None:
        while True:
            print("\nManage Bookings")
            print("1. View all bookings")
            print("2. Review pending bookings")
            print("3. Back")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self._display_bookings(self.booking_service.list_all_bookings())
            elif choice == "2":
                self._review_bookings()
            elif choice == "3":
                return
            else:
                print("Invalid choice.")

    # The _manage_users_menu method provides options for admin users to manage user accounts. It allows admins to view all users, add new users, update existing users, delete users, or go back to the previous menu. The method handles user input and calls the appropriate functions based on the admin's choice.
    def _manage_users_menu(self) -> None:
        while True:
            print("\nManage Users")
            print("1. View all users")
            print("2. Add a user")
            print("3. Update a user")
            print("4. Delete a user")
            print("5. Back")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self._display_users()
            elif choice == "2":
                self._add_user()
            elif choice == "3":
                self._update_user()
            elif choice == "4":
                self._delete_user()
            elif choice == "5":
                return
            else:
                print("Invalid choice.")

    #   The _customer_menu method displays the customer-facing rental actions, including
    #   browsing cars, creating standard or smart bookings, viewing bookings, paying
    #   approved bookings, cancelling pending bookings, and logging out.
    def _customer_menu(self) -> None:
        print("\nCustomer Menu")
        print("1. View available cars")
        print("2. Create booking")
        print("3. Smart booking")
        print("4. View my bookings")
        print("5. Pay for booking")
        print("6. Cancel booking")
        print("7. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            self._display_cars(self.car_service.list_available_cars())
        elif choice == "2":
            self._create_booking()
        elif choice == "3":
            self._smart_booking()
        elif choice == "4":
            self._view_my_bookings()
        elif choice == "5":
            self._pay_for_booking()
        elif choice == "6":
            self._cancel_booking()
        elif choice == "7":
            self.current_session = None
            print("Logged out.")
        else:
            print("Invalid choice.")

    # The _add_car method is decorated with @admin_only, ensuring that only admin users can access this functionality. It prompts the admin for car details, collects the input into a payload, and attempts to add a new car to the inventory using the CarService. It handles any errors that may occur during this process and provides feedback to the admin.
    @admin_only
    def _add_car(self) -> None:
        print("\nAdd Car")
        try:
            payload = self._collect_car_payload()
            car = self.car_service.add_car(**payload)
            print(f"Car {car.car_id} added successfully.")
        except ValueError as error:
            print(error)

    #   The _update_car method is also decorated with @admin_only, allowing only admin users to update car details. It prompts the admin for the car ID and new details, collects the input into a payload, and attempts to update the specified car using the CarService. It handles any errors that may occur during this process and provides feedback to the admin.
    @admin_only
    def _update_car(self) -> None:
        print("\nUpdate Car")
        while True:
            try:
                car_id = int(input("Car ID: ").strip())
                break
            except ValueError:
                print("Invalid car ID. Please enter a number.")

        try:
            payload = self._collect_car_payload()
            car = self.car_service.update_car(car_id, **payload)
            print(f"Car {car.car_id} updated successfully.")
        except ValueError as error:
            print(error)

    # The _delete_car method is decorated with @admin_only, ensuring that only admin users can delete cars from the inventory. It prompts the admin for the car ID, attempts to delete the specified car using the CarService, and handles any errors that may occur during this process, providing feedback to the admin.
    @admin_only
    def _delete_car(self) -> None:
        print("\nDelete Car")
        while True:
            try:
                car_id = int(input("Car ID: ").strip())
                break
            except ValueError:
                print("Invalid car ID. Please enter a number.")

        try:
            self.car_service.delete_car(car_id)
            print("Car deleted successfully.")
        except ValueError as error:
            print(error)

    # The _add_user method is decorated with @admin_only, allowing only admin users to add new user accounts. It prompts the admin for user details, collects the input into a payload, and attempts to register a new user using the AuthService. It handles any errors that may occur during this process and provides feedback to the admin.
    @admin_only
    def _add_user(self) -> None:
        print("\nAdd User")
        try:
            payload = self._collect_user_payload(include_password=True)
            self.auth_service.register_user(
                payload["username"],
                payload["password"],
                payload["email"],
                payload["phone"],
                payload["role"],
            )
            print("User added successfully.")
        except ValueError as error:
            print(error)

    # The _update_user method is decorated with @admin_only, allowing only admin users to update existing user accounts. It prompts the admin for the user ID and new details, collects the input into a payload, and attempts to update the specified user using the AuthService. It handles any errors that may occur during this process and provides feedback to the admin.
    @admin_only
    def _update_user(self) -> None:
        print("\nUpdate User")
        while True:
            try:
                user_id = int(input("User ID: ").strip())
                break
            except ValueError:
                print("Invalid user ID. Please enter a number.")

        try:
            payload = self._collect_user_payload(include_password=True, password_optional=True)
            user = self.auth_service.update_user(
                user_id=user_id,
                username=payload["username"],
                email=payload["email"],
                phone=payload["phone"],
                role=payload["role"],
                password=payload["password"],
            )
            print(f"User {user.user_id} updated successfully.")
        except ValueError as error:
            print(error)

    # The _delete_user method is decorated with @admin_only, ensuring that only admin users can delete user accounts. It prompts the admin for the user ID, attempts to delete the specified user using the AuthService, and handles any errors that may occur during this process, providing feedback to the admin.
    @admin_only
    def _delete_user(self) -> None:
        print("\nDelete User")
        while True:
            try:
                user_id = int(input("User ID: ").strip())
                break
            except ValueError:
                print("Invalid user ID. Please enter a number.")

        try:
            self.auth_service.delete_user(user_id, self.current_session.user_id)
            print("User deleted successfully.")
        except ValueError as error:
            print(error)

    # The _review_bookings method is decorated with @admin_only, allowing only admin users to review pending bookings. It retrieves the list of pending bookings using the BookingService, displays them to the admin, and prompts for a booking ID and approval decision. It then attempts to review the specified booking based on the admin's input and provides feedback on the booking's new status.
    @admin_only
    def _review_bookings(self) -> None:
        pending = self.booking_service.list_pending_bookings()
        if not pending:
            print("No pending bookings.")
            return

        #   Display the list of pending bookings to the admin and prompt them to select a booking ID for review. The admin can then decide whether to approve or reject the booking, and the method will update the booking's status accordingly, providing feedback on the outcome of the review process.
        self._display_bookings(pending)
        while True:
            try:
                booking_id = int(input("Booking ID to review: ").strip())
                break
            except ValueError:
                print("Invalid booking ID. Please enter a number.")

        while True:
            decision = input("Approve booking? (y/n): ").strip().lower()
            if decision in {"y", "n"}:
                break
            print("Invalid input. Please enter y or n.")

        try:
            booking = self.booking_service.review_booking(booking_id, decision == "y")
            print(f"Booking #{booking.booking_id} is now {booking.status}.")
        except ValueError as error:
            print(error)

    # The _create_booking method allows customers to create a new booking. It prompts the customer for the car ID, rental dates, pickup location, and insurance option, then attempts to create a new booking using the BookingService. It handles any errors that may occur during this process and provides feedback to the customer, including details of the booking and the rental quote.
    def _create_booking(self) -> None:
        if self.current_session is None:
            print("Please log in first.")
            return

        # Display available cars to the customer before prompting for booking details
        self._display_cars(self.car_service.list_available_cars())
        try:
            car_id = int(input("Car ID: ").strip())
            self._finish_booking(car_id)
        except ValueError as error:
            print(error)

    # The _smart_booking method asks a few simple questions and recommends cars before booking.
    def _smart_booking(self) -> None:
        if self.current_session is None:
            print("Please log in first.")
            return
        try:
            print("\nSmart Booking Assistant")
            print("Answer a few quick questions and the system will suggest suitable cars.")
            trip_purpose = self._choose_trip_purpose()
            passenger_count = self._choose_passenger_count()
            priority = self._choose_priority()

            recommended_cars = self.car_service.recommend_cars(
                trip_purpose=trip_purpose,
                passenger_count=passenger_count,
                priority=priority,
            )
            if not recommended_cars:
                print("No suitable cars were found for that preference set.")
                return

            print("\nRecommended cars for your trip")
            self._display_cars(recommended_cars)
            car_id = int(input("Choose one of the recommended Car IDs: ").strip())
            recommended_ids = {car.car_id for car in recommended_cars}
            if car_id not in recommended_ids:
                raise ValueError("Please choose a car ID from the recommended list.")
            self._finish_booking(car_id)
        except ValueError as error:
            print(error)

    # The _finish_booking method completes the booking after the car has been chosen.
    def _finish_booking(self, car_id: int) -> None:
        start_date = input("Start date (YYYY-MM-DD): ").strip()
        end_date = input("End date (YYYY-MM-DD): ").strip()
        # Fail early on invalid dates before asking for more booking details.
        self._validate_date_range(start_date, end_date)
        pickup_location = self._choose_pickup_location()
        insurance_selected = self._choose_insurance()

        booking, quote = self.booking_service.create_booking(
            user_id=self.current_session.user_id,
            car_id=car_id,
            start_date=start_date,
            end_date=end_date,
            pickup_location=pickup_location,
            insurance_selected=insurance_selected,
        )
        print(
            f"Booking #{booking.booking_id} created. "
            f"Days: {quote.rental_days}, base ${quote.base_cost:.2f}, "
            f"insurance ${quote.insurance_cost:.2f}, total ${quote.total_cost:.2f}."
        )

    @staticmethod
    def _validate_date_range(start_date_text: str, end_date_text: str) -> None:
        # This lightweight CLI check improves the user experience; the
        # service layer still performs the full rental-period validation.
        start = date.fromisoformat(start_date_text)
        end = date.fromisoformat(end_date_text)
        if end < start:
            raise ValueError("End date must be after start date.")

    # The _view_my_bookings method shows the current customer's bookings.
    def _view_my_bookings(self) -> None:
        if self.current_session is None:
            print("Please log in first.")
            return
        bookings = self.booking_service.list_user_bookings(self.current_session.user_id)
        if not bookings:
            print("You have no bookings.")
            return
        self._display_bookings(bookings)

    # The _cancel_booking method lets the current customer cancel one of their pending bookings.
    def _cancel_booking(self) -> None:
        if self.current_session is None:
            print("Please log in first.")
            return
        try:
            booking_id = int(input("Booking ID to cancel: ").strip())
            self.booking_service.cancel_booking(booking_id, self.current_session.user_id)
            print("Booking cancelled successfully.")
        except ValueError as error:
            print(error)

    def _pay_for_booking(self) -> None:
        if self.current_session is None:
            print("Please log in first.")
            return
        approved_bookings = [
            booking
            for booking in self.booking_service.list_user_bookings(
                self.current_session.user_id
            )
            if booking.status == "approved"
        ]
        if not approved_bookings:
            print("You have no approved bookings waiting for payment.")
            return

        self._display_bookings(approved_bookings)
        try:
            booking_id = int(input("Booking ID to pay: ").strip())
            booking = self.booking_service.pay_booking(
                booking_id, self.current_session.user_id
            )
            print(f"Booking #{booking.booking_id} paid successfully.")
        except ValueError as error:
            print(error)

    #   The _choose_pickup_location method displays a list of predefined pickup locations to the user and prompts them to select one. It validates the user's input and returns the chosen pickup location, or raises an error if the input is invalid.
    def _choose_pickup_location(self) -> str:
        print("Pickup locations")
        for index, location in enumerate(self.PICKUP_LOCATIONS, start=1):
            print(f"{index}. {location}")
        choice = int(input("Choose pickup location: ").strip())
        if 1 <= choice <= len(self.PICKUP_LOCATIONS):
            return self.PICKUP_LOCATIONS[choice - 1]
        raise ValueError("Invalid pickup location.")

    # The _choose_insurance method prompts the user to decide whether they want to add insurance to their booking. It accepts a simple 'y' or 'n' input, returning True for 'y' and False for 'n'. If the user enters an invalid input, it raises a ValueError to indicate that the input was not recognized.
    def _choose_insurance(self) -> bool:
        choice = input("Add insurance? (y/n): ").strip().lower()
        if choice == "y":
            return True
        if choice == "n":
            return False
        raise ValueError("Invalid input. Please enter y or n.")

    # The _choose_trip_purpose method presents the user with a list of common trip purposes and prompts them to select one. It maps the user's choice to a corresponding trip purpose string and returns it. If the user enters an invalid choice, it raises a ValueError.
    def _choose_trip_purpose(self) -> str:
        print("\n1. What type of trip is this?")
        print("1. City travel")
        print("2. Family outing")
        print("3. Business travel")
        print("4. Long-distance trip")
        choice = input("Choose the best match: ").strip()
        purpose_map = {
            "1": "city",
            "2": "family",
            "3": "business",
            "4": "long trip",
        }
        if choice in purpose_map:
            return purpose_map[choice]
        raise ValueError("Invalid trip purpose.")

    # The _choose_passenger_count method asks the user how many people are traveling and provides two options: "1-2 people" or "3-5 people". It maps the user's choice to a corresponding passenger count string and returns it. If the user enters an invalid choice, it raises a ValueError.
    def _choose_passenger_count(self) -> str:
        print("\n2. How many people are travelling?")
        print("1. 1-2 people")
        print("2. 3-5 people")
        choice = input("Choose the best match: ").strip()
        passenger_map = {
            "1": "1-2",
            "2": "3-5",
        }
        if choice in passenger_map:
            return passenger_map[choice]
        raise ValueError("Invalid passenger count.")

    #   The _choose_priority method asks the user to select what matters most to them when choosing a car for their trip. It provides four options: lower price, newer car, lower mileage, or longer rental flexibility. The user's choice is mapped to a corresponding priority string and returned. If the user enters an invalid choice, it raises a ValueError.
    def _choose_priority(self) -> str:
        print("\n3. What matters most to you?")
        print("1. Lower price")
        print("2. Newer car")
        print("3. Lower mileage")
        print("4. Longer rental flexibility")
        choice = input("Choose one priority: ").strip()
        priority_map = {
            "1": "lower price",
            "2": "newer car",
            "3": "lower mileage",
            "4": "longer rental flexibility",
        }
        if choice in priority_map:
            return priority_map[choice]
        raise ValueError("Invalid priority.")

    # The _display_cars method takes a list of Car objects and formats them into compact display rows for CLI output. It uses the format_car_rows function to create readable strings for each car, which are then printed to the console.
    @staticmethod
    def _display_cars(cars) -> None:
        rows = format_car_rows(cars)
        if not rows:
            print("No cars found.")
            return
        for row in rows:
            print(row)

    #   The _display_bookings method takes a list of Booking objects and formats them into readable strings for CLI output. It shows the car name, rental dates, pickup location, total fee, and booking status.
    def _display_bookings(self, bookings) -> None:
        if not bookings:
            print("No bookings found.")
            return
        for booking in bookings:
            car = self.car_service.car_repository.get_by_id(booking.car_id)
            car_name = f"{car.year} {car.make} {car.model}" if car else f"Car {booking.car_id}"
            print(
                f"[{booking.booking_id}] {car_name} | "
                f"{booking.start_date} to {booking.end_date} | {booking.pickup_location} | "
                f"total=${booking.total_fee:.2f} | status={booking.status}"
            )

    # The _display_users method retrieves a list of all users from the AuthService and displays their details in a formatted manner. It shows the user ID, username, email, phone number, and role for each user. If no users are found, it displays an appropriate message.
    def _display_users(self) -> None:
        users = self.auth_service.list_all_users()
        if not users:
            print("No users found.")
            return
        for user in users:
            print(
                f"[{user.user_id}] {user.username} | "
                f"email={user.email or '-'} | phone={user.phone or '-'} | role={user.role}"
            )

    # The _collect_user_payload method prompts the admin for user details such as username, email, phone, role, and password (if required). It collects the input into a dictionary payload that can be used for creating or updating user accounts. The method also handles optional password input when updating a user, allowing the admin to leave the password blank to keep the current password unchanged.
    @staticmethod
    def _collect_user_payload(include_password: bool, password_optional: bool = False) -> dict:
        payload = {
            "username": input("Username: ").strip(),
            "email": input("Email: ").strip(),
            "phone": input("Phone: ").strip(),
            "role": input("Role (admin/customer): ").strip().lower(),
            "password": "",
        }
        if include_password:
            if password_optional:
                payload["password"] = getpass("New password (leave blank to keep current): ").strip()
            else:
                payload["password"] = getpass("Password: ").strip()
        return payload

    #   The _collect_car_payload method prompts the admin for the core car details needed by the system.
    #   Category and eco rating are no longer entered through the menu and are stored with simple default values.
    @staticmethod
    def _collect_car_payload() -> dict:
        return {
            "make": input("Make (e.g. BYD): ").strip(),
            "model": input("Model (e.g. Dolphin): ").strip(),
            "year": int(input("Year (e.g. 2025): ").strip()),
            "mileage": int(input("Mileage (e.g. 10000): ").strip()),
            "available_now": input("Available now? (y/n): ").strip().lower() == "y",
            "minimum_rent_period": int(input("Minimum rent period in days (e.g. 1): ").strip()),
            "maximum_rent_period": int(input("Maximum rent period in days (e.g. 14): ").strip()),
            "daily_rate": float(input("Daily rate (e.g. 100): ").strip()),
            "category": "Standard",
            "eco_rating": 3,
        }
