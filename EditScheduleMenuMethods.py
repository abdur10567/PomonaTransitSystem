import re
from DatabaseConnection import databaseConnection, cur
from ConvenienceFunctions import is_not_integer_or_zero, make_ordinal, is_not_one_or_two

def deleteTripOffering():
    TripNumber = input("Enter a Trip Number: ")
    while is_not_integer_or_zero(TripNumber):
        TripNumber = input("Enter a Trip Number: ")
    Date = input("Enter a date in YYYY-MM-DD format: ")
    ScheduledStartTime = input("Enter the scheduled start time: ")
    SQL_Delete = "DELETE FROM TripOffering " \
                 "WHERE TripNumber =" + TripNumber + " AND Date=\'" + Date + "\' AND ScheduledStartTime=\'" + ScheduledStartTime + "\';"
    cur.execute(SQL_Delete)
    databaseConnection.commit()
    print("\nTrip Offering Deleted.")
    input("Press enter to return to the Edit Schedule Menu...")


def addTripOfferings():
    numberToAdd = input("How many Trip Offerings to add?: ")

    while is_not_integer_or_zero(numberToAdd):
        numberToAdd = input("\nHow many Trip Offerings to add?: ")

    numberToAdd = int(numberToAdd)
    i = 1
    setOfTripOfferings = []
    iterationTripOffering = {}
    while i <= numberToAdd:
        print("\n")
        #PERHAPS WE CAN REMOVE THIS LINE?
        iterationTripOffering.clear()
        tripNumber = input("Enter trip number for "+make_ordinal(i)+" trip offering: ")
        while is_not_integer_or_zero(tripNumber):
            tripNumber = input("Enter trip number for "+make_ordinal(i)+" trip offering: ")
        iterationTripOffering['TripNumber'] = tripNumber
        iterationTripOffering['Date'] = input("Enter the date for "+make_ordinal(i)+" trip offering in YYYY-MM-DD format: ")
        iterationTripOffering['ScheduledStartTime'] = input("Enter the Scheduled Start Time for "+make_ordinal(i)+" trip offering: ")
        iterationTripOffering['ScheduledArrivalTime'] = input("Enter the Scheduled Arrival Time for "+make_ordinal(i)+" trip offering: ")
        iterationTripOffering['DriverName'] = input("Enter the driver name for "+make_ordinal(i)+" trip offering: ")
        busID = input("Enter the BusID for "+make_ordinal(i)+" trip offering: ")
        while is_not_integer_or_zero(busID):
            busID = input("Enter the BusID for " + make_ordinal(i) + " trip offering: ")
        iterationTripOffering['BusID'] = busID
        setOfTripOfferings.append(iterationTripOffering)
        i += 1

    #get all possible new trip numbers and check if they don't already exist in the parent table
    possibleTripNumbers = [x['TripNumber'] for x in setOfTripOfferings]
    missingTrips = []
    for tripNumber in possibleTripNumbers:
        cur.execute("SELECT * FROM Trip T WHERE T.TripNumber = "+ str(tripNumber))
        data = cur.fetchall()
        if len(data) == 0:
            missingTrips.append(tripNumber)

    # get all possible new drivers and check if they don't already exist in the parent table
    possibleDriverNames = [x['DriverName'] for x in setOfTripOfferings]
    missingDrivers = []
    for driver in possibleDriverNames:
        cur.execute("SELECT * FROM Driver D WHERE D.DriverName = \'" + driver + "\'")
        data = cur.fetchall()
        if len(data) == 0:
            missingDrivers.append(driver)


    # get all possible new busID's and check if they don't already exist in the parent table
    possibleBusIDs = [x['BusID'] for x in setOfTripOfferings]
    missingBusIDs = []
    for b in possibleBusIDs:
        cur.execute("SELECT * FROM Bus B WHERE B.BusID = " + b)
        data = cur.fetchall()
        if len(data) == 0:
            missingBusIDs.append(b)

    if missingDrivers or missingBusIDs or missingTrips:
        print("Cannot add some or all trip offerings. Values missing in parent tables.")
        choice = input("\nWould you like to add those missing entries into the parent tables?\n"
                       "Enter 1 to add and 2 to cancel: ")
        while is_not_one_or_two(choice):
            choice = input("\nWould you like to add those missing entries into the parent tables?\n"
                           "Enter 1 to add and 2 to cancel: ")
        if int(choice) == 2:
            return

    if missingTrips:
        print("\nAdding missing trip numbers in parent table Trip")
        setOfTrips = []
        iterationTrips = {}
        for i in missingTrips:
            print("\n")
            # PERHAPS WE CAN REMOVE THIS LINE?
            iterationTrips.clear()
            iterationTrips['TripNumber'] = int(i)
            iterationTrips['StartLocationName'] = input("Enter the start location name for new trip number "+i+": ")
            iterationTrips['DestinationName'] = input("Enter the destination name for new trip number "+i+": ")
            setOfTrips.append(iterationTrips)

        #Add in the new trips
        SQL_Insert = "INSERT INTO Trip (TripNumber, StartLocationName, DestinationName) " \
                    "VALUES "
        for trip in setOfTrips:
            SQL_Insert += "(" + str(trip.get('TripNumber')) + ",\'" + trip.get('StartLocationName') + "\',\'" + trip.get('DestinationName') + "\'),"
        SQL_Insert = SQL_Insert[:-1] + ";"
        cur.execute(SQL_Insert)
        databaseConnection.commit()
        input("New Trips have been added. Press Enter to continue...")


    if missingDrivers:
        print("\nAdding missing drivers in parent table Driver")
        setOfDrivers = []
        iterationDrivers = {}
        for i in missingDrivers:
            print("\n")
            # PERHAPS WE CAN REMOVE THIS LINE?
            iterationDrivers.clear()
            iterationDrivers['DriverName'] = i
            DriverTelephoneNumber = input("Enter a telephone number for the new driver " + i + ": ")
            cleanedNumber = re.sub('[^0-9]', '', DriverTelephoneNumber)
            while is_not_integer_or_zero(cleanedNumber):
                DriverTelephoneNumber = input("Enter a telephone number for the new driver " + i + ": ")
                cleanedNumber = re.sub('[^0-9]', '', DriverTelephoneNumber)
            iterationDrivers['DriverTelephoneNumber'] = cleanedNumber
            setOfDrivers.append(iterationDrivers)


        #Add in the new drivers
        SQL_Insert ="INSERT INTO Driver (DriverName, DriverTelephoneNumber) " \
                    "VALUES "
        for dr in setOfDrivers:
            SQL_Insert += "(\'" + dr.get('DriverName') + "\'," + dr.get('DriverTelephoneNumber') + "),"
        SQL_Insert = SQL_Insert[:-1] + ";"
        cur.execute(SQL_Insert)
        databaseConnection.commit()
        input("New drivers have been added. Press Enter to continue...")


    if missingBusIDs:
        print("\nAdding missing buses in parent table Bus")
        setOfBuses = []
        iterationBus = {}
        for i in missingBusIDs:
            print("\n")
            iterationBus.clear()
            iterationBus['BusID'] = int(i)
            iterationBus['Model'] = input("Enter a model for the new bus #"+i+":")
            year = input("Enter the year for the new bus #"+i+":")
            while is_not_integer_or_zero(year):
                year = input("Enter the year for the new bus #"+i+":")
            iterationBus['Year'] = year
            setOfBuses.append(iterationBus)

        #Add in the new buses
        SQL_Insert ="INSERT INTO Bus (BusID, Model, Year) " \
                    "VALUES "
        for bus in setOfBuses:
            SQL_Insert += "(" + str(bus.get('BusID')) + ",\'" + bus.get('Model') + "\'," + bus.get('Year') + "),"
        SQL_Insert = SQL_Insert[:-1] + ";"
        cur.execute(SQL_Insert)
        databaseConnection.commit()
        input("New buses have been added. Press Enter to continue...")

    #now add in those trip offerings
    SQL_Insert = "INSERT INTO TripOffering (TripNumber, Date, ScheduledStartTime, ScheduledArrivalTime, DriverName, BusID) " \
                    "VALUES "
    for tripOffering in setOfTripOfferings:
        SQL_Insert += "("+tripOffering.get('TripNumber')+",\'"+tripOffering.get('Date')+"\',\'"+tripOffering.get('ScheduledStartTime')+"\'," \
                        "\'"+tripOffering.get('ScheduledArrivalTime') + "\',\'"+tripOffering.get('DriverName')+"\',"+tripOffering.get('BusID')+"),"

    SQL_Insert = SQL_Insert[:-1] + ";"
    cur.execute(SQL_Insert)
    databaseConnection.commit()

    input("All New Trip Offerings have also been added. Press Enter to return to edit schedule menu...")



def changeDriver():
    TripNumber = input("Enter a Trip Number: ")
    while is_not_integer_or_zero(TripNumber):
        TripNumber = input("Enter a Trip Number: ")
    Date = input("Enter a date in YYYY-MM-DD format: ")
    ScheduledStartTime = input("Enter the scheduled start time: ")
    DriverName = input("Enter the new driver name: ")


    cur.execute("SELECT * FROM TripOffering T Where T.TripNumber = " + TripNumber + " AND T.Date = \'" +Date+"\' AND T.ScheduledStartTime = \'" +ScheduledStartTime+"\'")
    data = cur.fetchall()
    if len(data) == 0:
        print("No such Trip Offering.")
        input("Press Enter to return to edit schedule menu and try again...")
        return

    #first check if the new driver name exists within the parent table Driver
    cur.execute("SELECT * FROM Driver D WHERE D.DriverName = \'" + DriverName + "\'" )
    data = cur.fetchall()
    if len(data) == 0:
        print("Cannot change driver for the given trip offering. In the parent table \'Driver\', the driver name: " + DriverName + " is missing.")
        choice = input("\nWould you like to add that driver to the parent table or cancel this action?\n"
                       "Enter 1 to add and 2 to cancel: ")
        while is_not_one_or_two(choice):
            choice = input("\nWould you like to add that driver to the parent table or cancel this action?\n"
                           "Enter 1 to add and 2 to cancel: ")

        #Drop out if user chooses to cancel action
        if int(choice) == 2:
            return

        DriverTelephoneNumber = input("Enter a telephone number for the new driver: ")
        cleanedNumber = re.sub('[^0-9]','', DriverTelephoneNumber)
        while is_not_integer_or_zero(cleanedNumber):
            DriverTelephoneNumber = input("Enter a telephone number for the new driver: ")
            cleanedNumber = re.sub('[^0-9]', '', DriverTelephoneNumber)

        #Add in the new driver
        SQL_Insert = "INSERT INTO Driver (DriverName, DriverTelephoneNumber) " \
                    "VALUES (\'" + DriverName + "\'," + cleanedNumber +");"
        cur.execute(SQL_Insert)
        databaseConnection.commit()
        input("New driver has been added. Press Enter to continue...")

    SQL_Update = "UPDATE TripOffering SET DriverName = \'" +DriverName+"\'" \
                 "WHERE TripNumber = "+TripNumber+" AND Date = \'" + Date + "\' AND ScheduledStartTime =\'" + ScheduledStartTime + "\'"

    cur.execute(SQL_Update)
    databaseConnection.commit()
    input("Driver has been changed for this trip offering. Press Enter to return to edit schedule menu...")

def changeBus():
    TripNumber = input("Enter a Trip Number: ")
    while is_not_integer_or_zero(TripNumber):
        TripNumber = input("Enter a Trip Number: ")
    Date = input("Enter a date in YYYY-MM-DD format: ")
    ScheduledStartTime = input("Enter the scheduled start time: ")
    BusID = input("Enter the new BusID: ")
    while is_not_integer_or_zero(BusID):
        BusID = input("Enter the new BusID: ")


    cur.execute("SELECT * FROM TripOffering T Where T.TripNumber = " + TripNumber + " AND T.Date = \'" +Date+"\' AND T.ScheduledStartTime = \'" +ScheduledStartTime+"\'")
    data = cur.fetchall()
    if len(data) == 0:
        print("No such Trip Offering.")
        input("Press Enter to return to edit schedule menu and try again...")
        return

    # first check if the new BusID name exists within the parent table Bus
    cur.execute("SELECT * FROM Bus B WHERE B.BusID = " + BusID)
    data = cur.fetchall()
    if len(data) == 0:
        print(
            "Cannot change bus for the given trip offering. In the parent table \'Bus\', the BusID: " + BusID + " is missing.")
        choice = input("\nWould you like to add that Bus to the parent table or cancel this action?\n"
                       "Enter 1 to add and 2 to cancel: ")
        while is_not_one_or_two(choice):
            choice = input("\nWould you like to add that Bus to the parent table or cancel this action?\n"
                           "Enter 1 to add and 2 to cancel: ")

        # Drop out if user chooses to cancel action
        if int(choice) == 2:
            return

        model = input("Enter the model of the bus: ")
        year = input("Enter the year of the bus: ")
        while is_not_integer_or_zero(year):
            year = input("Enter the year of the bus: ")

        # Add in the new bus
        SQL_Insert = "INSERT INTO Bus (BusID,Model,Year) " \
                     "VALUES (" + BusID + ",\'" + model + "\',"+year+");"
        cur.execute(SQL_Insert)
        databaseConnection.commit()

    SQL_Update = "UPDATE TripOffering SET BusID = " + BusID + " " \
                 "WHERE TripNumber = " + TripNumber + " AND Date = \'" + Date + "\' AND ScheduledStartTime =\'" + ScheduledStartTime + "\'"

    cur.execute(SQL_Update)
    databaseConnection.commit()
    input("Bus has been changed for this trip offering. Press Enter to return to edit schedule menu...")