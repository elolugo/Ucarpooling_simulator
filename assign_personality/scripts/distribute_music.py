import csv

import settings
import helper

from termcolor import colored

def distribute_music_taste():

    print('=========================DISTRIBUTING MUSIC TASTE=========================')

    """Count how many cars and the percentage of the total"""
    with open(settings.CSV_FORMDATA_INPUT_FILE_PATH, newline='', encoding=settings.FORM_FILE_ENCODING, errors='ignore') as csv_input_formdata:

        row_reader = csv.DictReader(csv_input_formdata, delimiter=settings.FORM_DELIMITER)

        total_records_form, music_distribution = helper.count_distribution(settings.FIELDNAME_MUSIC_TASTE, row_reader)

    """Assign the range of probability for each option of values"""
    helper.calculate_range_distribution(music_distribution)

    """Distribute the car and not car ownership"""
    with open(settings.CSV_USERDATA_INPUT_FILE_PATH, newline='', encoding=settings.SAPIENTIA_FILE_ENCODING) as csv_input_userdata, \
         open(settings.CSV_ASSIGNED_MUSIC_TASTE_FILE_PATH, 'w', newline='', encoding=settings.ASSIGNED_FILES_ENCODING) as csv_output_file:

        row_reader = csv.DictReader(csv_input_userdata, delimiter=settings.ASSIGNED_FILES_DELIMITER)

        """Writing the headers of the output file"""
        output_csv_fieldnames = row_reader.fieldnames
        output_csv_fieldnames.append(settings.FIELDNAME_MUSIC_TASTE)
        output_csv_writer = csv.DictWriter(csv_output_file, fieldnames=output_csv_fieldnames, delimiter=settings.ASSIGNED_FILES_DELIMITER)
        output_csv_writer.writeheader()

        """Actually apply the calculated distribution to the data"""
        helper.assign_distribution_to_alumni_data(
            row_reader=row_reader,
            csv_writer=output_csv_writer,
            distribution=music_distribution,
            column=settings.FIELDNAME_MUSIC_TASTE
        )


def populate_music_database():

    import sqlite3
    from sqlite3 import Error

    print(colored("Populating Database " + settings.DATABASE_TABLE_MUSIC, "yellow"))

    try:

        con = sqlite3.connect(settings.DATABASE)

        cursorObj = con.cursor()

        cursorObj.execute("drop table if exists " + settings.DATABASE_TABLE_MUSIC)
        cursorObj.execute(
            "CREATE TABLE " + settings.DATABASE_TABLE_MUSIC + "(uuid integer PRIMARY KEY, music text)")

        con.commit()

    except Error:

        print(Error)


    with open(settings.CSV_ASSIGNED_MUSIC_TASTE_FILE_PATH, 'r', newline='', encoding=settings.ASSIGNED_FILES_ENCODING) as csv_output_file:

        row_reader = csv.DictReader(csv_output_file, delimiter=settings.ASSIGNED_FILES_DELIMITER)

        for alumni in row_reader:
            query_string = "INSERT INTO " + settings.DATABASE_TABLE_MUSIC + \
                           " VALUES (" + alumni[settings.FIELDNAME_UUID] + ", '" \
                           + alumni[settings.FIELDNAME_MUSIC_TASTE] + "')"

            cursorObj.execute(query_string)

    con.commit()

    print(colored("Database " + settings.DATABASE_TABLE_MUSIC + " populated", "green"))

if __name__ == "__main__":
    distribute_music_taste()

    populate_music_database()