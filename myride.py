import MySQLdb
from MySQLdb import Error
from datetime import datetime
import math
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

my_conn = {
    "host": "95a84b26e59f.c66578f8.alu-cod.online",
    "user": "admin",
    "port": 36488,
    "password": "strongpassword",  # Make sure to provide the correct password
    "database": "myride"
}


logo = ''' 


███╗░░░███╗██╗░░░██╗  ██████╗░██╗██████╗░███████╗
████╗░████║╚██╗░██╔╝  ██╔══██╗██║██╔══██╗██╔════╝
██╔████╔██║░╚████╔╝░  ██████╔╝██║██║░░██║█████╗░░
██║╚██╔╝██║░░╚██╔╝░░  ██╔══██╗██║██║░░██║██╔══╝░░
██║░╚═╝░██║░░░██║░░░  ██║░░██║██║██████╔╝███████╗
╚═╝░░░░░╚═╝░░░╚═╝░░░  ╚═╝░░╚═╝╚═╝╚═════╝░╚══════╝

'''
bye_no = '''

██████╗░██╗░░░██╗███████╗███████╗██╗██╗
██╔══██╗╚██╗░██╔╝██╔════╝██╔════╝██║██║
██████╦╝░╚████╔╝░█████╗░░█████╗░░██║██║
██╔══██╗░░╚██╔╝░░██╔══╝░░██╔══╝░░╚═╝╚═╝
██████╦╝░░░██║░░░███████╗███████╗██╗██╗
╚═════╝░░░░╚═╝░░░╚══════╝╚══════╝╚═╝╚═╝
'''
print(logo)

# Connect to the database
def connect_db():
    try:
        connection = MySQLdb.connect(
            host=my_conn["host"],
            user=my_conn["user"],
            passwd=my_conn["password"],
            db=my_conn["database"],
            port=my_conn["port"]
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None
        # driver Login
def driver_login():
    driver_name = input("Enter your UserName: ")
    driver_password = input("Enter your Password: ")
    print(f"ohhhhh welcome{driver_name}! you are welcome to our system")
    
#passenger kilometers calculations
global destination
global current_location
def calculate_ride_cost():
   
    # Initialize geocoder
    geolocator = Nominatim(user_agent="myride_app")
    
    # Get current location
    current_location = input("Enter your current location: ")
    try:
        current_loc = geolocator.geocode(current_location)
        if not current_loc:
            print("Sorry, couldn't find your current location. Please try again with a more specific address.")
            return
        print(f"Found: {current_loc.address}")
        current_coords = (current_loc.latitude, current_loc.longitude)
    except Exception as e:
        print(f"Error finding location: {e}")
        return
    
    # Get destination
    destination = input("Enter your destination: ")
    try:
        dest_loc = geolocator.geocode(destination)
        if not dest_loc:
            print("Sorry, couldn't find your destination. Please try again with a more specific address.")
            return
        print(f"Found: {dest_loc.address}")
        dest_coords = (dest_loc.latitude, dest_loc.longitude)
    except Exception as e:
        print(f"Error finding destination: {e}")
        return
    
    # Calculate distance
    distance_km = geodesic(current_coords, dest_coords).kilometers
    
    # Round up to nearest 0.1 km
    distance_km = math.ceil(distance_km * 10) / 10
    
    # Calculate cost (500 RWF per km)
    cost_rwf = distance_km * 500
    
    # Display results
    print("\n" + "=" * 50)
    print(f"OOh thanks for using our system")
    print("=" * 50)
    print(f"From: {current_loc.address}")
    print(f"To: {dest_loc.address}")
    print(f"Distance: {distance_km:.1f} kilometers")
    print(f"Cost: {cost_rwf:.0f} RWF (at 350 RWF per kilometer)")
    print("=" * 50)
    
    return {
        "from": current_loc.address,
        "to": dest_loc.address,
        "distance_km": distance_km,
        "cost_rwf": cost_rwf
    }
    # Driver registration
def add_driver():
    connection = connect_db()
    driver_choice = input("Are you Registared as driver (yes/no): ")
    if driver_choice.lower() == "no":        
        if connection:
            print("Enter your credentials to register as Driver")
            driver_name = input("Enter your name: ")
            while True:
                driver_phone = input("Enter your phone number: ")
                if len(driver_phone) == 10 and driver_phone.isdigit():
                    break
                print("invalid phone number ❌ (must be exactly 10 digits)")
            while True:
                driver_password = input("Enter your password: ")
                if len(driver_password) <= 10:
                    break
                print("Password must be 10 characters ")
            while True:
                available_seats = input("Enter the number of available seats in your car: ")
                if available_seats.isdigit() and int(available_seats) <= 8:
                    break
                print("Please that car doesn't exist in our company")
            current_location = input("Enter your current location: ")
            destination = input("Enter your destination: ")
    if driver_choice.lower() == "yes":
        print("You are not registered as a driver. Please register first.")
        driver_login()


            
    try:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO driver (DriverName, DriverPhoneNumber, DriverPassword, AvailableSeats, CurrentLocation, Destination)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (driver_name, driver_phone, driver_password, available_seats, current_location, destination))
        connection.commit()
        print(f"Driver {driver_name} registered successfully!")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

# Match drivers and passengers
def match_driver_to_passenger():
    connection = connect_db()
    if connection:
        passenger_currentLocation= input("Enter your current location: ")
        passenger_destination = input("Enter your destination: ")
        try:
            cursor = connection.cursor()
            query = """
            SELECT * FROM driver WHERE Destination = %s AND AvailableSeats > 0
            """
            cursor.execute(query, (passenger_destination,))
            drivers = cursor.fetchall()
            if drivers:
                print("Available drivers:")
                for driver in drivers:
                    print(f"Driver Name: {driver[1]}, Phone: {driver[2]}, Seats Available: {driver[4]}, Location: {driver[5]}")
                    while True:
                        bookirde=input("Do you want to book a ride with this driver? (yes/no): ")
                        if bookirde.lower() == "yes":
                            add_passenger()
                            break
            else:
                print("No drivers available for your destination.")

        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Passenger registration
global passenger_name
def add_passenger():
    connection = connect_db()
    if connection:
        print("Enter your details to register")
        passenger_name = input("Enter your name: ")
        while True:
            passenger_phone = input("Enter your phone number: ")
            if len(passenger_phone) == 10 and passenger_phone.isdigit():
                break
            print("invalid phone number ❌ (must be exactly 10 digits)")
        calculate_ride_cost()
        # pickup_location = input("Enter your pickup location: ")
        # destination = input("Enter your destination: ")
        
        try:
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO Passenger (PassengerName, PassengerPhoneNumber)
            VALUES (%s, %s)
            """
            cursor.execute(insert_query, (passenger_name, passenger_phone))
            connection.commit()
            print(f"Passenger {passenger_name} registered successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

    # Match drivers and passengers
    def match_driver_to_passenger():
        connection = connect_db()
        if connection:
            passenger_currentLocation= input("Enter your current location: ")
            passenger_destination = input("Enter your destination: ")
            try:
                cursor = connection.cursor()
                query = """
                SELECT * FROM driver WHERE Destination = %s AND AvailableSeats > 0
                """
                cursor.execute(query, (passenger_destination,))
                drivers = cursor.fetchall()
                if drivers:
                    print("Available drivers:")
                    for driver in drivers:
                        print(f"Driver Name: {driver[1]}, Phone: {driver[2]}, Seats Available: {driver[4]}, Location: {driver[5]}")
                        while True:
                            bookirde=input("Do you want to book a ride with this driver? (yes/no): ")
                            if bookirde.lower() == "yes":
                                add_passenger()
                                break
                else:
                    print("No drivers available for your destination.")

            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()


# Add trip
def add_trip(driver_id, passenger_id, price):
    connection = connect_db()
    if connection:
        trip_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO Trips (DriverId, PassengerId, Price, TripDate)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (driver_id, passenger_id, price, trip_date))
            connection.commit()
            print("Trip added successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()
    

