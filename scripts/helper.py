"""
Helper functions that are used throughout all files on the project
"""

import datetime
from scripts import settings
import random


def get_alumni_sapientia(row):

    alumni = {
        settings.FIELDNAME_UUID: row['UUID'],
        'SEXO': row['SEXO'],
        'CARRERA': row['CARRERA'],
        # 'DIRECCION': row['DIRECCION'],
        settings.FIELDNAME_LATITUDE: float(row['LATITUD']),
        settings.FIELDNAME_LONGITUDE: float(row['LONGITUD']),
    }

    return alumni

def get_alumni_form(row):

    alumni = {
        settings.FIELDNAME_UUID: str(row['UUID_FORM']),
        'CAREER': row['CAREER'],
        settings.FIELDNAME_TOA: datetime.datetime.strptime(row['TIME_OF_ARRIVAL'], '%H:%M:%S'),
        settings.FIELDNAME_TOD: datetime.datetime.strptime(row['TIME_OF_DEPARTURE'], '%H:%M:%S'),
        'SEX': row['SEX'],
        'SMOKER': row['SMOKER'],
        'ELOQUENCE_LEVEL': row['ELOQUENCE_LEVEL'],
        'IMPORTANCE_SMOKER': row['IMPORTANCE_SMOKER'],
        'IMPORTANCE_ELOQUENCE': row['IMPORTANCE_ELOQUENCE'],
        'IMPORTANCE_MUSIC': row['IMPORTANCE_MUSIC'],
        'IMPORTANCE_SEX': row['IMPORTANCE_SEX'],
        settings.FIELDNAME_TRANSPORT: row['TRANSPORT'],
        'MUSIC': row['MUSIC'],
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
    print("==============================================================================")
    print(f'total records in form data: {total_records}')
    for key in distribution:

        count = distribution[key]
        distribution[key] = {
            'count': count,
            'percentage': count / total_records
        }

        print(
            f'Total of {key} in the form is: {distribution[key]["count"]}  ------ percentage: {distribution[key]["percentage"]}%')

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

        for means_tranport in distribution:

            if distribution[means_tranport]['min'] < random_value <= distribution[means_tranport]['max']:

                alumni[column] = means_tranport

                csv_writer.writerow(alumni)

                if 'total_distributed' in distribution[means_tranport]:
                    distribution[means_tranport]['total_distributed'] += 1
                else:
                    distribution[means_tranport]['total_distributed'] = 1

                total_records += 1

                break

    """Printing all the results"""
    print("==============================================================================")
    print(f'Total records assigned to the sapientia data: {total_records}')

    for means_tranport in distribution:
        print(f'{means_tranport} assigned: {distribution[means_tranport]["total_distributed"]} accounting for: {distribution[means_tranport]["total_distributed"] / total_records}%')