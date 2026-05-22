# Manual Test Cases

This document records the main manual CLI tests for the `SmartDrive Car Rental System`.
The test cases were organised from the full terminal test session and grouped into complete business scenarios.
For each test case, the `Actual Result` section keeps the full terminal output for that scenario instead of a shortened summary.

Note:
Some earlier test cases in this document were captured before the final round of updates, and a few later sections were refreshed to match the latest version of the system. In particular, the Smart Booking example in `Test Case 8` and the payment-related test cases near the end reflect the current menu structure and payment workflow, so some booking IDs and dates are not part of one continuous terminal session.

## Test Scope

The manual tests cover the following system behaviours:

- guest registration and login
- customer booking creation
- Smart Booking Assistant recommendation and booking flow
- invalid input handling
- booking cancellation
- admin user management
- admin booking review
- payment of approved bookings
- final booking status and car availability updates

## Test Environment

- Application: `python3 app.py`
- Database: local SQLite database created by the system
- Default admin account:
  - username: `admin`
  - password: `admin123`

## Test Case 1: Admin Login and Initial Data Check

**Objective**  
Check that the admin account can log in and that the system starts with seeded cars, no bookings, and the default admin user.

**Steps**
1. Start the program.
2. Choose `Login` from the guest menu.
3. Log in with the default admin account.
4. Open `Manage Cars` and view all cars.
5. Open `Manage Bookings` and view all bookings.
6. Open `Manage Users` and view all users.

**Expected Result**
- Admin login is successful.
- The seeded car list is displayed.
- The booking list is empty before any customer booking is created.
- The default admin user is displayed in the user list.

**Actual Result**
```text
Welcome to the SmartDrive Car Rental System

Guest Menu
1. Register customer
2. Login
3. Exit
Choose an option: 2

Login
Username: admin
Password:
Welcome, admin (admin).

Admin Menu
1. Manage cars
2. Manage bookings
3. Manage users
4. Logout
Choose an option: 1

Manage Cars
1. View all cars
2. Add a car
3. Update a car
4. Delete a car
5. Back
Choose an option: 1
[1] 2021 Suzuki Swift | mileage 36000 | rate $58.00/day | rent 1-5 days | available yes
[2] 2023 Toyota Corolla Hybrid | mileage 18000 | rate $76.00/day | rent 1-12 days | available yes
[3] 2024 Mazda 3 | mileage 12000 | rate $88.00/day | rent 1-10 days | available yes
[4] 2022 Mitsubishi Outlander | mileage 27000 | rate $102.00/day | rent 2-18 days | available yes
[5] 2024 Hyundai Tucson | mileage 11000 | rate $112.00/day | rent 2-21 days | available yes
[6] 2024 Tesla Model 3 | mileage 9000 | rate $124.00/day | rent 1-7 days | available yes
[7] 2025 Skoda Superb | mileage 6000 | rate $128.00/day | rent 1-14 days | available yes
[8] 2023 Kia Carnival | mileage 15000 | rate $138.00/day | rent 2-14 days | available yes
[9] 2025 Toyota RAV4 Hybrid | mileage 7000 | rate $145.00/day | rent 3-28 days | available yes
[10] 2025 Mercedes-Benz C200 | mileage 5000 | rate $165.00/day | rent 1-14 days | available yes

Admin Menu
1. Manage cars
2. Manage bookings
3. Manage users
4. Logout
Choose an option: 2

Manage Bookings
1. View all bookings
2. Review pending bookings
3. Back
Choose an option: 1
No bookings found.

Admin Menu
1. Manage cars
2. Manage bookings
3. Manage users
4. Logout
Choose an option: 3

Manage Users
1. View all users
2. Add a user
3. Update a user
4. Delete a user
5. Back
Choose an option: 1
[1] admin | email=admin@gmail.com | phone=0211234567 | role=admin
```

**Status**  
Passed

## Test Case 2: Invalid User Update Input

**Objective**  
Check that invalid user ID input is handled safely in the admin update user workflow.

**Steps**
1. Stay logged in as admin.
2. Open `Manage Users`.
3. Choose `Update a user`.
4. Enter a non-numeric user ID.

**Expected Result**
- The system should not crash.
- The system should return to the admin workflow after handling the invalid input.

**Actual Result**
```text
Admin Menu
1. Manage cars
2. Manage bookings
3. Manage users
4. Logout
Choose an option: 3

Manage Users
1. View all users
2. Add a user
3. Update a user
4. Delete a user
5. Back
Choose an option: 3

Update User
User ID: b

Admin Menu
1. Manage cars
2. Manage bookings
3. Manage users
4. Logout
Choose an option: 4
Logged out.
```

**Status**  
Passed

## Test Case 3: Customer Registration and Login

**Objective**  
Check that a guest can register a new customer and log in successfully.

**Steps**
1. Return to the guest menu.
2. Choose `Register customer`.
3. Enter a new username, email, phone number, and password.
4. Choose `Login`.
5. Log in with the new account.

**Expected Result**
- A new customer account is created successfully.
- The customer can log in and access the customer menu.

**Actual Result**
```text
Guest Menu
1. Register customer
2. Login
3. Exit
Choose an option: 2

Login
Username: b

Guest Menu
1. Register customer
2. Login
3. Exit
Choose an option:
Invalid choice.

Guest Menu
1. Register customer
2. Login
3. Exit
Choose an option: 1

Customer Registration
Username: alex
Email: alex@gmail.com
Phone: 02033445566
Password:
Customer account created successfully.

Guest Menu
1. Register customer
2. Login
3. Exit
Choose an option: 2

Login
Username: alex
Password:
Welcome, alex (customer).
```

**Status**  
Passed

## Test Case 4: View Available Cars as Customer

**Objective**  
Check that a logged-in customer can see all currently available cars.

**Steps**
1. Log in as customer `alex`.
2. Choose `View available cars`.

**Expected Result**
- The available fleet is displayed to the customer.

**Actual Result**
```text
Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 1
[1] 2021 Suzuki Swift | mileage 36000 | rate $58.00/day | rent 1-5 days | available yes
[2] 2023 Toyota Corolla Hybrid | mileage 18000 | rate $76.00/day | rent 1-12 days | available yes
[3] 2024 Mazda 3 | mileage 12000 | rate $88.00/day | rent 1-10 days | available yes
[4] 2022 Mitsubishi Outlander | mileage 27000 | rate $102.00/day | rent 2-18 days | available yes
[5] 2024 Hyundai Tucson | mileage 11000 | rate $112.00/day | rent 2-21 days | available yes
[6] 2024 Tesla Model 3 | mileage 9000 | rate $124.00/day | rent 1-7 days | available yes
[7] 2025 Skoda Superb | mileage 6000 | rate $128.00/day | rent 1-14 days | available yes
[8] 2023 Kia Carnival | mileage 15000 | rate $138.00/day | rent 2-14 days | available yes
[9] 2025 Toyota RAV4 Hybrid | mileage 7000 | rate $145.00/day | rent 3-28 days | available yes
[10] 2025 Mercedes-Benz C200 | mileage 5000 | rate $165.00/day | rent 1-14 days | available yes
```

**Status**  
Passed

## Test Case 5: Standard Booking Creation

**Objective**  
Check that a customer can create a standard booking and receive the correct quote.

**Steps**
1. Choose `Create booking`.
2. Select car ID `3`.
3. Enter rental dates `2026-05-10` to `2026-05-15`.
4. Choose pickup location `Auckland CBD`.
5. Add insurance.

**Expected Result**
- The booking is created successfully.
- A price breakdown is displayed.
- The booking status is saved as `pending`.

**Actual Result**
```text
Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 2
[1] 2021 Suzuki Swift | mileage 36000 | rate $58.00/day | rent 1-5 days | available yes
[2] 2023 Toyota Corolla Hybrid | mileage 18000 | rate $76.00/day | rent 1-12 days | available yes
[3] 2024 Mazda 3 | mileage 12000 | rate $88.00/day | rent 1-10 days | available yes
[4] 2022 Mitsubishi Outlander | mileage 27000 | rate $102.00/day | rent 2-18 days | available yes
[5] 2024 Hyundai Tucson | mileage 11000 | rate $112.00/day | rent 2-21 days | available yes
[6] 2024 Tesla Model 3 | mileage 9000 | rate $124.00/day | rent 1-7 days | available yes
[7] 2025 Skoda Superb | mileage 6000 | rate $128.00/day | rent 1-14 days | available yes
[8] 2023 Kia Carnival | mileage 15000 | rate $138.00/day | rent 2-14 days | available yes
[9] 2025 Toyota RAV4 Hybrid | mileage 7000 | rate $145.00/day | rent 3-28 days | available yes
[10] 2025 Mercedes-Benz C200 | mileage 5000 | rate $165.00/day | rent 1-14 days | available yes
Car ID: 3
Start date (YYYY-MM-DD): 2026-05-10
End date (YYYY-MM-DD): 2026-05-15
Pickup locations
1. Auckland CBD
2. Auckland Airport
3. North Shore
Choose pickup location: 1
Add insurance? (y/n): y
Booking #1 created. Days: 6, base $528.00, insurance $120.00, total $648.00.
```

**Status**  
Passed

## Test Case 6: Smart Booking Assistant Invalid Recommended Car Selection

**Objective**  
Check that the Smart Booking Assistant rejects a car ID that is not in the recommended list.

**Steps**
1. Open `Smart booking`.
2. Select:
   - trip type: `Family outing`
   - passengers: `3-5 people`
   - priority: `Lower mileage`
3. Enter an invalid car ID outside the recommendation list.

**Expected Result**
- The system displays the recommended cars.
- The system rejects the invalid car ID.

**Actual Result**
```text
Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 3

Smart Booking Assistant
Answer a few quick questions and the system will suggest suitable cars.

1. What type of trip is this?
1. City travel
2. Family outing
3. Business travel
4. Long-distance trip
Choose the best match: 2

2. How many people are travelling?
1. 1-2 people
2. 3-5 people
Choose the best match: 2

3. What matters most to you?
1. Lower price
2. Newer car
3. Lower mileage
4. Longer rental flexibility
Choose one priority: 3

Recommended cars for your trip
[9] 2025 Toyota RAV4 Hybrid | mileage 7000 | rate $145.00/day | rent 3-28 days | available yes
[5] 2024 Hyundai Tucson | mileage 11000 | rate $112.00/day | rent 2-21 days | available yes
[8] 2023 Kia Carnival | mileage 15000 | rate $138.00/day | rent 2-14 days | available yes
Choose one of the recommended Car IDs: 1
Please choose a car ID from the recommended list.
```

**Status**  
Passed

## Test Case 7: Smart Booking Assistant Invalid Priority Input

**Objective**  
Check that the Smart Booking Assistant validates the priority input.

**Steps**
1. Open `Smart booking`.
2. Select:
   - trip type: `Family outing`
   - passengers: `3-5 people`
3. Leave the priority field blank.

**Expected Result**
- The system rejects the invalid priority input.

**Actual Result**
```text
Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 3

Smart Booking Assistant
Answer a few quick questions and the system will suggest suitable cars.

1. What type of trip is this?
1. City travel
2. Family outing
3. Business travel
4. Long-distance trip
Choose the best match: 2

2. How many people are travelling?
1. 1-2 people
2. 3-5 people
Choose the best match: 2

3. What matters most to you?
1. Lower price
2. Newer car
3. Lower mileage
4. Longer rental flexibility
Choose one priority:
Invalid priority.
```

**Status**  
Passed

## Test Case 8: Smart Booking Assistant Recommendation and Booking

**Objective**  
Check that the Smart Booking Assistant recommends suitable cars and can be used to complete a booking.

**Steps**
1. Open `Smart booking`.
2. Select:
   - trip type: `Family outing`
   - passengers: `3-5 people`
   - priority: `Lower mileage`
3. Review the recommended cars.
4. Choose recommended car ID `8`.
5. Enter rental dates `2025-05-01` to `2025-05-10`.
6. Choose pickup location `Auckland Airport`.
7. Add insurance.

**Expected Result**
- The system recommends suitable cars.
- The selected recommended car can be booked successfully.
- The booking is created as `pending`.

**Actual Result**
```text
Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 3

Smart Booking Assistant
Answer a few quick questions and the system will suggest suitable cars.

1. What type of trip is this?
1. City travel
2. Family outing
3. Business travel
4. Long-distance trip
Choose the best match: 2

2. How many people are travelling?
1. 1-2 people
2. 3-5 people
Choose the best match: 2

3. What matters most to you?
1. Lower price
2. Newer car
3. Lower mileage
4. Longer rental flexibility
Choose one priority: 3

Recommended cars for your trip
[5] 2024 Hyundai Tucson | mileage 11000 | rate $112.00/day | rent 2-21 days | available yes
[8] 2023 Kia Carnival | mileage 15000 | rate $138.00/day | rent 2-14 days | available yes
[10] 2025 Mercedes-Benz C200 | mileage 5000 | rate $165.00/day | rent 1-14 days | available yes
Choose one of the recommended Car IDs: 8
Start date (YYYY-MM-DD): 2025-05-01
End date (YYYY-MM-DD): 2025-05-10
Pickup locations
1. Auckland CBD
2. Auckland Airport
3. North Shore
Choose pickup location: 2
Add insurance? (y/n): y
Booking #5 created. Days: 10, base $1380.00, insurance $200.00, total $1580.00.
```

**Status**  
Passed

## Test Case 9: View Customer Bookings

**Objective**  
Check that the customer can view all current personal bookings after standard and smart bookings are created.

**Steps**
1. Choose `View my bookings`.

**Expected Result**
- The customer sees both pending bookings.

**Actual Result**
```text
Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 4
[1] 2024 Mazda 3 | 2026-05-10 to 2026-05-15 | Auckland CBD | total=$648.00 | status=pending
[2] 2025 Toyota RAV4 Hybrid | 2026-05-10 to 2026-05-20 | Auckland CBD | total=$1815.00 | status=pending
```

**Status**  
Passed

## Test Case 10: Rental Policy Validation in Smart Booking

**Objective**  
Check that the system blocks a Smart Booking request when the rental period is outside the selected car policy.

**Steps**
1. Open `Smart booking`.
2. Select:
   - trip type: `City travel`
   - passengers: `1-2 people`
   - priority: `Lower price`
3. Choose recommended car ID `1`.
4. Enter dates `2026-05-05` to `2026-05-10`.
5. Choose pickup location `North Shore`.
6. Do not add insurance.

**Expected Result**
- The system rejects the booking with a rental policy validation message.

**Actual Result**
```text
Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 3

Smart Booking Assistant
Answer a few quick questions and the system will suggest suitable cars.

1. What type of trip is this?
1. City travel
2. Family outing
3. Business travel
4. Long-distance trip
Choose the best match: 1

2. How many people are travelling?
1. 1-2 people
2. 3-5 people
Choose the best match: 1

3. What matters most to you?
1. Lower price
2. Newer car
3. Lower mileage
4. Longer rental flexibility
Choose one priority: 1

Recommended cars for your trip
[1] 2021 Suzuki Swift | mileage 36000 | rate $58.00/day | rent 1-5 days | available yes
[2] 2023 Toyota Corolla Hybrid | mileage 18000 | rate $76.00/day | rent 1-12 days | available yes
[3] 2024 Mazda 3 | mileage 12000 | rate $88.00/day | rent 1-10 days | available yes
Choose one of the recommended Car IDs: 1
Start date (YYYY-MM-DD): 2026-05-05
End date (YYYY-MM-DD): 2026-05-10
Pickup locations
1. Auckland CBD
2. Auckland Airport
3. North Shore
Choose pickup location: 3
Add insurance? (y/n): n
Rental period is outside the car policy.
```

**Status**  
Passed

## Test Case 11: Smart Booking with Valid Low-Cost Option

**Objective**  
Check that a valid low-cost Smart Booking can be completed after correcting the rental period.

**Steps**
1. Open `Smart booking` again.
2. Use the same city, passenger, and priority answers as in Test Case 10.
3. Choose recommended car ID `1`.
4. Enter valid dates `2026-05-05` to `2026-05-09`.
5. Choose pickup location `Auckland CBD`.
6. Do not add insurance.

**Expected Result**
- The booking is created successfully.
- The quote reflects the lower-price option and no insurance.

**Actual Result**
```text
Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 3

Smart Booking Assistant
Answer a few quick questions and the system will suggest suitable cars.

1. What type of trip is this?
1. City travel
2. Family outing
3. Business travel
4. Long-distance trip
Choose the best match: 1

2. How many people are travelling?
1. 1-2 people
2. 3-5 people
Choose the best match: 1

3. What matters most to you?
1. Lower price
2. Newer car
3. Lower mileage
4. Longer rental flexibility
Choose one priority: 1

Recommended cars for your trip
[1] 2021 Suzuki Swift | mileage 36000 | rate $58.00/day | rent 1-5 days | available yes
[2] 2023 Toyota Corolla Hybrid | mileage 18000 | rate $76.00/day | rent 1-12 days | available yes
[3] 2024 Mazda 3 | mileage 12000 | rate $88.00/day | rent 1-10 days | available yes
Choose one of the recommended Car IDs: 1
Start date (YYYY-MM-DD): 2026-05-05
End date (YYYY-MM-DD): 2026-05-09
Pickup locations
1. Auckland CBD
2. Auckland Airport
3. North Shore
Choose pickup location: 1
Add insurance? (y/n): n
Booking #3 created. Days: 5, base $290.00, insurance $0.00, total $290.00.
```

**Status**  
Passed

## Test Case 12: View Updated Customer Bookings

**Objective**  
Check that the customer booking list updates after the third booking is created.

**Steps**
1. Choose `View my bookings` again.

**Expected Result**
- All current pending bookings are displayed.

**Actual Result**
```text
Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 4
[1] 2024 Mazda 3 | 2026-05-10 to 2026-05-15 | Auckland CBD | total=$648.00 | status=pending
[2] 2025 Toyota RAV4 Hybrid | 2026-05-10 to 2026-05-20 | Auckland CBD | total=$1815.00 | status=pending
[3] 2021 Suzuki Swift | 2026-05-05 to 2026-05-09 | Auckland CBD | total=$290.00 | status=pending
```

**Status**  
Passed

## Test Case 13: Customer Booking Cancellation

**Objective**  
Check that a customer can cancel a pending booking and that the booking list updates correctly.

**Steps**
1. Choose `Cancel booking`.
2. Cancel booking ID `1`.
3. Open `View my bookings` again.

**Expected Result**
- The selected booking is cancelled successfully.
- The cancelled booking is no longer shown in the customer's active booking list.

**Actual Result**
```text
Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 6
Booking ID to cancel: 1
Booking cancelled successfully.

Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 4
[2] 2025 Toyota RAV4 Hybrid | 2026-05-10 to 2026-05-20 | Auckland CBD | total=$1815.00 | status=pending
[3] 2021 Suzuki Swift | 2026-05-05 to 2026-05-09 | Auckland CBD | total=$290.00 | status=pending
```

**Status**  
Passed

## Test Case 14: Admin User Management

**Objective**  
Check that the admin can view existing users and add a new customer account.

**Steps**
1. Log in as admin.
2. Open `Manage Users`.
3. View all users.
4. Add a new user with role `customer`.
5. View all users again.

**Expected Result**
- Existing users are displayed correctly.
- A new user can be created successfully.
- The new user appears in the user list.

**Actual Result**
```text
Guest Menu
1. Register customer
2. Login
3. Exit
Choose an option: 2

Login
Username: admin
Password:
Welcome, admin (admin).

Admin Menu
1. Manage cars
2. Manage bookings
3. Manage users
4. Logout
Choose an option: 3

Manage Users
1. View all users
2. Add a user
3. Update a user
4. Delete a user
5. Back
Choose an option: 1
[1] admin | email=admin@gmail.com | phone=0211234567 | role=admin
[2] alex | email=alex@gmail.com | phone=02033445566 | role=customer

Admin Menu
1. Manage cars
2. Manage bookings
3. Manage users
4. Logout
Choose an option: 3

Manage Users
1. View all users
2. Add a user
3. Update a user
4. Delete a user
5. Back
Choose an option: 2

Add User
Username: cris
Email: cris@gmail.com
Phone: 20766554433
Role (admin/customer): customer
Password:
User added successfully.

Admin Menu
1. Manage cars
2. Manage bookings
3. Manage users
4. Logout
Choose an option: 3

Manage Users
1. View all users
2. Add a user
3. Update a user
4. Delete a user
5. Back
Choose an option: 1
[1] admin | email=admin@gmail.com | phone=0211234567 | role=admin
[2] alex | email=alex@gmail.com | phone=02033445566 | role=customer
[3] cris | email=cris@gmail.com | phone=20766554433 | role=customer
```

**Status**  
Passed

## Test Case 15: Admin Booking Review

**Objective**  
Check that the admin can reject one pending booking and approve another pending booking.

**Steps**
1. Open `Manage Bookings`.
2. View all bookings.
3. Review booking `#2` and reject it.
4. Review booking `#3` and approve it.
5. View all bookings again.

**Expected Result**
- The admin can review pending bookings.
- One booking is updated to `rejected`.
- One booking is updated to `approved`.

**Actual Result**
```text
Admin Menu
1. Manage cars
2. Manage bookings
3. Manage users
4. Logout
Choose an option: 2

Manage Bookings
1. View all bookings
2. Review pending bookings
3. Back
Choose an option: 1
[2] 2025 Toyota RAV4 Hybrid | 2026-05-10 to 2026-05-20 | Auckland CBD | total=$1815.00 | status=pending
[3] 2021 Suzuki Swift | 2026-05-05 to 2026-05-09 | Auckland CBD | total=$290.00 | status=pending

Admin Menu
1. Manage cars
2. Manage bookings
3. Manage users
4. Logout
Choose an option: 2

Manage Bookings
1. View all bookings
2. Review pending bookings
3. Back
Choose an option: 2
[2] 2025 Toyota RAV4 Hybrid | 2026-05-10 to 2026-05-20 | Auckland CBD | total=$1815.00 | status=pending
[3] 2021 Suzuki Swift | 2026-05-05 to 2026-05-09 | Auckland CBD | total=$290.00 | status=pending
Booking ID to review: 2
Approve booking? (y/n): n
Booking #2 is now rejected.

Admin Menu
1. Manage cars
2. Manage bookings
3. Manage users
4. Logout
Choose an option: 2

Manage Bookings
1. View all bookings
2. Review pending bookings
3. Back
Choose an option: 1
[2] 2025 Toyota RAV4 Hybrid | 2026-05-10 to 2026-05-20 | Auckland CBD | total=$1815.00 | status=rejected
[3] 2021 Suzuki Swift | 2026-05-05 to 2026-05-09 | Auckland CBD | total=$290.00 | status=pending

Admin Menu
1. Manage cars
2. Manage bookings
3. Manage users
4. Logout
Choose an option: 2

Manage Bookings
1. View all bookings
2. Review pending bookings
3. Back
Choose an option: 2
[3] 2021 Suzuki Swift | 2026-05-05 to 2026-05-09 | Auckland CBD | total=$290.00 | status=pending
Booking ID to review: 3
Approve booking? (y/n): y
Booking #3 is now approved.

Admin Menu
1. Manage cars
2. Manage bookings
3. Manage users
4. Logout
Choose an option: 2

Manage Bookings
1. View all bookings
2. Review pending bookings
3. Back
Choose an option: 1
[2] 2025 Toyota RAV4 Hybrid | 2026-05-10 to 2026-05-20 | Auckland CBD | total=$1815.00 | status=rejected
[3] 2021 Suzuki Swift | 2026-05-05 to 2026-05-09 | Auckland CBD | total=$290.00 | status=approved
```

**Status**  
Passed

## Test Case 16: New Customer with No Bookings

**Objective**  
Check that a newly added customer with no bookings sees the correct empty result.

**Steps**
1. Log in as customer `cris`.
2. Choose `View my bookings`.

**Expected Result**
- The system reports that the customer has no bookings.

**Actual Result**
```text
Admin Menu
1. Manage cars
2. Manage bookings
3. Manage users
4. Logout
Choose an option: 4
Logged out.

Guest Menu
1. Register customer
2. Login
3. Exit
Choose an option: 2

Login
Username: cris
Password:
Welcome, cris (customer).

Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 4
You have no bookings.
```

**Status**  
Passed

## Test Case 17: Final Customer View After Admin Review

**Objective**  
Check that the original customer sees the final booking results and updated car availability after admin review.

**Steps**
1. Log out as `cris`.
2. Log in again as customer `alex`.
3. View available cars.
4. View my bookings.

**Expected Result**
- The available car list reflects the approved booking.
- The booking list shows the final `rejected` and `approved` results.

**Actual Result**
```text
Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 7
Logged out.

Guest Menu
1. Register customer
2. Login
3. Exit
Choose an option: 2

Login
Username: alex
Password:
Welcome, alex (customer).

Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 1
[2] 2023 Toyota Corolla Hybrid | mileage 18000 | rate $76.00/day | rent 1-12 days | available yes
[3] 2024 Mazda 3 | mileage 12000 | rate $88.00/day | rent 1-10 days | available yes
[4] 2022 Mitsubishi Outlander | mileage 27000 | rate $102.00/day | rent 2-18 days | available yes
[5] 2024 Hyundai Tucson | mileage 11000 | rate $112.00/day | rent 2-21 days | available yes
[6] 2024 Tesla Model 3 | mileage 9000 | rate $124.00/day | rent 1-7 days | available yes
[7] 2025 Skoda Superb | mileage 6000 | rate $128.00/day | rent 1-14 days | available yes
[8] 2023 Kia Carnival | mileage 15000 | rate $138.00/day | rent 2-14 days | available yes
[9] 2025 Toyota RAV4 Hybrid | mileage 7000 | rate $145.00/day | rent 3-28 days | available yes
[10] 2025 Mercedes-Benz C200 | mileage 5000 | rate $165.00/day | rent 1-14 days | available yes

Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 4
[2] 2025 Toyota RAV4 Hybrid | 2026-05-10 to 2026-05-20 | Auckland CBD | total=$1815.00 | status=rejected
[3] 2021 Suzuki Swift | 2026-05-05 to 2026-05-09 | Auckland CBD | total=$290.00 | status=approved

Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 4
[2] 2025 Toyota RAV4 Hybrid | 2026-05-10 to 2026-05-20 | Auckland CBD | total=$1815.00 | status=rejected
[3] 2021 Suzuki Swift | 2026-05-05 to 2026-05-09 | Auckland CBD | total=$290.00 | status=approved
```

**Status**  
Passed

## Test Case 18: Payment Blocked Before Approval

**Objective**  
Check that the customer cannot pay when there is no approved booking available for payment.

**Steps**
1. Log in as customer `alex`.
2. Open `View my bookings`.
3. Open `Pay for booking`.
4. Confirm that no payable booking is shown.
5. Create a new smart booking.
6. Open `Pay for booking` again before admin review.

**Expected Result**
- Rejected and already paid bookings are shown only in `View my bookings`.
- The payment menu does not allow payment before admin approval.
- The system displays `You have no approved bookings waiting for payment.`

**Actual Result**
```text
Guest Menu
1. Register customer
2. Login
3. Exit
Choose an option: 2

Login
Username: alex
Password:
Welcome, alex (customer).

Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 4
[2] 2021 Suzuki Swift | 2026-05-05 to 2026-05-09 | Auckland CBD | total=$290.00 | status=rejected
[3] 2025 Toyota RAV4 Hybrid | 2026-05-01 to 2026-05-25 | Auckland Airport | total=$4125.00 | status=paid

Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 5
You have no approved bookings waiting for payment.

Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 3

Smart Booking Assistant
Answer a few quick questions and the system will suggest suitable cars.

1. What type of trip is this?
1. City travel
2. Family outing
3. Business travel
4. Long-distance trip
Choose the best match: 2

2. How many people are travelling?
1. 1-2 people
2. 3-5 people
Choose the best match: 2

3. What matters most to you?
1. Lower price
2. Newer car
3. Lower mileage
4. Longer rental flexibility
Choose one priority: 3

Recommended cars for your trip
[5] 2024 Hyundai Tucson | mileage 11000 | rate $112.00/day | rent 2-21 days | available yes
[8] 2023 Kia Carnival | mileage 15000 | rate $138.00/day | rent 2-14 days | available yes
[4] 2022 Mitsubishi Outlander | mileage 27000 | rate $102.00/day | rent 2-18 days | available yes
Choose one of the recommended Car IDs: 4
Start date (YYYY-MM-DD): 2026-05-01
End date (YYYY-MM-DD): 2026-05-14
Pickup locations
1. Auckland CBD
2. Auckland Airport
3. North Shore
Choose pickup location: 1
Add insurance? (y/n): y
Booking #4 created. Days: 14, base $1428.00, insurance $280.00, total $1708.00.

Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 5
You have no approved bookings waiting for payment.
```

**Status**  
Passed

## Test Case 19: Approved Booking Payment

**Objective**  
Check that a customer can pay for a booking only after it has been approved by the admin.

**Steps**
1. Log in as customer `alex`.
2. Open `View my bookings`.
3. Open `Pay for booking`.
4. Confirm that only approved bookings are shown.
5. Enter booking ID `4`.

**Expected Result**
- Rejected and paid bookings are not shown in the payment list.
- Approved bookings are listed as payable.
- The selected booking is updated from `approved` to `paid`.

**Actual Result**
```text
Guest Menu
1. Register customer
2. Login
3. Exit
Choose an option: 2

Login
Username: alex
Password:
Welcome, alex (customer).

Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 4
[2] 2021 Suzuki Swift | 2026-05-05 to 2026-05-09 | Auckland CBD | total=$290.00 | status=rejected
[3] 2025 Toyota RAV4 Hybrid | 2026-05-01 to 2026-05-25 | Auckland Airport | total=$4125.00 | status=paid
[4] 2022 Mitsubishi Outlander | 2026-05-01 to 2026-05-14 | Auckland CBD | total=$1708.00 | status=approved

Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 5
[4] 2022 Mitsubishi Outlander | 2026-05-01 to 2026-05-14 | Auckland CBD | total=$1708.00 | status=approved
Booking ID to pay: 4
Booking #4 paid successfully.
```

**Status**  
Passed

## Test Case 20: Final Customer View After Payment

**Objective**  
Check that the paid booking is shown correctly in the customer booking list and that unavailable cars are no longer displayed in the available fleet.

**Steps**
1. Stay logged in as `alex`.
2. Open `View my bookings`.
3. Open `View available cars`.

**Expected Result**
- The booking paid in Test Case 19 is displayed with status `paid`.
- The paid and approved booking's car is no longer shown in the available car list.

**Actual Result**
```text
Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 4
[2] 2021 Suzuki Swift | 2026-05-05 to 2026-05-09 | Auckland CBD | total=$290.00 | status=rejected
[3] 2025 Toyota RAV4 Hybrid | 2026-05-01 to 2026-05-25 | Auckland Airport | total=$4125.00 | status=paid
[4] 2022 Mitsubishi Outlander | 2026-05-01 to 2026-05-14 | Auckland CBD | total=$1708.00 | status=paid

Customer Menu
1. View available cars
2. Create booking
3. Smart booking
4. View my bookings
5. Pay for booking
6. Cancel booking
7. Logout
Choose an option: 1
[1] 2021 Suzuki Swift | mileage 36000 | rate $58.00/day | rent 1-5 days | available yes
[2] 2023 Toyota Corolla Hybrid | mileage 18000 | rate $76.00/day | rent 1-12 days | available yes
[3] 2024 Mazda 3 | mileage 12000 | rate $88.00/day | rent 1-10 days | available yes
[5] 2024 Hyundai Tucson | mileage 11000 | rate $112.00/day | rent 2-21 days | available yes
[6] 2024 Tesla Model 3 | mileage 9000 | rate $124.00/day | rent 1-7 days | available yes
[7] 2025 Skoda Superb | mileage 6000 | rate $128.00/day | rent 1-14 days | available yes
[8] 2023 Kia Carnival | mileage 15000 | rate $138.00/day | rent 2-14 days | available yes
[10] 2025 Mercedes-Benz C200 | mileage 5000 | rate $165.00/day | rent 1-14 days | available yes
```

**Status**  
Passed

## Summary

The manual test results show that the main workflow of the system worked correctly during the CLI test session:

- guest registration and login worked
- customer booking creation worked
- the Smart Booking Assistant produced visible recommendations and supported booking creation
- invalid inputs were handled with error messages
- booking cancellation worked
- admin user management worked
- admin booking review changed booking status correctly
- payment was correctly blocked before admin approval
- approved bookings could be paid successfully by the customer
- final customer results reflected rejected and paid bookings

This document can be reused later as the testing chapter in the full user document.
