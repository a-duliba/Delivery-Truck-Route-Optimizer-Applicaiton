# Author: Andrew Duliba
# Student ID: 003300689
# Title: NHP2 — NHP2 Task 1: WGUPS Routing Program
# Citing source: WGU code repository C950 - Webinar-4 - Python Modules


# Imports
import csv
import datetime
import truck
from package import Package
from hashtable import ChainingHashTable
from builtins import ValueError

# Read and assign CSV files
distance_csv = list(csv.reader(open('./csv/distance_data.csv')))
address_csv = list(csv.reader(open('./csv/address_data.csv')))
package_csv = list(csv.reader(open('./csv/package_data.csv')))

# Function to load package data from a file into the hash table
"""
    Loads package data from a file into the hash table.

    Time complexity: O(N), where N is the number of packages in the file.
    Space complexity: O(1) (excluding the space for the hash table).
    """
def loadPackageData(fileName, packageHashTable):
    # Open the package data file
    with open(fileName) as packageInfo:
        packageData = csv.reader(packageInfo)
        for package in packageData:
            # Extract package information from the file
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pStatus = "A Hub"

            # Create a package object
            p = Package(pID, pAddress, pCity, pState, pZipcode, pDeadline, pWeight, pStatus)

            # Insert the package into the hash table
            packageHashTable.insert(pID, p)

# Function to calculate distance between two addresses
"""
    Calculates the distance between two addresses.

    Time complexity: O(1)
    Space complexity: O(1)
    """
def distanceInBetween(xValue, yValue):
    distance = distance_csv[xValue][yValue]
    if distance == '':
        distance = distance_csv[yValue][xValue]
    return float(distance)


# Function to extract address number from address string
"""
    Extracts the address number from an address string.

    Time complexity: O(N), where N is the number of addresses in the CSV file.
    Space complexity: O(1)
    """
def extractAddress(address):
    for row in address_csv:
        if address in row[2]:
            return int(row[0])


# Create truck objects
truck1 = truck.Truck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 S 700 E",
                     datetime.timedelta(hours=8))
truck2 = truck.Truck(16, 18, None, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0,
                     "4001 S 700 E", datetime.timedelta(hours=10, minutes=20))
truck3 = truck.Truck(16, 18, None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, "4001 S 700 E",
                     datetime.timedelta(hours=9, minutes=5))


# Create hash table for packages
packageHashTable = ChainingHashTable()


# Load package data into hash table
loadPackageData("csv/package_data.csv", packageHashTable)


# Function to order packages on a given truck using the nearest neighbor algorithm
# This function also calculates the distance driven by the truck once the packages are sorted
"""
    Orders packages on a given truck using the nearest neighbor algorithm and calculates the distance driven.

    Time complexity: O(N^2), where N is the number of packages on the truck.
    Space complexity: O(N), where N is the number of packages on the truck.
    """
def deliveringPackages(trucks):
    # Place all packages into array of not delivered
    notDelivered = []
    for packageID in trucks.packages:
        package = packageHashTable.search(packageID)
        notDelivered.append(package)
    # Clear the package list of a given truck so the packages can be placed back into the truck in the order
    # of the nearest neighbor
    trucks.packages.clear()

    # Cycle through the list of not_delivered until none remain in the list
    # Adds the nearest package into the truck.packages list one by one
    while len(notDelivered) > 0:
        nextAddress = 2000
        nextPackage = None
        for package in notDelivered:
            if distanceInBetween(extractAddress(trucks.address), extractAddress(package.address)) <= nextAddress:
                nextAddress = distanceInBetween(extractAddress(trucks.address), extractAddress(package.address))
                nextPackage = package
        # Appends the closest package to the front of the delivery list
        trucks.packages.append(nextPackage.ID)
        # Removes this package from the not delivered list
        notDelivered.remove(nextPackage)
        # for each delivery the mileage keeps being added up, updates addresses, and time of delivery based on next
        # address
        trucks.mileage += nextAddress
        trucks.address = nextPackage.address
        trucks.time += datetime.timedelta(hours=nextAddress / 18)
        nextPackage.deliveryTime = trucks.time
        nextPackage.departureTime = trucks.departureTime


# Load trucks
deliveringPackages(truck1)
deliveringPackages(truck2)

# This make it so that truck 3 stay at the hub until both of the other trucks are finished delivering their packages
truck3.depart_time = min(truck1.time, truck2.time)
deliveringPackages(truck3)


class Main:
    # User Interface
    # Prompts the user with a message that has calculated the total miles traveled by all WGU trucks.
    print("Western Governors University Parcel Service (WGUPS)")
    print("The total mileage traveled by all trucks is:")
    print(truck1.mileage + truck2.mileage + truck3.mileage)

    # Prompt the user for input to check the status of packages or exit
    while True:
        try:
            # Ask the user to enter their choice: continue or exit
            input1 = input(
                "If you would like to check the status of package(s), type 'continue'\nIf you would like to exit, type "
                "'exit'\n")

            if input1 == "continue":
                # Break the loop and continue with the program if the user chooses to continue
                break
            elif input1 == "exit":
                # Exit the program if the user chooses to exit
                exit()
            else:
                # Raise a ValueError if the user enters an invalid input
                raise ValueError("Your input was invalid.\nPlease type either 'continue' or 'exit'.")
        except ValueError as e:
            # Handle the ValueError by printing the error message
            print(e)


    # Prompt the user to enter a specific time to check package statuses
    while True:
        try:
            # Ask the user to enter a time in HH:MM:SS format
            userTime = input(
                "Please enter a time to check the status of package(s). Use the following format, HH:MM:SS\n")

            # Split the user's input into hours, minutes, and seconds
            (h, m, s) = userTime.split(":")

            # Convert the input into a timedelta object representing the specified time
            convertTimedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

            # Break the loop and continue with the rest of the code
            break
        except ValueError:
            # Handle the ValueError if the user's input is invalid
            print("Your input was invalid.\nRead the directions carefully and try again.")

    # Prompt the user to choose between checking a specific package or all packages
    while True:
        input2 = input(
            "To check the status of a specific package, type '1'\nTo check the status of all packages, type '2'\n")

        # Check if the user wants to check a specific package
        if input2 == "1":
            while True:
                try:
                    # Prompt the user to enter a specific package ID between 1 and 40
                    soloInput = input("Enter the specific package ID you'd like to check (between 1 and 40):\n")
                    package_id = int(soloInput)

                    # Check if the entered package ID is within the valid range
                    if 1 <= package_id <= 40:
                        # Retrieve the package information and update its status based on the specified time
                        package = packageHashTable.search(package_id)
                        package.updateStatus(convertTimedelta)
                        print(str(package))
                        break
                    else:
                        raise ValueError("Invalid package ID. Please enter a number between 1 and 40.")
                except ValueError as e:
                    # Handle the ValueError if the user's input for the package ID is invalid
                    print(e)

            while True:
                # After checking a specific package, prompt the user for the next action
                choice = input(
                    "Choose an option:\n1. Check another package\n2. Check all packages\n3. Use a new time\n4. Exit\n")

                # Check if the user wants to check another package
                if choice == "1":
                    # Prompt the user to enter a specific package ID between 1 and 40
                    while True:
                        try:
                            soloInput = input("Enter the specific package ID you'd like to check (between 1 and 40):\n")
                            package_id = int(soloInput)

                            # Check if the entered package ID is within the valid range
                            if 1 <= package_id <= 40:
                                # Retrieve the package information and update its status based on the specified time
                                package = packageHashTable.search(package_id)
                                package.updateStatus(convertTimedelta)
                                print(str(package))
                                break
                            else:
                                raise ValueError("Invalid package ID. Please enter a number between 1 and 40.")
                        except ValueError as e:
                            # Handle the ValueError if the user's input for the package ID is invalid
                            print(e)

                    while True:
                        # After checking a specific package, prompt the user for the next action
                        choice = input(
                            "Choose an option:\n1. Check another package\n2. Check all packages\n3. Use a new time\n4. "
                            "Exit\n")

                        # Check if the user wants to check another package
                        if choice == "1":
                            continue
                        # Check if the user wants to check all packages
                        elif choice == "2":
                            while True:
                                try:
                                    # Retrieve and print the status of all packages based on the specified time
                                    for packageID in range(1, 41):
                                        package = packageHashTable.search(packageID)
                                        package.updateStatus(convertTimedelta)
                                        print(str(package))
                                    break
                                except ValueError:
                                    print("Something went wrong! Please contact support for help!")
                        # Check if the user wants to use a new time
                        elif choice == "3":
                            while True:
                                try:
                                    # Prompt the user to enter a new time to check the status of packages
                                    userTime = input(
                                        "Please enter a new time to check the status of package(s). Use the following "
                                        "format, HH:MM:SS\n")
                                    (h, m, s) = userTime.split(":")
                                    convertTimedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                                    break
                                except ValueError:
                                    print("Your input was invalid.\nRead the directions carefully and try again.")
                            break
                        # Check if the user wants to exit the program
                        elif choice == "4":
                            exit()
                        else:
                            print("Invalid input. Please enter a valid option.")

        # Check if the user wants to check the status of all packages
        elif input2 == "2":
            try:
                # Retrieve and print the status of all packages based on the specified time
                for packageID in range(1, 41):
                    package = packageHashTable.search(packageID)
                    package.updateStatus(convertTimedelta)
                    print(str(package))
                break
            except ValueError:
                print("Something went wrong! Please contact support for help!")

        # Handle the case when the user enters an invalid option
        else:
            print("Your input was invalid.\nPlease type either '1' or '2'. ")
