import random

# Sample data storage
users = {"riders": {}, "drivers": {}}
rides = []

# Register a user
def register_user(user_type):
    print(f"Registering a {user_type.capitalize()}")
    username = input("Enter username: ")
    if username in users[user_type]:
        print("Username already exists. Try logging in.")
        return
    password = input("Enter password: ")
    users[user_type][username] = password
    print(f"{user_type.capitalize()} registered successfully!")

# Login a user
def login_user(user_type):
    print(f"Logging in as a {user_type.capitalize()}")
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username in users[user_type] and users[user_type][username] == password:
        print(f"Welcome, {username}!")
        return username
    print("Invalid credentials.")
    return None

# Request a ride
def request_ride(rider):
    pickup = input("Enter pickup location: ")
    dropoff = input("Enter drop-off location: ")
    ride_id = len(rides) + 1
    rides.append({"rider": rider, "pickup": pickup, "dropoff": dropoff, "status": "Pending"})
    print(f"Ride request created with ID: {ride_id}")
    return ride_id

# Find a driver
def find_driver():
    driver_list = list(users["drivers"].keys())
    if not driver_list:
        print("No drivers available right now.")
        return None
    driver = random.choice(driver_list)
    print(f"Driver {driver} matched!")
    return driver

# Main menu
def main():
    print("Welcome to RideShare!")
    while True:
        print("\nMenu:")
        print("1. Register as Rider")
        print("2. Register as Driver")
        print("3. Login as Rider")
        print("4. Login as Driver")
        print("5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            register_user("riders")
        elif choice == "2":
            register_user("drivers")
        elif choice == "3":
            rider = login_user("riders")
            if rider:
                ride_id = request_ride(rider)
                driver = find_driver()
                if driver:
                    rides[ride_id - 1]["status"] = "Matched"
                    rides[ride_id - 1]["driver"] = driver
                    print(f"Ride confirmed! Driver {driver} will pick you up from {rides[ride_id - 1]['pickup']} and take you to {rides[ride_id - 1]['dropoff']}.")
        elif choice == "4":
            driver = login_user("drivers")
            if driver:
                print(f"Welcome, Driver {driver}!")
        elif choice == "5":
            print("Thank you for using RideShare!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()

