import csv

import sqlite3
from sqlite3 import Error

from termcolor import colored

import settings
import helper

def sql_connection():
    try:

        con = sqlite3.connect(settings.DATABASE)

        return con

    except Error:

        print(Error)


def create_tables(con):
    """
    Deletes all the tables.
    Erase everything and start from scratch with only the alumni database populated
    """

    print("=================================CREATING TABLES=========================")
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
        helper.success_message("Created alumni database")

        """
        Table for car data
        """
        cursorObj.execute('drop table if exists alumni_cars')
        con.commit()
        helper.success_message("Deleted cars database")

        """
        Table for eloquence data
        """
        cursorObj.execute('drop table if exists alumni_eloquence')
        con.commit()
        helper.success_message("Deleted eloquence database")

        """
        Table for itinerary data
        """
        cursorObj.execute('drop table if exists alumni_itinerary')
        con.commit()
        helper.success_message("Deleted itinerary database")

        """
        Table for smoker data
        """
        cursorObj.execute('drop table if exists alumni_smoker')
        con.commit()
        helper.success_message("Deleted smoker database")

        """
        Table for smoker data
        """
        cursorObj.execute('drop table if exists alumni_music')
        con.commit()
        helper.success_message("Deleted music taste database")

    except Error:
        helper.error_message(Error)

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

    helper.success_message("Uploaded successfully Sapientia Data to the DB")

if __name__ == "__main__":
    con = sql_connection()

    create_tables(con)

    populate_alumni_table(con)
