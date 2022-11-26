import sqlite3
from consolemenu import *
from consolemenu.items import *

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
                #"FOREIGN KEY (Date) REFERENCES TripOffering (Date),"
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
    Date = input("Enter a date in YYYY-MM-DD format: ")
    ScheduledStartTime = input("Enter the scheduled start time: ")
    ScheduledStartTime.lower()
    SQL_Query = "DELETE FROM TripOffering " \
                "WHERE TripNumber =\'"+TripNumber+"\' AND Date=\'"+Date+"\' AND ScheduledStartTime=\'"+ScheduledStartTime+"\';"
    cur.execute(SQL_Query)


def addTripOffering():
    print("option 2 lol")


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
        " asks if you have more trips to enter)", addTripOffering)

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
