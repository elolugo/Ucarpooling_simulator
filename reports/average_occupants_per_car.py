import psycopg2
import psycopg2.extras

from pypika import Query, Table

import settings
import helper


def generate_report(connections):
    """Generate report for amount of vehicles less with carpooling"""

    cursor = connections['smarttraffic'].cursor(cursor_factory=psycopg2.extras.DictCursor)

    querystring = """
    select carpool_id, count(ucarpoolingprofile_id) from
    public.uccarpool_carpool_poolers as poolers
    group by carpool_id
    """

    cursor.execute(querystring)
    rows = cursor.fetchall()

    total_poolers = 0
    total_carpools = 0
    for row in rows:
        total_poolers += row['count']
        total_carpools += 1

    helper.info_message(f'{total_carpools} total carpools')
    helper.info_message(f'{total_poolers / total_carpools} average poolers per carpool')


if __name__ == "__main__":
    connections = helper.connect_server_database()
    generate_report(connections)


