import sqlite3 as sql

import config

class Shipment:
    def __init__(self, date, tracking, gun, base, cable=0):
        self.gun         = gun
        self.base        = base
        self.cable       = cable
        self.date        = date
        self.tracking    = tracking

class Incident:
    def __init__(self, incidentnum, calldate, storenum, storecontact):
        self.incidentnum     = incidentnum
        self.calldate        = calldate
        self.storenum        = storenum
        self.storecontact    = storecontact
        

class InventoryDatabaseConnection:
    def __init__(self):
        con = sql.connect(config.db)
        con.execute("PRAGMA foreign_keys = ON")
        cur = con.cursor()

        self.con = con
        self.cur = cur

    def get_incident_by_incidentnum(self, incidentnumber):
        for row in self.cur.execute("SELECT * FROM INCIDENT WHERE INCIDENTNUM = ?", (incidentnumber,)):
            print(row)

    def get_shipment_by_tracking(self, tracking):
        for row in self.cur.execute("SELECT * FROM SHIPMENT WHERE TRACKING = ?", (tracking,)):
            print(row)

    def get_gun_by_ser(self, ser):
        for row in self.cur.execute("SELECT * FROM GUN WHERE SER = ?", (ser,)):
            print(row)

    def get_base_by_ser(self, ser):
        for row in self.cur.execute("SELECT * FROM BASE WHERE SER = ?", (ser,)):
            print(row)

    def insert_incident(self, _incident: Incident):
        data = (
            _incident.incidentnum    , 
            _incident.calldate       , 
            _incident.storenum       , 
            _incident.storecontact    
        )
        self.cur.execute("INSERT INTO INCIDENT VALUES(?, ?, ?, ?, NULL, NULL)",data)

    def insert_shipment(self, _shipment: Incident):
        data = (
            _shipment.gun     , 
            _shipment.base    , 
            _shipment.cable   , 
            _shipment.date    , 
            _shipment.tracking
        )

        self.cur.execute("INSERT INTO INCIDENT VALUES(NULL, ?, ?, ?, ?, ?)",data)

    def insert_gun_or_base(self, itemflag, ser, mod=None):
        if not ser:
            raise ValueError("Serial Number MUST be provided when inserting a gun or base!")
        data = (ser, mod)
        match itemflag:
            case 0: #gun
                self.cur.execute("INSERT INTO GUN VALUES(?, ?)", data)
            case 1: #base
                self.cur.execute("INSERT INTO BASE VALUES(?, ?)", data)
            case _:
                raise ValueError("Itemflag MUST be a one or zero!")





 ##                                     ##
## This section is for testing purposes  ##
 ##                                     ##

if __name__ == '__main__':
    dbcon = InventoryDatabaseConnection()

    while True:
        userinput = input("IncidentDatabaseAPI>").lower()
        match userinput:

            case "insert":
                i2 = input("Incident or Shipment? ")
                if i2[0].lower() == 'i':
                    newinc = Incident(
                        input("Enter incident number: "),
                        input("Enter date of call: "),
                        input("Enter Store Number: "),
                        input("Enter Name of Store Contact: ")
                    )
                    dbcon.insert_incident(newinc)
                elif i2[0].lower() == 's':
                    newship = Shipment(
                        input("Enter S/N of Gun: "),
                        input("Enter S/N of Base: "),
                        input("Enter Number of Cables: "),
                        input("Enter Date of Shipment: "),
                        input("Enter tracking number: "),
                    )
                    dbcon.insert_shipment(newship)
                else:
                    print("Unknown insert type provided")

            case "show":
                i2 = input("What table would you like to show?")
                if i2[0].lower() == 'i':
                    for row in dbcon.cur.execute("SELECT * FROM INCIDENT"):
                        print(row) 
                elif i2[0].lower() == 's':
                    for row in dbcon.cur.execute("SELECT * FROM SHIPMENT"):
                        print(row)
                elif i2[0].lower() == 'g':
                    for row in dbcon.cur.execute("SELECT * FROM GUN"):
                        print(row)
                elif i2[0].lower() == 'b':
                    for row in dbcon.cur.execute("SELECT * FROM BASE"):
                        print(row)
                else:
                    print("Unknown table requested for show")

            case "quit":
                break

            case _:
                print(f"Command '{userinput}' not defined")