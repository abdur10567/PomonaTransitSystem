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
                "SequenceNumber integer,"
                "DrivingTime text,"
                "PRIMARY KEY (TripNumber, StopNumber)"
                "FOREIGN KEY (TripNumber) REFERENCES Trip (TripNumber),"
                "FOREIGN KEY (StopNumber) REFERENCES Stop (StopNumber)"
                ");")
    databaseConnection.commit()
