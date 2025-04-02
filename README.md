# My Ride - App

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Technologies Used](#technologies-used)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

MyRide is a ride-matching system designed to connect passengers with available drivers. The system provides functionalities for drivers to register, add trips, and for passengers to book rides based on available routes. An admin panel allows drivers and passengers to be monitored.

## Features

- Driver registration and login
- Adding and updating trip details
- Passenger registration and ride booking
- Automated ride cost calculation based on distance
- Admin dashboard to view drivers and passengers

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- MySQL Server
- Required Python libraries (see `MYSQL Client`)

### Steps to Install

1. Clone this repository:
   ```sh
   git clone https://github.com/semanaparfait/myride.git
   cd myride
   ```
2. Install required dependencies:
   ```sh
   pip install mysqlclient
   pip install geopy
   ```
3. Configure the database connection in `my_conn` dictionary within the script.

## Database Setup

1. Create a MySQL database named `myride`.
2. Run the following SQL script to set up the required tables:
   ```sql
   CREATE TABLE driver (
       DriverID INT PRIMARY KEY AUTO_INCREMENT,
       DriverName VARCHAR(255),
       DriverPhoneNumber VARCHAR(10),
       DriverPassword VARCHAR(255),
       AvailableSeats INT,
       CurrentLocation VARCHAR(255),
       Destination VARCHAR(255)
   );

   CREATE TABLE Passenger (
       PassengerID INT PRIMARY KEY AUTO_INCREMENT,
       PassengerName VARCHAR(255),
       PassengerPhoneNumber VARCHAR(10),
       PickupLocation VARCHAR(255),
       Destination VARCHAR(255)
   );
   ```
3. Verify the database connection using `connect_db()`.

## Usage

Run the application:

```sh
python myride.py
```

### Main Menu Options

1. **Continue as Driver**: Register/Login as a driver and add a trip.
2. **Continue as Passenger**: Register and book a ride.
3. **Find a Ride**: View available drivers and request a ride.
4. **Admin Login**: Access the admin panel (use the keyword `myride`).
5. **Exit**: Close the application.

## Code Structure

- **`connect_db()`**: Establishes a database connection.
- **Driver Functions**:
  - `add_driver()`: Register/Login a driver.
  - `add_trip_asdriver()`: Adds a new trip.
  - `driver_login()`: Authenticates a driver.
- **Passenger Functions**:
  - `add_passenger()`: Registers a passenger and books a ride.
  - `match_driver_to_passenger()`: Matches passengers with available drivers.
  - `calculate_ride_cost()`: Computes the trip cost based on distance.
- **Admin Functions**:
  - `admin_login()`: Grants admin access.
  - `admin_dashboard()`: Displays drivers and passengers.
- **Utility Functions**:
  - Uses `geopy` for location lookup and distance calculation.

## Technologies Used

- **Programming Language**: Python
- **Database**: MySQL
- **Libraries**: `MySQLdb`, `geopy`, `math`, `datetime`

## Troubleshooting

- If the database connection fails, check credentials in `my_conn`.
- Ensure MySQL service is running.
- If geolocation lookup fails, check the internet connection.

## Contributing

Feel free to contribute by forking the repository and submitting pull requests.

## License

This project is licensed under the MyRide License.


