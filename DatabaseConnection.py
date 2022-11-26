import sqlite3

databaseConnection = sqlite3.connect('test.db', check_same_thread=False)
cur = databaseConnection.cursor()