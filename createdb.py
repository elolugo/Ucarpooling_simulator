import csv

import sqlite3
from sqlite3 import Error

from termcolor import colored

import settings

def sql_connection():
    try:

        con = sqlite3.connect(settings.DATABASE)

        return con

    except Error:

        print(Error)


def create_tables(con):
    print("=================================CREATING TABLES======================")
    cursorObj = con.cursor()

    try:
        """
        Main table for the sapientia data
        """

        """Delete the table if exists"""
        cursorObj.execute('drop table if exists alumni')
        """Create main table for alumni data"""
        cursorObj.execute(
            "CREATE TABLE alumni(uuid integer PRIMARY KEY, sex text, career text)")
        con.commit()
        print("Created alumni database")

        """
        Table for car data
        """
        cursorObj.execute('drop table if exists alumni_cars')
        con.commit()
        print("Deleted cars database")

        """
        Table for eloquence data
        """
        cursorObj.execute('drop table if exists alumni_eloquence')
        con.commit()
        print("Deleted eloquence database")

        """
        Table for itinerary data
        """
        cursorObj.execute('drop table if exists alumni_itinerary')
        con.commit()
        print("Deleted itinerary database")

        """
        Table for smoker data
        """
        cursorObj.execute('drop table if exists alumni_smoker')
        con.commit()
        print("Deleted smoker database")

        """
        Table for smoker data
        """
        cursorObj.execute('drop table if exists alumni_music')
        con.commit()
        print("Deleted music taste database")

    except Error:

        print(colored(Error, 'red'))

def populate_alumni_table(con):
    """
    Populate the main alumni table with sapientia data
    """
    cursorObj = con.cursor()

    with open(settings.CSV_USERDATA_INPUT_FILE_PATH, newline='', encoding=settings.SAPIENTIA_FILE_ENCODING,
              errors='ignore') as csv_input_userdata:

        row_reader = csv.DictReader(csv_input_userdata, delimiter=settings.ASSIGNED_FILES_DELIMITER)

        for alumni in row_reader:

            query_string = "INSERT INTO " + settings.DATABASE_TABLE_ALUMNI + \
                           " VALUES (" + alumni[settings.FIELDNAME_UUID] + ", '"\
                           + alumni[settings.FIELDNAME_SEX] + "', '" + alumni[settings.FIELDNAME_CAREER] + "')"

            cursorObj.execute(query_string)

    con.commit()

    print(colored("Uploaded successfully Sapientia Data to the DB", "green"))

if __name__ == "__main__":
    con = sql_connection()

    create_tables(con)

    populate_alumni_table(con)
