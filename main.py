import sqlite3
from consolemenu import *
from consolemenu.items import *
from convenienceFunctions import is_not_integer, make_ordinal, is_not_one_or_two

databaseConnection = sqlite3.connect('test.db', check_same_thread=False)
cur = databaseConnection.cursor()
print("Opened database successfully")


def initializeDatabase():
    # Add all tables to database
    cur.execute("CREATE TABLE IF NOT EXISTS Trip ("
                "TripNumber integer NOT NULL,"
                "StartLocationName text,"
                "DestinationName text,"
                "PRIMARY KEY (TripNumber)"
                ");")
    databaseConnection.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS TripOffering ("
                "TripNumber integer NOT NULL,"
                "Date text NOT NULL,"
                "ScheduledStartTime text NOT NULL,"
                "ScheduledArrivalTime text,"
                "DriverName text NOT NULL,"
                "BusID integer NOT NULL,"
                "PRIMARY KEY (TripNumber, Date, ScheduledStartTime),"
                "FOREIGN KEY (TripNumber) REFERENCES Trip (TripNumber),"
                "FOREIGN KEY (BusID) REFERENCES Bus (BusID),"
                "FOREIGN KEY (DriverName) REFERENCES Driver (DriverName)"
                ");")
    databaseConnection.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS Bus ("
                "BusID integer NOT NULL,"
                "Model text,"
                "Year text,"
                "PRIMARY KEY (BusID)"
                ");")
    databaseConnection.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS Driver ("
                "DriverName text NOT NULL,"
                "DriverTelephoneNumber integer,"
                "PRIMARY KEY (DriverName)"
                ");")
    databaseConnection.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS Stop ("
                "StopNumber integer NOT NULL,"
                "StopAddress text,"
                "PRIMARY KEY (StopNumber)"
                ");")
    databaseConnection.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS ActualTripStopInfo ("
                "TripNumber integer NOT NULL,"
                "Date text NOT NULL,"
                "ScheduledStartTime text NOT NULL,"
                "StopNumber integer NOT NULL,"
                "ScheduledArrivalTime text,"
                "ActualStartTime text,"
                "ActualArrivalTime text,"
                "NumberOfPassengerIn integer,"
                "NumberOfPassengerOut integer,"
                "PRIMARY KEY (TripNumber, Date, ScheduledStartTime, StopNumber),"
                "FOREIGN KEY (TripNumber) REFERENCES Trip (TripNumber),"
                # "FOREIGN KEY (Date) REFERENCES TripOffering (Date),"
                "FOREIGN KEY (ScheduledStartTime) REFERENCES TripOffering (ScheduledStartTime),"
                "FOREIGN KEY (StopNumber) REFERENCES Stop (StopNumber),"
                "FOREIGN KEY (ScheduledArrivalTime) REFERENCES TripOffering (ScheduledArrivalTime)"
                ");")
    databaseConnection.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS TripStopInfo ("
                "TripNumber integer NOT NULL,"
                "StopNumber integer NOT NULL,"
                "SequenceNumber integer,"
                "DrivingTime text,"
                "PRIMARY KEY (TripNumber, StopNumber)"
                ");")
    databaseConnection.commit()


def displaySchedule():
    startLocationName = input("Enter a start location: ")
    startLocationName.lower()
    DestinationName = input("Enter a destination: ")
    DestinationName.lower()
    Date = input("Enter a date in YYYY-MM-DD format: ")
    SQL_Query = "SELECT T2.* " \
                "FROM TripOffering T2 " \
                "WHERE T2.Date =\'" + Date + "\' AND T2.TripNumber IN(SELECT T.TripNumber " \
                                             "FROM Trip T " \
                                             "WHERE T.StartLocationName =\'" + startLocationName + "\' " \
                                                                                                   "AND T.DestinationName=\'" + DestinationName + "\');"
    cur.execute(SQL_Query)
    output = cur.fetchall()
    for row in output:
        print(row)


def deleteTripOffering():
    TripNumber = input("Enter a Trip Number: ")
    while is_not_integer(TripNumber):
        TripNumber = input("Enter a Trip Number: ")
    Date = input("Enter a date in YYYY-MM-DD format: ")
    ScheduledStartTime = input("Enter the scheduled start time: ")
    ScheduledStartTime.lower()
    SQL_Query = "DELETE FROM TripOffering " \
                "WHERE TripNumber =" + TripNumber + " AND Date=\'" + Date + "\' AND ScheduledStartTime=\'" + ScheduledStartTime + "\';"
    cur.execute(SQL_Query)


def addTripOfferings():
    numberToAdd = input("How many Trip Offerings to add?: ")

    while is_not_integer(numberToAdd):
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
        while is_not_integer(tripNumber):
            tripNumber = input("Enter trip number for "+make_ordinal(i)+" trip offering: ")
        iterationTripOffering['TripNumber'] = tripNumber
        iterationTripOffering['Date'] = input("Enter the date for "+make_ordinal(i)+" trip offering in YYYY-MM-DD format: ")
        iterationTripOffering['ScheduledStartTime'] = input("Enter the Scheduled Start Time for "+make_ordinal(i)+" trip offering: ")
        iterationTripOffering['ScheduledArrivalTime'] = input("Enter the Scheduled Arrival Time for "+make_ordinal(i)+" trip offering: ")
        iterationTripOffering['DriverName'] = input("Enter the driver name for "+make_ordinal(i)+" trip offering: ")
        busID = input("Enter the BusID for "+make_ordinal(i)+" trip offering: ")
        while is_not_integer(busID):
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

    if missingTrips:
        print("Cannot add some or all trip offerings. In the parent table \'Trip\', trips with the trip numbers: \n" + str(missingTrips) + " are missing.")
        choice = input("\nWould you like to add those Trips or cancel this action?\n"
                       "Enter 1 to add and 2 to cancel: ")
        while is_not_one_or_two(choice):
            choice = input("Would you like to add those Trips or cancel this action?\n"
                           "Enter 1 to add and 2 to cancel: ")

        if int(choice) == 2:
            return

        #ask use for the information needed to add new trips
        setOfTrips = []
        iterationTrips = {}
        for i in missingTrips:
            print("\n")
            # PERHAPS WE CAN REMOVE THIS LINE?
            iterationTrips.clear()
            iterationTrips['TripNumber'] = int(i)
            iterationTrips['StartLocationName'] = input("Enter the start location name for trip number "+i+": ")
            iterationTrips['DestinationName'] = input("Enter the destination name for trip number "+i+": ")

        #Add in the new trips
        SQL_Query = "INSERT INTO Trip (TripNumber, StartLocationName, DestinationName) " \
                    "VALUES "
        for trip in setOfTrips:
            SQL_Query += "(" + trip.get('TripNumber') + "," + trip.get('StartLocationName') + "," + trip.get('DestinationName') + "),"
        SQL_Query = SQL_Query[:-1] + ";"
        cur.execute(SQL_Query)

    input("New Trips have been added. Press Enter to continue...")

    #now add in those trip offerings
    SQL_Query = "INSERT INTO TripOffering (TripNumber, Date, ScheduledStartTime, ScheduledArrivalTime, DriverName, BusID) " \
                    "VALUES "
    for tripOffering in setOfTripOfferings:
        SQL_Query += "("+tripOffering.get('TripNumber')+","+tripOffering.get('Date')+","+tripOffering.get('ScheduledStartTime')+"," \
                        ""+tripOffering.get('ScheduledArrivalTime') + ","+tripOffering.get('DriverName')+","+tripOffering.get('BusID')+"),"

    SQL_Query = SQL_Query[:-1] + ";"
    cur.execute(SQL_Query)

    input("New Trip Offerings have also been added. Press Enter to return to edit schedule menu...")




def changeDriver():
    print("option 3 lol")


def changeBus():
    print("option 4 lol")


def displayStops():
    print("Display stops")


def displayDriverSchedule():
    print("Display Driver schedule")


def addDriver():
    print("Add a driver")


def addBus():
    print("Add a Bus")


def deleteBus():
    print("Delete a bus")


def insertActualTrip():
    print("Insert Actual Trip")


def main():
    # initialize our database and create its tables
    initializeDatabase()
    print("Database initialized Successfully")

    # create a menu with options
    menu = ConsoleMenu("Main Menu")
    function_item1 = FunctionItem(
        "Display the schedule of all trips for a given start location, destination, and date.", displaySchedule)

    function_item2 = FunctionItem(
        "Display the stops of a given trip.", displayStops)

    function_item3 = FunctionItem(
        "Display the weekly schedule of a given driver and date.", displayDriverSchedule)

    function_item4 = FunctionItem(
        "Add a driver.", addDriver)

    function_item5 = FunctionItem(
        "Add a bus.", addBus)

    function_item6 = FunctionItem(
        "Delete a bus.", deleteBus)

    function_item7 = FunctionItem(
        "Insert data for an actual trip specified by its key.", insertActualTrip)

    editScheduleSubmenu = ConsoleMenu("Edit Schedules")
    editScheduleOption1 = FunctionItem("Delete a trip offering by TripNumber, Date, and Scheduled Start Time.",
                                       deleteTripOffering)

    # WHAT DOES THE PROFESSOR WANT FOR THIS ONE?
    editScheduleOption2 = FunctionItem(
        "Add a set of trip offerings assuming the values of all attributes are given (the software"
        " asks if you have more trips to enter)", addTripOfferings)

    editScheduleOption3 = FunctionItem("Change the driver for a given Trip Offering.", changeDriver)
    editScheduleOption4 = FunctionItem("Change the bus for a given Trip Offering.", changeBus)

    editScheduleSubmenu.append_item(editScheduleOption1)
    editScheduleSubmenu.append_item(editScheduleOption2)
    editScheduleSubmenu.append_item(editScheduleOption3)
    editScheduleSubmenu.append_item(editScheduleOption4)

    submenu_item_1 = SubmenuItem("Edit Schedules", submenu=editScheduleSubmenu)
    submenu_item_1.set_menu(menu)

    menu.append_item(function_item1)
    menu.append_item(submenu_item_1)
    menu.append_item(function_item2)
    menu.append_item(function_item3)
    menu.append_item(function_item4)
    menu.append_item(function_item5)
    menu.append_item(function_item6)
    menu.append_item(function_item7)
    menu.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
