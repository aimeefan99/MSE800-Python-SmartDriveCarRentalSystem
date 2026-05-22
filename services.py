"""Business services for registration, inventory, booking, and pricing."""
# The services.py file contains the business logic for the car rental system, including user authentication, car inventory management, and booking workflow.
import hashlib
from dataclasses import dataclass
from datetime import date
from typing import List, Tuple
from models import Booking, Car, User
from repositories import BookingRepository, CarRepository, UserRepository

@dataclass
# The RentalQuote class represents the result of a rental fee calculation, including the number of rental days, base cost, insurance cost, and total cost. It is used to provide customers with a detailed breakdown of their rental fees when creating a booking.
class RentalQuote:
    """Result of rental fee calculation."""

    rental_days: int
    base_cost: float
    insurance_cost: float
    total_cost: float

#   The AuthService class handles user registration and login functionality. It interacts with the UserRepository to create new users and authenticate existing users based on their username and password. The register_user method allows for creating new users with a specified role (admin or customer), while the login method verifies user credentials and returns the corresponding User object if authentication is successful.
class AuthService:
    """Handles registration and login."""

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    #   The register_user method allows for creating a new user in the system. It takes a username, password, and role as input, validates the role and checks for existing usernames to prevent duplicates. If the input is valid, it creates a new User object with a hashed password and saves it to the repository, returning the created user.
    def register_user(
        self,
        username: str,
        password: str,
        email: str,
        phone: str,
        role: str,
    ) -> User:
        if role not in {"admin", "customer"}:
            raise ValueError("Role must be admin or customer.")
        if self.user_repository.find_by_username(username):
            raise ValueError("Username already exists.")
        user = User(
            user_id=None,
            username=username,
            password_hash=hashlib.sha256(password.encode()).hexdigest(),
            email=email,
            phone=phone,
            role=role,
        )
        return self.user_repository.create(user)

    #   The login method authenticates a user by verifying their username and password. It retrieves the user from the repository based on the provided username, checks if the user exists, and compares the hashed password with the stored hash. If authentication is successful, it returns the User object; otherwise, it raises an error indicating that the user was not found or the password is invalid.
    def login(self, username: str, password: str) -> User:
        user = self.user_repository.find_by_username(username)
        if user is None:
            raise ValueError("User not found.")
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash != user.password_hash:
            raise ValueError("Invalid password.")
        return user

    def list_all_users(self) -> List[User]:
        return self.user_repository.list_all()

    def update_user(
        self,
        user_id: int,
        username: str,
        email: str,
        phone: str,
        role: str,
        password: str = "",
    ) -> User:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found.")
        if role not in {"admin", "customer"}:
            raise ValueError("Role must be admin or customer.")

        existing_user = self.user_repository.find_by_username(username)
        if existing_user is not None and existing_user.user_id != user_id:
            raise ValueError("Username already exists.")

        user.username = username
        user.email = email
        user.phone = phone
        user.role = role
        if password:
            user.password_hash = hashlib.sha256(password.encode()).hexdigest()

        self.user_repository.update(user)
        return user

    def delete_user(self, user_id: int, current_user_id: int) -> None:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found.")
        if user.user_id == current_user_id:
            raise ValueError("You cannot delete the account you are currently using.")
        if user.username == "admin":
            raise ValueError("The default admin account cannot be deleted.")
        self.user_repository.delete(user_id)

#   The CarService class provides functionality for managing the car inventory, including adding new cars, updating existing cars, deleting cars, and listing available cars. It interacts with the CarRepository to perform these operations and ensures that the necessary validations are in place when modifying the car inventory.
class CarService:
    """Admin-facing car inventory service."""

    def __init__(self, car_repository: CarRepository) -> None:
        self.car_repository = car_repository

    def add_car(self, **payload) -> Car:
        car = Car(car_id=None, **payload)
        return self.car_repository.create(car)

    def update_car(self, car_id: int, **payload) -> Car:
        car = self.car_repository.get_by_id(car_id)
        if car is None:
            raise ValueError("Car not found.")
        for key, value in payload.items():
            setattr(car, key, value)
        self.car_repository.update(car)
        return car

    def delete_car(self, car_id: int) -> None:
        if self.car_repository.get_by_id(car_id) is None:
            raise ValueError("Car not found.")
        self.car_repository.delete(car_id)

    def list_all_cars(self) -> List[Car]:
        return self.car_repository.list_all()

    def list_available_cars(self) -> List[Car]:
        return self.car_repository.list_available()

    # The recommend_cars method provides a lightweight smart-booking recommendation based on customer answers.
    def recommend_cars(self, trip_purpose: str, passenger_count: str, priority: str) -> List[Car]:
        cars = self.car_repository.list_available()
        scored_cars = []

        for car in cars:
            score = 0

            # First prefer cars that match the group size reasonably well.
            if passenger_count == "3-5":
                if car.category in {"SUV", "Van", "Standard"}:
                    score += 30
                else:
                    score -= 25
            elif passenger_count == "1-2":
                if car.category in {"Compact", "Sedan", "Hybrid"}:
                    score += 12

            # Then shape the result around the trip type.
            if trip_purpose == "city":
                if car.category in {"Compact", "Sedan", "Hybrid"}:
                    score += 18
                if car.daily_rate <= 90:
                    score += 12
                if car.mileage <= 20000:
                    score += 6
            elif trip_purpose == "family":
                if car.category in {"SUV", "Van", "Standard"}:
                    score += 25
                else:
                    score -= 20
            elif trip_purpose == "business":
                if car.category in {"Sedan", "Hybrid"}:
                    score += 12
                score += (car.year - 2020) * 4
            elif trip_purpose == "long trip":
                if car.category in {"SUV", "Sedan", "Hybrid"}:
                    score += 10
                score += car.maximum_rent_period * 2
                if car.mileage <= 15000:
                    score += 10

            # Finally apply the customer's top priority as a stronger tie-breaker.
            if priority == "lower price":
                score += max(0, 180 - int(car.daily_rate))
            elif priority == "newer car":
                score += (car.year - 2020) * 10
            elif priority == "lower mileage":
                score += max(0, 50000 - car.mileage) / 1000
            elif priority == "longer rental flexibility":
                score += car.maximum_rent_period * 5

            scored_cars.append((score, car))
            
        # Sort by score, then by maximum rent period, then by year, then by daily rate (lowest first)
        scored_cars.sort(
            key=lambda item: (item[0], item[1].maximum_rent_period, item[1].year, -item[1].daily_rate),
            reverse=True,
        )
        return [car for _, car in scored_cars[:3]]

# The BookingService class manages the rental workflow for both customers and admins. 
# It allows customers to create new bookings by selecting a car, specifying rental dates, and choosing additional options like insurance. 
# The service calculates the rental quote based on the selected car and rental period. 
# For admins, it provides functionality to review pending bookings and approve or reject them, which updates the booking status and car availability accordingly. 
# The service also includes methods to list pending and all bookings for administrative purposes.
class BookingService:
    """Customer and admin rental workflow service."""

    INSURANCE_DAILY_RATE = 20.0

    # The __init__ method initializes the BookingService with the necessary repositories for managing bookings and cars. It takes instances of BookingRepository and CarRepository as parameters and assigns them to instance variables for use in the service's methods.
    def __init__(
        self,
        booking_repository: BookingRepository,
        car_repository: CarRepository,
    ) -> None:
        self.booking_repository = booking_repository
        self.car_repository = car_repository

    # The create_booking method allows customers to create a new booking by providing their user ID, selected car ID, rental dates, pickup location, and insurance option. It validates the car's availability and rental period, calculates the rental quote, and creates a new booking in the repository. The method returns the created Booking object along with the RentalQuote for the customer's reference.
    def create_booking(
        self,
        user_id: int,
        car_id: int,
        start_date: str,
        end_date: str,
        pickup_location: str,
        insurance_selected: bool,
    ) -> Tuple[Booking, RentalQuote]:
        car = self.car_repository.get_by_id(car_id)
        if car is None:
            raise ValueError("Car not found.")
        if not car.available_now:
            raise ValueError("Selected car is not available right now.")

        rental_days = self._calculate_days(start_date, end_date)
        if rental_days < car.minimum_rent_period or rental_days > car.maximum_rent_period:
            raise ValueError("Rental period is outside the car policy.")

        quote = self._calculate_quote(
            car=car,
            rental_days=rental_days,
            insurance_selected=insurance_selected,
        )
        booking = Booking(
            booking_id=None,
            user_id=user_id,
            car_id=car_id,
            start_date=start_date,
            end_date=end_date,
            pickup_location=pickup_location,
            total_fee=quote.total_cost,
            status="pending",
            insurance_selected=insurance_selected,
        )
        created = self.booking_repository.create(booking)
        return created, quote

    # The review_booking method allows admins to review a pending booking by its ID and either approve or reject it. It updates the booking's status accordingly and, if approved, marks the associated car as unavailable. The method returns the updated Booking object after the review process is complete.
    def review_booking(self, booking_id: int, approved: bool) -> Booking:
        booking = self.booking_repository.get_by_id(booking_id)
        if booking is None:
            raise ValueError("Booking not found.")
        if booking.status != "pending":
            raise ValueError("Booking has already been reviewed.")

        status = "approved" if approved else "rejected"
        self.booking_repository.update_status(booking_id, status)
        updated = self.booking_repository.get_by_id(booking_id)
        assert updated is not None

        car = self.car_repository.get_by_id(updated.car_id)
        if approved and car is not None:
            car.available_now = False
            self.car_repository.update(car)

        return updated

    def pay_booking(self, booking_id: int, user_id: int) -> Booking:
        """Mark an approved customer booking as paid."""

        booking = self.booking_repository.get_by_id(booking_id)
        if booking is None:
            raise ValueError("Booking not found.")
        if booking.user_id != user_id:
            raise ValueError("You can only pay for your own booking.")
        if booking.status != "approved":
            raise ValueError("Only approved bookings can be paid.")

        self.booking_repository.update_status(booking_id, "paid")
        updated = self.booking_repository.get_by_id(booking_id)
        assert updated is not None
        return updated

    # The list_pending_bookings method retrieves and returns a list of all bookings that are currently in the "pending" status. 
    # This allows admins to view and manage bookings that require their review.
    def list_pending_bookings(self) -> List[Booking]:
        return self.booking_repository.list_by_status("pending")

    # The list_user_bookings method retrieves all bookings created by a specific customer.
    def list_user_bookings(self, user_id: int) -> List[Booking]:
        return self.booking_repository.list_by_user(user_id)

    # The cancel_booking method allows a customer to delete their own pending booking.
    def cancel_booking(self, booking_id: int, user_id: int) -> None:
        booking = self.booking_repository.get_by_id(booking_id)
        if booking is None:
            raise ValueError("Booking not found.")
        if booking.user_id != user_id:
            raise ValueError("You can only cancel your own booking.")
        if booking.status != "pending":
            raise ValueError("Only pending bookings can be cancelled.")
        self.booking_repository.delete(booking_id)

    # The list_all_bookings method retrieves and returns a list of all bookings in the system, regardless of their status. 
    # This provides admins with a comprehensive view of all rental bookings for management and reporting purposes.
    def list_all_bookings(self) -> List[Booking]:
        return self.booking_repository.list_all()

    # The _calculate_quote method computes the rental quote based on the selected car, rental days, and insurance option. 
    # It calculates the base cost by multiplying the car's daily rate by the number of rental days, adds the insurance cost if selected, and returns a RentalQuote object containing the breakdown of costs and total cost for the rental.
    def _calculate_quote(
        self,
        car: Car,
        rental_days: int,
        insurance_selected: bool,
    ) -> RentalQuote:
        base_cost = car.daily_rate * rental_days
        insurance_cost = 0.0
        if insurance_selected:
            insurance_cost = self.INSURANCE_DAILY_RATE * rental_days
        return RentalQuote(
            rental_days=rental_days,
            base_cost=base_cost,
            insurance_cost=insurance_cost,
            total_cost=base_cost + insurance_cost,
        )

    @staticmethod
    #   The _calculate_days method takes the start and end dates of a rental period as input, calculates the number of rental days by finding the difference between the two dates, and returns the total number of days. 
    #   It also validates that the end date is after the start date, raising an error if the dates are invalid.
    def _calculate_days(start_date_text: str, end_date_text: str) -> int:
        start = date.fromisoformat(start_date_text)
        end = date.fromisoformat(end_date_text)
        duration = (end - start).days + 1
        if duration <= 0:
            raise ValueError("End date must be after start date.")
        return duration
