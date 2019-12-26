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

def create_view(con):
    """Creates a view that selects all the distributed alumni data"""

    print("=================================CREATING VIEW=========================")
    cursorObj = con.cursor()

    try:
        """Deleting view if extists"""
        cursorObj.execute("DROP VIEW IF EXISTS ALUMNI_VIEW")
        con.commit()

        """Create view"""
        query = """
        CREATE VIEW ALUMNI_VIEW AS
        SELECT alumni.uuid, sex, career, alumni_cars.transport, alumni_smoker.smoker, alumni_music.music,
        alumni_eloquence.eloquence_level, alumni_itinerary.latitude, longitude, time_of_arrival, time_of_departure
            from alumni
            inner join alumni_cars on alumni_cars.uuid=alumni.uuid
            inner join alumni_smoker on alumni.uuid=alumni_smoker.uuid
            inner join alumni_music on alumni.uuid=alumni_music.uuid
            inner join alumni_eloquence on alumni.uuid=alumni_eloquence.uuid
            inner join alumni_itinerary on alumni.uuid=alumni_itinerary.uuid;"""

        cursorObj.execute(query)
        con.commit()
        helper.success_message("Created ALUMNI_VIEW View")

    except Error:
        helper.error_message(Error)


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
        cursorObj.execute("drop table if exists " + settings.DATABASE_TABLE_CARS)
        cursorObj.execute(
            "CREATE TABLE " + settings.DATABASE_TABLE_CARS + "(uuid integer PRIMARY KEY, transport text)")
        con.commit()
        helper.success_message("Created cars table")

        """
        Table for eloquence data
        """
        cursorObj.execute("drop table if exists " + settings.DATABASE_TABLE_ELOQUENCE)
        cursorObj.execute(
            "CREATE TABLE " + settings.DATABASE_TABLE_ELOQUENCE + "(uuid integer PRIMARY KEY, eloquence_level text)")
        con.commit()
        helper.success_message("Created eloquence table")

        """
        Table for itinerary data
        """
        cursorObj.execute("drop table if exists " + settings.DATABASE_TABLE_ITINERARY)
        cursorObj.execute(
            "CREATE TABLE " + settings.DATABASE_TABLE_ITINERARY + "(uuid integer PRIMARY KEY, "
                                                                  "latitude real, "
                                                                  "longitude real, "
                                                                  "time_of_arrival text, "
                                                                  "time_of_departure text)")
        con.commit()
        helper.success_message("Created itinerary table")

        """
        Table for music data
        """
        cursorObj.execute("drop table if exists " + settings.DATABASE_TABLE_MUSIC)
        cursorObj.execute(
            "CREATE TABLE " + settings.DATABASE_TABLE_MUSIC + "(uuid integer PRIMARY KEY, music text)")
        con.commit()
        helper.success_message("Deleted music taste database")

        """
        Table for smoker data
        """
        cursorObj.execute("drop table if exists " + settings.DATABASE_TABLE_SMOKER)
        cursorObj.execute(
            "CREATE TABLE " + settings.DATABASE_TABLE_SMOKER + "(uuid integer PRIMARY KEY, smoker text)")
        con.commit()

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

    create_view(con)
