import psycopg2
import psycopg2.extras

from pypika import Query, Table

import settings
import helper


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


