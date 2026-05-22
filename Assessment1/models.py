"""Domain models for the car rental system."""
# The models.py file defines the domain models for the car rental system, including the User, Car, and Booking classes. These classes represent the core entities in the application and are used to structure the data throughout the system. 
# Each class is defined as a dataclass, which provides a convenient way to create classes that primarily store data without needing to write boilerplate code for initialization and representation. 
from dataclasses import dataclass
from typing import Optional

# The User class represents an application user with a role-based permission model. It includes attributes for user ID, username, password hash, and role (e.g., admin or customer). 
# The user_id attribute is optional and can be None when creating a new user before it is saved to the database.
@dataclass
class User:
    """Application user with a role-based permission model."""

    user_id: Optional[int]
    username: str
    password_hash: str
    email: str
    phone: str
    role: str

# The Car class represents a car in the inventory with attributes such as make, model, year, mileage, availability status, rental period limits, daily rate, category, and eco rating. 
# The car_id attribute is optional and can be None when creating a new car before it is saved to the database.
@dataclass
class Car:
    """Car inventory record."""

    car_id: Optional[int]
    make: str
    model: str
    year: int
    mileage: int
    available_now: bool
    minimum_rent_period: int
    maximum_rent_period: int
    daily_rate: float
    category: str
    eco_rating: int

# The Booking class represents a rental booking placed by a customer, including attributes for booking ID, user ID, car ID, rental dates, pickup location, total fee, booking status, and insurance selection. 
# The booking_id attribute is optional and can be None when creating a new booking before it is saved to the database.
@dataclass
class Booking:
    """Rental booking placed by a customer."""

    booking_id: Optional[int]
    user_id: int
    car_id: int
    start_date: str
    end_date: str
    pickup_location: str
    total_fee: float
    status: str
    insurance_selected: bool
