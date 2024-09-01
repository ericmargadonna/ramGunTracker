import sqlite3 as sql

import config


class Incident:
    def __init__(self, incidentnum, calldate, storenum, storecontact, sentgun, sentbase, sentcable, sentshipdate, senttracking, sentdeliverdate, recvgun, recvbase, recvcable, recvdate, recvtracking):
        self.incidentnum     = incidentnum
        self.calldate        = calldate
        self.storenum        = storenum
        self.storecontact    = storecontact
        self.sentgun         = sentgun
        self.sentbase        = sentbase
        self.sentcable       = sentcable
        self.sentshipdate    = sentshipdate
        self.senttracking    = senttracking
        self.sentdeliverdate = sentdeliverdate
        self.recvgun         = recvgun
        self.recvbase        = recvbase
        self.recvcable       = recvcable
        self.recvdate        = recvdate
        self.recvtracking    = recvtracking

class InventoryDatabase:
    def __init__(self):
        con = sql.connect(config.db)
        con.execute("PRAGMA foreign_keys = ON")
        cur = con.cursor()

        self.con = con
        self.cur = cur

    def get_incident(self, incidentnumber):
        for row in self.cur.execute("SELECT * FROM INCIDENT WHERE INCIDENTNUM = ?", (incidentnumber,)):
            print(row)

    def insert_incident(self, incident: Incident):
        data = (
            incident.incidentnum    , 
            incident.calldate       , 
            incident.storenum       , 
            incident.storecontact   , 
            incident.sentgun        , 
            incident.sentbase       , 
            incident.sentcable      , 
            incident.sentshipdate   , 
            incident.senttracking   , 
            incident.sentdeliverdate, 
            incident.recvgun        , 
            incident.recvbase       , 
            incident.recvcable      , 
            incident.recvdate       , 
            incident.recvtracking   , 
        )
        self.cur.execute("INSERT INTO INCIDENT VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",data)


if __name__ == '__main__':
    dbcon = InventoryDatabase()
    inum = input("Enter an incident number> ")
    testIncident = Incident(inum, "07/31/24", "624", "Bob", None, None, None, None, None, None, None, None, None, None, None)

    dbcon.insert_incident(testIncident)

    dbcon.get_incident(inum)

