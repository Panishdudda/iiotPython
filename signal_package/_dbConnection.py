import sqlite3 as sqlite

def databaseConnection(database):
    CONNECTION = sqlite.connect(database)
    if CONNECTION:
        CURSOR = CONNECTION.cursor()
        print("ESTABLISHED CONNECTION SUCESSFULLY WITH DATABASE")
        return CONNECTION,CURSOR
    else:
        print("FAILED TO ESTABLISH CONNECTION WITH DATABASE") 
        return None
