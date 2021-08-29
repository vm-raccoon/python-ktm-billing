import os
import sqlite3
from datetime import datetime

class Database:

    def __init__(self, filename):
        self.__filename = filename + ".sqlite3"
        self.__createFile()

    def __createFile(self):
        try:
            connection = sqlite3.connect(self.__filename)
            self.__createTableHistory(connection)
        except sqlite3.Error:
            pass
        finally:
            if connection:
                connection.close()

    def __createTableHistory(self, connection):
        cursor = connection.cursor()
        query = """
            CREATE TABLE if not exists "history" (
                "ID"	INTEGER NOT NULL,
                "DateTime"	TEXT NOT NULL,
                "Balance"	REAL NOT NULL,
                "Cost"	REAL NOT NULL,
                "Message"	TEXT NOT NULL,
                "Rate"	TEXT,
                "Speed"	TEXT,
                PRIMARY KEY("ID" AUTOINCREMENT)
            );
        """
        cursor.execute(query)
        connection.commit()
        cursor.close()

    def __insertIntoHistory(self, connection, data):
        cursor = connection.cursor()
        query = f"""
            insert into "history" (
                "DateTime", "Balance", "Cost", "Message", "Rate", "Speed"
            ) values (
                "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}", {data["balance"]}, {data["cost"]}, "{data["message_end"]}", "{data["rate"]}", "{data["speed"]}"
            );
        """
        cursor.execute(query)
        connection.commit()
        cursor.close()

    def insert(self, data):
        try:
            connection = sqlite3.connect(self.__filename)
            self.__insertIntoHistory(connection, data)
        except sqlite3.Error as error:
            print(error)
        finally:
            if connection:
                connection.close()

    def __getLastHistoryRow(self, connection):
        cursor = connection.cursor()
        query = """
            select 
                "ID" as "id",
                "DateTime" as "datetime",
                "Balance" as "balance",
                "Cost" as "cost",
                "Message" as "message",
                "Rate" as "rate",
                "Speed" as "speed"
            from 
                history
            order by 
                DateTime desc
            limit 1;
        """
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row

    def getLastHistoryRow(self):
        lastRow = None
        try:
            connection = sqlite3.connect(self.__filename)
            connection.row_factory = sqlite3.Row
            lastRow = self.__getLastHistoryRow(connection)
        except sqlite3.Error as error:
            print(error)
        finally:
            if connection:
                connection.close()
        return dict(lastRow) if lastRow is not None else False
