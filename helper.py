"""
Helper functions that are used throughout all files on the project
"""

import datetime
import settings
import random
import psycopg2

from termcolor import colored


def warning_message(message):
    print(colored(message, "yellow"))


def error_message(message):
    print(colored(message, "red"))


def success_message(message):
    print(colored(message, "green"))


def detail_message(message):
    print(colored(message, "cyan"))


def info_message(message):
    print(colored(message, "grey"))


def no_matches_message(message):
    print(colored(message, "magenta"))


def get_alumni_sapientia(row):

    alumni = {
        settings.FIELDNAME_UUID: row[settings.FIELDNAME_UUID],
        settings.FIELDNAME_SEX: row[settings.FIELDNAME_SEX],
        settings.FIELDNAME_CAREER: row[settings.FIELDNAME_CAREER],
        settings.FIELDNAME_ADDRESS: row[settings.FIELDNAME_ADDRESS],
        settings.FIELDNAME_LATITUDE: float(row[settings.FIELDNAME_LATITUDE]),
        settings.FIELDNAME_LONGITUDE: float(row[settings.FIELDNAME_LONGITUDE]),
    }

    return alumni

def get_alumni_form(row):

    alumni = {
        settings.FIELDNAME_UUID: str(row['UUID_FORM']),
        'CAREER': row['CAREER'],
        settings.FIELDNAME_TOA: datetime.datetime.strptime(row['TIME_OF_ARRIVAL'], '%H:%M:%S'),
        settings.FIELDNAME_TOD: datetime.datetime.strptime(row['TIME_OF_DEPARTURE'], '%H:%M:%S'),
        settings.FIELDNAME_SEX: row[settings.FIELDNAME_SEX],
        settings.FIELDNAME_SMOKER: row[settings.FIELDNAME_SMOKER],
        settings.FIELDNAME_ELOQUENCE: row[settings.FIELDNAME_ELOQUENCE],
        'IMPORTANCE_SMOKER': row['IMPORTANCE_SMOKER'],
        'IMPORTANCE_ELOQUENCE': row['IMPORTANCE_ELOQUENCE'],
        'IMPORTANCE_MUSIC': row['IMPORTANCE_MUSIC'],
        'IMPORTANCE_SEX': row['IMPORTANCE_SEX'],
        settings.FIELDNAME_TRANSPORT: row[settings.FIELDNAME_TRANSPORT],
        settings.FIELDNAME_MUSIC_TASTE: row[settings.FIELDNAME_MUSIC_TASTE],
        'CARPOOL': row['CARPOOL']
    }

    return alumni


def count_distribution(column_to_count, row_reader):
    """
    Counts the distribution of a column of the form data.
    Returns the counts of values and the total record of the form data
    """

    total_records = 0

    distribution = {}

    for row in row_reader:  # For each row in the original CSV
        total_records = total_records + 1

        alumni = get_alumni_form(row)
        record_value = alumni[column_to_count]

        if record_value in distribution:
            distribution[record_value] = distribution[record_value] + 1
        else:
            distribution[record_value] = 1

    # Printing the results
    print("-------------------------------------------------------------------------")
    print(f'total records in form data: {total_records}')
    for key in distribution:

        count = distribution[key]
        distribution[key] = {
            'count': count,
            'percentage': count / total_records
        }

        print(
            f'Total of {key} in the form is: {distribution[key]["count"]}  ------ percentage: {(distribution[key]["percentage"])*100}%')

    return total_records, distribution


def calculate_range_distribution(distribution):
    """
    Assign the range of probability for each option of values.
    """

    ordered_options = sorted(distribution.items(), key=lambda kv: kv[1]['count'], reverse=False)

    # Assign range for distribution
    min = 0
    max = 0
    for item in ordered_options:
        item_percentage = item[1]['percentage']
        min = max
        max = min + item_percentage

        option = item[0]
        distribution[option]['min'] = min
        distribution[option]['max'] = max


def assign_distribution_to_alumni_data(row_reader, csv_writer, distribution, column):
    """
    Actually apply the calculated distribution to the data
    """

    total_records = 0

    for row in row_reader:  # For each row in the original CSV

        alumni = get_alumni_sapientia(row)

        # Generating random value from 0 to 1
        random_value = random.random()

        for option in distribution:

            if distribution[option]['min'] < random_value <= distribution[option]['max']:

                alumni[column] = option

                csv_writer.writerow(alumni)

                if 'total_distributed' in distribution[option]:
                    distribution[option]['total_distributed'] += 1
                else:
                    distribution[option]['total_distributed'] = 1

                total_records += 1

                break

    """Printing all the results"""
    print("-------------------------------------------------------------------------")
    print(f'Total records assigned to the sapientia data: {total_records}')

    try:

        for option in distribution:
            print(f'{option} assigned: {distribution[option]["total_distributed"]} accounting for: {(distribution[option]["total_distributed"] / total_records)*100}%')

    except Exception:

        print(option + " was not assigned to anyone")


def connect_server_database():
    """Returns a connection object for executing sql queris in the django database"""

    database = settings.DATABASE_SMARTTRAFFIC
    app_con = psycopg2.connect(
        database=database["NAME"],
        user=database["USER"],
        password=database["PASSWORD"],
        host=database["HOST"],
        port=database["PORT"]
    )

    database = settings.DATABASE_MAP
    map_con = psycopg2.connect(
        database=database["NAME"],
        user=database["USER"],
        password=database["PASSWORD"],
        host=database["HOST"],
        port=database["PORT"]
    )

    success_message("Databases connected")
    return {'smarttraffic': app_con, 'map': map_con}