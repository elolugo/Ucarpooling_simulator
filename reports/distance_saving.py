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

    """Count the distances that users had to travel prior Ucarpooling"""
    querystring = """
    select itinerary."ucarpoolingProfile_id", route."aggCost" from
	uccarpool_useritinerary as itinerary
    inner join uccarpool_itineraryroute as route on route.itinerary_id=itinerary.id
    """

    cursor.execute(querystring)
    rows = cursor.fetchall()

    for row in rows:
        cost = row['aggCost'][-1] if row['aggCost'] else 0
        alumnis[row['ucarpoolingProfile_id']] = {'before': cost}

    """Count the users that has vehicles after Ucarpooling"""
    querystring = """
    select itinerary."ucarpoolingProfile_id" , carpool.id, route."aggCost" from
	uccarpool_useritinerary as itinerary
    inner join uccarpool_itineraryroute as route on route.itinerary_id=itinerary.id
	left join uccarpool_carpool as carpool on itinerary."ucarpoolingProfile_id"=carpool.driver_id
	"""

    cursor.execute(querystring)
    rows = cursor.fetchall()

    for row in rows:
        cost = row['aggCost'][-1] if row['aggCost'] else 0
        alumnis[row['ucarpoolingProfile_id']]['after'] = cost if row['id'] else 0

    """Write in the csv data"""
    with open(settings.CSV_REPORT_DISTANCE_FILE_PATH, 'w', newline='',
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

    querystring = """
    select * from
    public.uccarpool_carpool_poolers as poolers
    inner join uccarpool_useritinerary as itinerary on poolers.ucarpoolingprofile_id=itinerary."ucarpoolingProfile_id"
    inner join uccarpool_itineraryroute as route on route.itinerary_id=itinerary.id
    """

    cursor.execute(querystring)
    rows = cursor.fetchall()

    total_distance_saved = 0
    for row in rows:
        aggCost = row['aggCost']
        total_distance_saved += aggCost[-1]

    total_distance_saved = round(total_distance_saved / 1000, 3)

    helper.info_message(f'{total_distance_saved} kilometers saved')
    helper.info_message(f'{total_distance_saved * 0.1} liters in fuel saved')
    helper.info_message(f'{total_distance_saved * 0.1 * 6000} guaranies saved')


if __name__ == "__main__":
    connections = helper.connect_server_database()
    generate_report(connections)
    generate_csv_report(connections)


