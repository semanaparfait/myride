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
