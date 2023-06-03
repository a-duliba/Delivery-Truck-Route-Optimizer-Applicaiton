# Citing source: WGU code repository C950 - Webinar-4 - Python Modules


# Package class
class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline, weight, status):
        # Constructor method that initializes the attributes of a Package object
        self.ID = ID  # Package ID
        self.address = address  # Delivery address
        self.city = city  # City of delivery address
        self.state = state  # State of delivery address
        self.zipcode = zipcode  # ZIP code of delivery address
        self.deadline = deadline  # Deadline time for delivery
        self.weight = weight  # Weight of the package
        self.status = status  # Current status of the package
        self.departureTime = None  # Departure time of the package (initially set to None)
        self.deliveryTime = None  # Delivery time of the package (initially set to None)

    def __str__(self):
        # Method that returns a string representation of the Package object
        return f"{self.ID}, {self.address}, {self.city}, {self.state}, {self.zipcode}, {self.deadline}, {self.weight}, {self.deliveryTime}, {self.status}"

    def updateStatus(self, convertTimedelta):
        # Method to update the status of the package based on the specified time
        if self.deliveryTime < convertTimedelta:
            # If the delivery time of the package is earlier than the specified time, it is marked as "Delivered"
            self.status = "Delivered"
        elif self.departureTime > convertTimedelta:
            # If the departure time of the package is later than the specified time, it is marked as "En route"
            self.status = "En route"
        else:
            # Otherwise, the package is marked as "At Hub"
            self.status = "At Hub"
