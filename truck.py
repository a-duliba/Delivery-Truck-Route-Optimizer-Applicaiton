# Citing source: WGU code repository C950 - Webinar-4 - Python Modules


# Truck class
class Truck:
    def __init__(self, capacity, speed, load, packages, mileage, address, departureTime):
        # Constructor method that initializes the attributes of a Truck object
        self.capacity = capacity  # Maximum capacity of the truck
        self.speed = speed  # Speed of the truck
        self.load = load  # Current load of the truck
        self.packages = packages  # List of packages assigned to the truck
        self.mileage = mileage  # Total mileage traveled by the truck
        self.address = address  # Current address of the truck
        self.departureTime = departureTime  # Departure time of the truck
        self.time = departureTime  # Current time of the truck (initially set to the departure time)

    def __str__(self):
        # Method that returns a string representation of the Truck object
        return f"{self.capacity}, {self.speed}, {self.load}, {self.packages}, {self.mileage}, {self.address}, {self.departureTime}"
