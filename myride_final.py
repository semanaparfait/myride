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
    


# Passenger registration
def add_passenger():
    global passenger_name,passenger_phone
    connection = connect_db()
    print("\n Passenger options:")
    print("1. Register as passenger")
    print("2. Book a trip")
    print("3. Available Drivers")
    print("4. Go back")
    passenger_choice=input("Enter your choice: ")
    if passenger_choice.lower() == "1":
        if connection:
            passenger_choice_yes_no = input("Do you really want to register as a passenger? (yes/no): ")
            if passenger_choice_yes_no.lower() == "no":
                return
            elif passenger_choice_yes_no.lower() == "yes":
                print("\nEnter your details to register")
                passenger_name = input("\nEnter your name: ")
                while True:
                    passenger_phone = input("Enter your phone number: ")
                    if len(passenger_phone) == 10 and passenger_phone.isdigit():
                        break
                    print("invalid phone number ❌ (must be exactly 10 digits)")
                calculate_ride_cost()
                try:
                    cursor = connection.cursor()
                    insert_query = """
                    INSERT INTO Passenger (PassengerName, PassengerPhoneNumber,PickupLocation ,Destination)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (passenger_name, passenger_phone, current_location, destination ))
                    connection.commit()
                    print(f"Passenger {passenger_name} registered successfully!")
                except Error as e:
                    print(f"Error: {e}")
                finally:
                    cursor.close()
                    connection.close()
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")
                return
    if passenger_choice.lower() == "2":
        while True:
            trip_choice_yes_no=input("\n Do you really need to book a trip with MY RIDE? (yes/no): ")
            if trip_choice_yes_no.lower() == "no":
                return
            elif trip_choice_yes_no.lower() == "yes":
                booking_trip_as_team()
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'. if you want to book a trip with MY RIDE")
    if passenger_choice.lower() == "3":
        passenger_view_driver = input("\n In which Destination you want to go: ")
        query = """
           SELECT Destination FROM driver Where Destination = %s
           """
        # print(query)

        # pickup_location = input("Enter your pickup location: ")
        # destination = input("Enter your destination: ")
        
        

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
                        print(f"Driver Name: {driver[1]}, Phone: {driver[3]}, Seats Available: {driver[4]}, Location: {driver[5]}")
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

#booking trip as team on passengers
def booking_trip_as_team():
    global current_location,destination, distance_km
    connection = connect_db()
    if connection:
        team_name = input("Enter team name: ")
        while True:
            team_members = input("Enter team members: ")
            if team_members.isdigit():
                team_members = int(team_members)
                if team_members <= 8 and int(team_members) >= 2:
                    print(f"Great! {team_name} has {team_members} members. Proceeding with booking...")
                    calculate_ride_cost()
                    break
                else:
                    print(f"Sorry ,{team_name} team we can't afford {team_members} size should be less than 8 people")
            else:
                print("Invalid input. Please enter a valid number of team members.")
        # team_current_location = input("Enter team current location: ")
        # team_destination = input("Enter team destination: ")
         # Calculate cost (500 RWF per km)
        # cost_rwf = distance_km * 500
        # calculate_ride_cost(distance_km)
        # total_cost = calculate_ride_cost(distance_km) * team_members
        # print(f"Total cost for this trip: {total_cost} RWF (for {distance_km} km)")
        
        try:
            cursor = connection.cursor()
            Driv_query = """
            INSERT INTO passengerstrips(passengerTeamName, passengerteammember, TripPickupLocation, TripDestination) VALUES (%s, %s, %s, %s)
            
            """
            cursor.execute(Driv_query, ( team_name ,team_members, current_location, destination))
            connection.commit()

            cursor.execute("SELECT * FROM driver WHERE Destination = %s AND CurrentLocation = %s", (destination, current_location))

            drivers_table = cursor.fetchall()
            if drivers_table:
                print("Available drivers who can pick you:")
                for driver in drivers_table:
                    # if team_current_location == current_location and team_destination == destination :
                    print("Trip booked successfully")
                    print(f"Driver called: {driver[1]}, and has {driver[4]} seats car available in car he is on the way to {driver[5]} picking you! wait a few seconds")                       
            else:
                print(f"No Driver available in this current location.!! Please wait while we are looking For ur driver.")     
                          
                          # if team_members >= available_seats and team_current_location ==current_location and team_destination == destination :

        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Admin dashboard
def admin_dashboard():
    connection = connect_db()
    if connection:
        print("Welcome to the Admin Dashboard!")
        while True:
            print("\nMenu:")
            print("1. View Drivers")
            print("2. View Passengers")
            print("3. View Trips")
            print("4. View Payments")
            print("5. Exit")
        
            choice = input("Enter your choice: ")
            
            if choice == '1':
                view_drivers(connection)
            elif choice == '2':
                view_passengers(connection)
            elif choice == '3':
                view_passengers_trips(connection)
            elif choice == '4':
                print("Payment methos is not implemented yet becouse we are still in development phase and no APIs")
            elif choice == '5':
                print("Exiting Admin Dashboard...")
                break
            else:
                print("Invalid choice. Please try again.")
        connection.close()

def view_passengers_trips(connection):
    try:
        cursor = connection.cursor()
        querypasstrip = "SELECT * FROM passengerstrips"
        cursor.execute(querypasstrip)
        passengerstrip= cursor.fetchall()
        if passengerstrip:
            print("Passenger Details:")
            for passengerstrips in passengerstrip:
                print(f"ID: {passengerstrips[0]}, Name: {passengerstrips[1]}, Phone: {passengerstrips[2]}, Pickup Location: {passengerstrips[3]}, Destination: {passengerstrips[4]}")
        else:
            print("No passengers registered.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

def view_drivers(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM driver"
        cursor.execute(query)
        drivers = cursor.fetchall()
        if drivers:
            print("Driver Details:")
            for driver in drivers:
                print(f"ID: {driver[0]}, Name: {driver[1]}, Phone: {driver[2]}, Seats Available: {driver[4]}, Location: {driver[5]}, Destination: {driver[6]}")
        else:
            print("No drivers available.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

def view_passengers(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM Passenger"
        cursor.execute(query)
        passengers = cursor.fetchall()
        if passengers:
            print("Passenger Details:")
            for passenger in passengers:
                print(f"ID: {passenger[0]}, Name: {passenger[1]}, Phone: {passenger[2]}, Pickup Location: {passenger[3]}, Destination: {passenger[4]}")
        else:
            print("No passengers registered.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

# Admin login
def admin_login():
    connection = connect_db()
    if connection:
        print("Enter admin keyword to login:")
        while True:
            admin_keyword=input("Enter The keyword to access the admin dashboard: ").lower()
            if admin_keyword == "myride":
                admin_dashboard()
                break
            print("Invalid keyword. Please try again.")
            
                    
                
# Main menu
def main_menu():
    print("Welcome to My Ride!")
    while True:
        print("\nMenu:")
        print("1. Continue as Driver")
        print("2. Continue as Passenger")
        print("3. Find a Ride")
        print("4. Admin Login")
        print("5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_driver()
        elif choice == '2':
            add_passenger()
        elif choice == '3':
            match_driver_to_passenger()
        elif choice == '4':
            admin_login()
        elif choice == '5':
            print("Thank you for using My Ride. Goodbye!")
            print(bye_no)
            break
        else:
            print("Invalid choice. Please try again.")

# Run the application
if __name__ == "__main__":
    main_menu()
    
