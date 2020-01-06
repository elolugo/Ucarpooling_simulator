import psycopg2
import psycopg2.extras

from pypika import Query, Table

import settings
import helper


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


