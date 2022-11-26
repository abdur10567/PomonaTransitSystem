from DatabaseConnection import databaseConnection, cur
from ConvenienceFunctions import is_not_integer, make_ordinal, is_not_one_or_two


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
    TripNumber = input("Enter a Trip Number: ")
    while is_not_integer(TripNumber):
        TripNumber = input("Enter a Trip Number: ")
    StopNumber = input("Enter a Stop Number: ")
    while is_not_integer(TripNumber):
        StopNumber = input("Enter a Stop Number: ")

    SQL_Query = "SELECT * FROM TripStopInfo T WHERE T.TripNumber = " + TripNumber + " AND T.StopNumber = " + StopNumber + ";"
    cur.execute(SQL_Query)
    output = cur.fetchall()
    print(output)


#Ask professor about this one?
def displayDriverSchedule():
    print("Display Driver schedule")


def addDriver():
    DriverName = input("Enter the new driver name: ")
    DriverName.lower()
    DriverTelephoneNumber = input("Enter a telephone number for the new driver: ")
    cleanedNumber = re.sub('[^0-9]', '', DriverTelephoneNumber)
    while is_not_integer(cleanedNumber):
        DriverTelephoneNumber = input("Enter a telephone number for the new driver: ")
        cleanedNumber = re.sub('[^0-9]', '', DriverTelephoneNumber)

    # Add in the new driver
    SQL_Insert = "INSERT INTO Driver (DriverName, DriverTelephoneNumber) " \
                 "VALUES (\'" + DriverName + "\'," + DriverTelephoneNumber + ");"
    cur.execute(SQL_Insert)
    databaseConnection.commit()


def addBus():
    BusID = input("Enter the new BusID: ")
    while is_not_integer(BusID):
        BusID = input("Enter the new BusID: ")
    model = input("Enter the model of the bus: ")
    year = input("Enter the year of the bus: ")
    while is_not_integer(year):
        year = input("Enter the year of the bus: ")

    # Add in the new bus
    SQL_Insert = "INSERT INTO Bus (BusID,Model,Year) " \
                 "VALUES (" + BusID + ",\'" + model + "\'," + year + ");"
    cur.execute(SQL_Insert)
    databaseConnection.commit()


def deleteBus():
    BusID = input("Enter the BusID of the Bus to delete: ")
    while is_not_integer(BusID):
        BusID = input("Enter the BusID of the Bus to delete: ")

    SQL_Delete = "DELETE FROM Bus WHERE BusID = " + BusID + ";"
    cur.execute(SQL_Delete)
    databaseConnection.commit()


def insertActualTrip():
    print("Insert Actual Trip")
