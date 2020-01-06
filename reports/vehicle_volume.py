import csv

import psycopg2
import psycopg2.extras

from pypika import Query, Table

import settings
import helper


def generate_csv_report(connections):
    """Generate a csv report with details of each alumni if they used cars before and after"""

    alumnis = {}

    cursor = connections['smarttraffic'].cursor(cursor_factory=psycopg2.extras.DictCursor)

    """Count the users that had vehicles prior Ucarpooling"""
    querystring = """
    select profile.id, itinerary."isDriver"  from
	ucusers_ucarpoolingprofile as profile
	inner join uccarpool_useritinerary as itinerary on itinerary."ucarpoolingProfile_id"=profile.id
    """

    cursor.execute(querystring)
    rows = cursor.fetchall()

    for row in rows:
        alumnis[row['id']] = {'before': row['isDriver']}

    """Count the users that has vehicles after Ucarpooling"""
    querystring = """
    select profile.id, carpool.driver_id  from
	ucusers_ucarpoolingprofile as profile
	left join uccarpool_carpool as carpool on profile.id=carpool.driver_id
	"""

    cursor.execute(querystring)
    rows = cursor.fetchall()

    for row in rows:
        alumnis[row['id']]['after'] = True if row['driver_id'] else False

    """Write in the csv data"""
    with open(settings.CSV_REPORT_CARS_FILE_PATH, 'w', newline='',
              encoding=settings.ASSIGNED_FILES_ENCODING) as csv_output_file:

        """Writing the headers of the output_data file"""
        output_csv_fieldnames = ['before', 'after']
        output_csv_writer = csv.DictWriter(csv_output_file, fieldnames=output_csv_fieldnames,
                                           delimiter=settings.ASSIGNED_FILES_DELIMITER)
        output_csv_writer.writeheader()

        """Iterate for each alumni"""
        for alumni in alumnis:
            output_csv_writer.writerow(alumnis[alumni])

    helper.info_message(f'Generated the cvs report file')


def generate_report(connections):
    """Generate report for amount of vehicles less with carpooling"""

    cursor = connections['smarttraffic'].cursor(cursor_factory=psycopg2.extras.DictCursor)


    cursor.execute('select count(*) from public.uccarpool_itineraryroute')
    row = cursor.fetchone()
    amount_vehicles_before = row['count']

    cursor.execute('select count(*) FROM public.uccarpool_carpool as carpool')
    row = cursor.fetchone()
    amount_vehicles_after = row['count']

    helper.info_message(f'There were {amount_vehicles_before} vehicles before')
    helper.info_message(f'There are {amount_vehicles_after} vehicles after')
    helper.info_message(f'There was a reduction of {round((1-float(amount_vehicles_after/amount_vehicles_before)) * 100, 2)}%')



if __name__ == "__main__":
    connections = helper.connect_server_database()
    generate_report(connections)
    generate_csv_report(connections)


