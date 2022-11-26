from DatabaseConnection import databaseConnection, cur

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