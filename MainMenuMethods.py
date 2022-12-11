import re
from DatabaseConnection import databaseConnection, cur
from ConvenienceFunctions import is_not_integer_or_zero, make_ordinal, is_not_one_or_two, is_not_integer, week_magic


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
    if len(output) == 0:
        print("No trip offerings for that trip and date.")
        input("Press Enter to return to the main menu and try again...")
        return

    print("TripNumber, Date, Start Time, Arrival Time, Driver, BusID.")
    for row in output:
        print(row)
    input("\nPress enter to return to main menu...")

def displayStops():
    TripNumber = input("Enter a Trip Number: ")
    while is_not_integer_or_zero(TripNumber):
        TripNumber = input("Enter a Trip Number: ")

    SQL_Query = "SELECT * FROM Trip T WHERE T.TripNumber = " + TripNumber + " "
    cur.execute(SQL_Query)
    output = cur.fetchall()
    if len(output) == 0:
        print("No such Trip")
        input("Press Enter to return to the main menu and try again...")
        return

    SQL_Query = "SELECT * FROM TripStopInfo T WHERE T.TripNumber = " + TripNumber + " "
    cur.execute(SQL_Query)
    output = cur.fetchall()
    if len(output) == 0:
        print("This Trip apparently has no stops.")
        input("Press Enter to return to the main menu and try again...")
        return
    print("TripNumber, StopNumber, Sequence, Driving Time")
    for row in output:
        print(row)
    input("\nPress enter to return to main menu...")


#Ask professor about this one?
def displayDriverSchedule():
    DriverName = input("Enter the driver name: ")
    DriverName.lower()
    Date = input("Enter a date in YYYY-MM-DD format: ")
    startOfWeek, endOfWeek = week_magic(Date)
    if(startOfWeek == None or endOfWeek == None):
        input("Press Enter to return to main menu and try again...")
        return

    SQL_Query = "SELECT * FROM Driver D WHERE D.DriverName = \'" + DriverName + "\' "
    cur.execute(SQL_Query)
    output = cur.fetchall()
    if len(output) == 0:
        print("No such Driver")
        input("Press Enter to return to the main menu and try again...")
        return

    SQL_Query = "SELECT * FROM TripOffering T WHERE T.DriverName = \'" + DriverName + "\' AND T.Date >= \'" + str(startOfWeek) + "\' AND T.Date <= \'" + str(endOfWeek) + "\'"
    cur.execute(SQL_Query)
    output = cur.fetchall()
    print("Trip schedule between", startOfWeek,"and",endOfWeek,"for", DriverName +": ")
    for row in output:
        print(row)
    input("\nPress enter to return to main menu...")



def addDriver():
    DriverName = input("Enter the new driver name: ")
    DriverName.lower()
    DriverTelephoneNumber = input("Enter a telephone number for the new driver: ")
    cleanedNumber = re.sub('[^0-9]', '', DriverTelephoneNumber)
    while is_not_integer_or_zero(cleanedNumber):
        DriverTelephoneNumber = input("Enter a telephone number for the new driver: ")
        cleanedNumber = re.sub('[^0-9]', '', DriverTelephoneNumber)

    #check if driver is already in the system
    cur.execute("SELECT * FROM Driver D WHERE D.DriverName = \'" + DriverName + "\'")
    data = cur.fetchall()
    if len(data) != 0:
        print("This driver is already in the system.")
        input("Press enter to retun to main menu and try again...")
        return

    # Add in the new driver
    SQL_Insert = "INSERT INTO Driver (DriverName, DriverTelephoneNumber) " \
                 "VALUES (\'" + DriverName + "\'," + cleanedNumber + ");"
    cur.execute(SQL_Insert)
    databaseConnection.commit()
    input("\nNew Driver has been added. Press enter to return to main menu...")


def addBus():
    BusID = input("Enter the new BusID: ")
    while is_not_integer_or_zero(BusID):
        BusID = input("Enter the new BusID: ")
    model = input("Enter the model of the bus: ")
    year = input("Enter the year of the bus: ")
    while is_not_integer_or_zero(year):
        year = input("Enter the year of the bus: ")


    #check if bus is already in the system
    cur.execute("SELECT * FROM Bus B WHERE B.BusID = " + BusID + "")
    data = cur.fetchall()
    if len(data) != 0:
        print("This Bus is already in the system.")
        input("Press enter to retun to main menu and try again...")
        return

    # Add in the new bus
    SQL_Insert = "INSERT INTO Bus (BusID,Model,Year) " \
                 "VALUES (" + BusID + ",\'" + model + "\'," + year + ");"
    cur.execute(SQL_Insert)
    databaseConnection.commit()
    input("\nNew Bus has been added. Press enter to return to main menu...")


def deleteBus():
    BusID = input("Enter the BusID of the Bus to delete: ")
    while is_not_integer_or_zero(BusID):
        BusID = input("Enter the BusID of the Bus to delete: ")

    #check if bus is already in the system
    cur.execute("SELECT * FROM Bus B WHERE B.BusID = " + BusID + "")
    data = cur.fetchall()
    if len(data) == 0:
        print("This Bus is not in the system.")
        input("Press enter to retun to main menu and try again...")
        return

    SQL_Delete = "DELETE FROM Bus WHERE BusID = " + BusID + ";"
    cur.execute(SQL_Delete)
    databaseConnection.commit()
    input("Bus number "+ str(BusID)+ " has been deleted. Press enter to return to main menu...")


def insertActualTrip():
    print("Provide key for a trip offering")
    tripNumber = input("Enter the trip number for the trip offering: ")
    while is_not_integer_or_zero(tripNumber):
        tripNumber = input("Enter the trip number for the trip offering: ")
    Date = input("Enter the date for the trip offering in YYYY-MM-DD format: ")
    ScheduledStartTime = input("Enter the trip offering's scheduled start time: ")

    # check if this trip offering is invalid
    cur.execute("SELECT * FROM TripOffering T WHERE T.TripNumber = " + str(
        tripNumber) + " AND T.Date = \'" + Date + "\' AND T.ScheduledStartTime = \'" + ScheduledStartTime + "\'")
    data = cur.fetchall()
    if len(data) == 0:
        input("The trip offering with the trip number "+tripNumber+", date "+Date+", and start time "+ScheduledStartTime+" does not exist."
              "\nPress enter to return to main menu and try again...")
        return

    ScheduledArrivalTime = data[0][3]

    print("\nNow enter values for actural trip stop info")
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


    #check if the stop exists
    cur.execute("SELECT * FROM Stop S WHERE S.StopNumber = " + StopNumber)
    data = cur.fetchall()
    if len(data) == 0:
        input("The stop with the stop number "+StopNumber+" does not exist."
              "\nPress enter to return to main menu and try again...")
        return

    #check if that entry in ActualTripStopInfo already exists
    cur.execute("SELECT * FROM ActualTripStopInfo A WHERE A.TripNumber = " + tripNumber + " AND A.Date = \'" +Date+ "\' AND A.ScheduledStartTime = \'" + ScheduledStartTime + "\' AND A.StopNumber = " + str(StopNumber)+" ")
    data = cur.fetchall()
    if len(data) != 0:
        print("The actual trip stop info for this trip offering stop is already in the system.")
        input("Press enter to retun to main menu and try again...")
        return



    SQL_Insert = "INSERT INTO ActualTripStopInfo (TripNumber,Date,ScheduledStartTime,StopNumber,ScheduledArrivalTime,ActualStartTime," \
                 "ActualArrivalTime,NumberOfPassengerIn,NumberOfPassengerOut) " \
                 "VALUES (" + tripNumber + ",\'" + Date + "\',\'" + ScheduledStartTime + "\',"  + StopNumber + "" \
                          ",\'"+ ScheduledArrivalTime + "\',\'"+ ActualStartTime + "\',\'" + ActualArrivalTime + "\'," + NumberOfPassengersIn + "," + NumberOfPassengersOut + ");"
    cur.execute(SQL_Insert)
    databaseConnection.commit()
    input("The Actual trip stop info has been added. Press enter to return to main menu...")


#get some clarification on the tables??