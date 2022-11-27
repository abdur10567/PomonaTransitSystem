from DatabaseConnection import databaseConnection, cur
from ConvenienceFunctions import is_not_integer_or_zero, make_ordinal, is_not_one_or_two, is_not_integer


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
    while is_not_integer_or_zero(TripNumber):
        TripNumber = input("Enter a Trip Number: ")
    StopNumber = input("Enter a Stop Number: ")
    while is_not_integer_or_zero(TripNumber):
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
    while is_not_integer_or_zero(cleanedNumber):
        DriverTelephoneNumber = input("Enter a telephone number for the new driver: ")
        cleanedNumber = re.sub('[^0-9]', '', DriverTelephoneNumber)

    # Add in the new driver
    SQL_Insert = "INSERT INTO Driver (DriverName, DriverTelephoneNumber) " \
                 "VALUES (\'" + DriverName + "\'," + cleanedNumber + ");"
    cur.execute(SQL_Insert)
    databaseConnection.commit()


def addBus():
    BusID = input("Enter the new BusID: ")
    while is_not_integer_or_zero(BusID):
        BusID = input("Enter the new BusID: ")
    model = input("Enter the model of the bus: ")
    year = input("Enter the year of the bus: ")
    while is_not_integer_or_zero(year):
        year = input("Enter the year of the bus: ")

    # Add in the new bus
    SQL_Insert = "INSERT INTO Bus (BusID,Model,Year) " \
                 "VALUES (" + BusID + ",\'" + model + "\'," + year + ");"
    cur.execute(SQL_Insert)
    databaseConnection.commit()


def deleteBus():
    BusID = input("Enter the BusID of the Bus to delete: ")
    while is_not_integer_or_zero(BusID):
        BusID = input("Enter the BusID of the Bus to delete: ")

    SQL_Delete = "DELETE FROM Bus WHERE BusID = " + BusID + ";"
    cur.execute(SQL_Delete)
    databaseConnection.commit()


def insertActualTrip():
    # PERHAPS WE CAN REMOVE THIS LINE?
    tripNumber = input("Enter the trip number for the trip offering: ")
    while is_not_integer_or_zero(tripNumber):
        tripNumber = input("Enter the trip number for the trip offering: ")
    Date = input("Enter the date for the trip offering in YYYY-MM-DD format: ")
    ScheduledStartTime = input("Enter the trip offering's scheduled start time: ")
    ScheduledArrivalTime = input("Enter the trip offering's scheduled arrival time: ")
    StopNumber = input("Enter the stop number: ")
    while is_not_integer_or_zero(StopNumber):
        StopNumber = input("Enter the stop number: ")

    ActualStartTime = input("Enter the trip offering's actual start time: ")
    ActualArrivalTime = input("Enter the trip offering's actual arrival time: ")
    StopNumber = input("Enter the stop number: ")
    while is_not_integer_or_zero(StopNumber):
        StopNumber = input("Enter the stop number: ")
    NumberOfPassengersIn = input("Number of passengers entering at this stop: ")
    while is_not_integer(NumberOfPassengersIn):
        NumberOfPassengersIn = input("Number of passengers entering at this stop: ")
    NumberOfPassengersOut = input("Number of passengers entering at this stop: ")
    while is_not_integer(NumberOfPassengersOut):
        NumberOfPassengersOut = input("Number of passengers exiting at this stop: ")

    #check if this trip offering, stop, or trip are invalid
    cur.execute("SELECT * FROM Trip T WHERE T.TripNumber = " + tripNumber)
    data = cur.fetchall()
    if len(data) == 0:
        input("The trip with the trip number "+tripNumber+" does not exist.\nPress enter to return to main menu and try again...")
        return

    cur.execute("SELECT * FROM TripOffering T WHERE T.TripNumber = "+tripNumber+" AND T.Date = \'"+Date+"\' AND T.ScheduledStartTime = \'" + ScheduledStartTime +"\'")
    data = cur.fetchall()
    if len(data) == 0:
        input("The trip offering with the trip number "+tripNumber+", date "+Date+", and start time "+ScheduledStartTime+" does not exist."
              "\nPress enter to return to main menu and try again...")
        return

    cur.execute("SELECT * FROM Stop S WHERE S.StopNumber = " + StopNumber)
    data = cur.fetchall()
    if len(data) == 0:
        input("The stop with the stop number "+StopNumber+" does not exist."
              "\nPress enter to return to main menu and try again...")
        return

    SQL_Insert = "INSERT INTO ActualTripStopInfo (TripNumber,Date,ScheduledStartTime,StopNumber,ScheduledArrivalTime,ActualStartTime," \
                 "ActualArrivalTime,NumberOfPassengerIn,NumberOfPassengerOut) " \
                 "VALUES (" + tripNumber + ",\'" + Date + "\',\'" + ScheduledStartTime + "\',"  + StopNumber + "" \
                          ",\'"+ ScheduledArrivalTime + "\',\'"+ ActualStartTime + "\',\'" + ActualArrivalTime + "\'," + NumberOfPassengersIn + "," + NumberOfPassengersOut + ");"
    cur.execute(SQL_Insert)
    databaseConnection.commit()


#get some clarification on the tables??