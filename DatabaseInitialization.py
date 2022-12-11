from DatabaseConnection import databaseConnection, cur


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
                "FOREIGN KEY (Date) REFERENCES TripOffering (Date),"
                "FOREIGN KEY (ScheduledStartTime) REFERENCES TripOffering (ScheduledStartTime),"
                "FOREIGN KEY (StopNumber) REFERENCES Stop (StopNumber),"
                "FOREIGN KEY (ScheduledArrivalTime) REFERENCES TripOffering (ScheduledArrivalTime)"
                ");")
    databaseConnection.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS TripStopInfo ("
                "TripNumber integer NOT NULL,"
                "StopNumber integer NOT NULL,"
                "SequenceNumber text,"
                "DrivingTime text,"
                "PRIMARY KEY (TripNumber, StopNumber)"
                "FOREIGN KEY (TripNumber) REFERENCES Trip (TripNumber),"
                "FOREIGN KEY (StopNumber) REFERENCES Stop (StopNumber)"
                ");")
    databaseConnection.commit()



def insertDummyData():
    SQL_Insert = "INSERT OR IGNORE INTO Trip (TripNumber,StartLocationName,DestinationName) " \
                 "VALUES " \
                 "(1,\"Los Angeles\",\"Pomona\")," \
                 "(2,\"Pomona\",\"Victorville\")," \
                 "(3,\"Diamond Bar\",\"Pomona\");"
    cur.execute(SQL_Insert)
    databaseConnection.commit()

    SQL_Insert = "INSERT OR IGNORE INTO Bus (BusID,Model,Year) " \
                 "VALUES " \
                 "(107,\"Model 1\",\"2007\")," \
                 "(126,\"Model 2\",\"2009\")," \
                 "(133,\"Model 3\",\"2011\");"
    cur.execute(SQL_Insert)
    databaseConnection.commit()

    SQL_Insert = "INSERT OR IGNORE INTO Driver (DriverName,DriverTelephoneNumber) " \
                 "VALUES " \
                 "(\"Jackson Overland\",5762427339)," \
                 "(\"Robert Waylan\",5763748207)," \
                 "(\"Samantha Greening\",5728861294);"
    cur.execute(SQL_Insert)
    databaseConnection.commit()

    SQL_Insert = "INSERT OR IGNORE INTO Stop (StopNumber,StopAddress) " \
                 "VALUES " \
                 "(17,\"14587 Calma Street\")," \
                 "(26,\"2786 Temple Avenue\")," \
                 "(9,\"7231 Hook Way\");"
    cur.execute(SQL_Insert)
    databaseConnection.commit()

    SQL_Insert = "INSERT OR IGNORE INTO TripOffering (TripNumber,Date,ScheduledStartTime,ScheduledArrivalTime,DriverName,BusID) " \
                 "VALUES " \
                 "(1,\"2022-05-11\",\"11:00 AM\", \"12:30 PM\",\"Jackson Overland\",107)," \
                 "(2,\"2022-05-12\",\"11:00 AM\", \"12:30 PM\",\"Jackson Overland\",107)," \
                 "(3,\"2022-05-13\",\"11:00 AM\", \"12:30 PM\",\"Jackson Overland\",107)," \
                 "(1,\"2022-05-11\",\"1:00 PM\", \"2:50 PM\",\"Jackson Overland\",107);"
    cur.execute(SQL_Insert)
    databaseConnection.commit()

    SQL_Insert = "INSERT OR IGNORE INTO TripStopInfo (TripNumber,StopNumber,SequenceNumber,DrivingTime) " \
                 "VALUES " \
                 "(1,17,\"26-9\", \"6 Hours\")," \
                 "(2,26,\"9-17\", \"2 Hours\")," \
                 "(3,9,\"17-26\", \"4 Hours\");"
    cur.execute(SQL_Insert)
    databaseConnection.commit()

    SQL_Insert = "INSERT OR IGNORE INTO ActualTripStopInfo (TripNumber,Date,ScheduledStartTime,StopNumber,ScheduledArrivalTime,ActualStartTime,ActualArrivalTime,NumberOfPassengerIn,NumberOfPassengerOut) " \
                 "VALUES " \
                 "(1,\"2022-05-11\",\"11:00 AM\",17,\"12:30 PM\",\"11:03 AM\",\"12:28 PM\",6,2);"
    cur.execute(SQL_Insert)
    databaseConnection.commit()