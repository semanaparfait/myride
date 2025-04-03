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
    "password": "strongpassword",  # Make sure to provide the correct password
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
driver_id = None
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


# Define global variables at the top
driver_name = None
driver_id = None
driver_phone = None
available_seats = None
current_location = None
destination = None
passenger_name = None
passenger_phone = None
current_location = None
cost_rwf = None
distance_km = None



#function to add driver in database
def add_driver():
    global driver_name
    connection = connect_db()
    print("\n Driver options")
    print("1. Register as driver")
    print("2. Login as driver")
    print("3. End job")
    print("4. Exit")
    driver_choice = input("Enter your choice: ")
    if driver_choice.lower() == "1":        
        if connection:
            print("Enter your credentials to register as Driver")
            driver_name = input("Enter your name: ")  # Now properly modifies the global variable
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
                if available_seats.isdigit() and int(available_seats) <= 8 and int(available_seats) >= 3:
                    break
                print("Please that car doesn't exist in our company")
            current_location = input("Enter your current location: ")
            destination = input("Enter your destination: ")
            
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
            # finally:
            #     if connection.is_connected():
            #         cursor.close()
            #         connection.close()
    
    elif driver_choice.lower() == "2":
        driver_login(connection)
        return


# Function for drivers to add a trip
def add_trip_asdriver():
    global driver_name, driver_id, available_seats,driver_phone 
    # Connect to the database
    connection = connect_db()
    print(f"\n Add trip for new trip {driver_name}")
    trip_location = input(" Enter your current location: ")
    trip_destination = input(" Enter your destination: ")
    try:
        cursor = connection.cursor()
        update_query = """
        INSERT INTO drivertripdetails (Driverid, DriverName, DriverPhoneNumber, AvailableSeats, drivertripcurrentloc, drivertripDestination)
        SELECT Driverid, DriverName, DriverPhoneNumber, AvailableSeats, %s, %s
        FROM driver
        WHERE Driverid = %s;
        """
        cursor.execute(update_query, (trip_location, trip_destination, driver_id))
        connection.commit()  # Move commit before closing connection
        if cursor.rowcount > 0:
            print("Trip added successfully")
        else:
            print("Trip  added")
    except Error as e:
        print(f"Error: {e}")
    # finally:
    #     if connection.is_connected():
    #         cursor.close()
    #         connection.close()


# Function to login driver and fetch details
def driver_login(connection):
    global driver_name, driver_id
    connection = connect_db()
    if connection:
        print("\n Enter your credentials to login as Driver")
        login_name = input("Enter your name: ")
        driver_password = input("Enter your password: ")
        
        try:
            cursor = connection.cursor()
            select_query = """
            SELECT DriverID, DriverName FROM driver 
            WHERE DriverName = %s AND DriverPassword = %s
            """
            cursor.execute(select_query, (login_name, driver_password))
            result = cursor.fetchone()
            
            if result:
                driver_id, driver_name = result  # Properly set global variables
                print(f"Welcome back, {driver_name}!")
                add_trip_yesorno = input(f"Mr {driver_name} do you really want to add trip (yes / no): ")
                if add_trip_yesorno.lower() == "yes":
                    add_trip_asdriver()
                else:
                    print("Trip not added")
                return driver_id
            else:
                print("Invalid credentials. Please try again or register if you don't have an account.")
                return None
        except Error as e:
            print(f"Error: {e}")
            return None
        # finally:
        #     if connection.is_connected():
        #         cursor.close()
        #         connection.close()
    else:
        print("Unable to connect to database")
        return None


#passenger kilometers calculations
def calculate_ride_cost():
    global destination
    global current_location
   
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
    # return cost_rwf
    
    # Display results
    print("\n" + "=" * 50)
    print(f"OOh thanks for using our system")
    print("=" * 50)
    print(f"From: {current_loc.address}")
    print(f"To: {dest_loc.address}")
    print(f"Distance: {distance_km:.1f} kilometers")
    print(f"Cost: {cost_rwf:.0f} RWF (at 350 RWF per kilometer)")
    print("This the cost per kilometer and per person")
    print("=" * 50)
    
    return {
        "from": current_loc.address,
        "to": dest_loc.address,
        "distance_km": distance_km,
        "cost_rwf": cost_rwf
    }
    
