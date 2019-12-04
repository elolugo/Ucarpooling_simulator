import requests

import sqlite3
from sqlite3 import Error

from pypika import Query, Table
from datetime import date

import settings
import helper


def upload_users_itinerary():
    """
    Uploads all the generated users profile to api/ucarpooling/users/
    """

    alumni_auth = Table(settings.DATABASE_TABLE_AUTH)

    try:
        con = sqlite3.connect(settings.DATABASE)
        con.row_factory = sqlite3.Row

        cursorObj = con.cursor()

        """Building the query for retrieving all the users and their assigned profiles"""
        querystring = Query \
            .from_(Table(settings.DATABASE_TABLE_ALUMNI)) \
            .join(Table(settings.DATABASE_TABLE_ITINERARY)) \
            .on_field('uuid') \
            .join(Table(settings.DATABASE_TABLE_CARS)) \
            .on_field('uuid') \
            .select('*')\
            .limit(5)

        # print(querystring.get_sql())
        """Executing the query"""
        rows = cursorObj.execute(querystring.get_sql()).fetchall()

        """Iteraring for each row in the database for alumni"""
        for alumni in rows:


            """Building the body in a json-like format for the boy of the POST request"""
            orige = f'{alumni[settings.FIELDNAME_LATITUDE.lower()]},{alumni[settings.FIELDNAME_LONGITUDE.lower()]}'
            toa = f'{date.today()}T{alumni[settings.FIELDNAME_TOA.lower()]}Z'
            body = {
                "isDriver": True if alumni[settings.FIELDNAME_TRANSPORT.lower()] == 'Car' else False,
                "origin": orige,
                "destination": "-25.324491,-57.635437",  # Uca latitude and longitude
                "timeOfArrival": toa
            }

            """Getting the token of the alumni for the POST header"""
            querystring = Query\
                .from_(alumni_auth)\
                .select(alumni_auth.token)\
                .where(alumni_auth.uuid == alumni[settings.FIELDNAME_UUID.lower()])

            cursorObj.execute(querystring.get_sql())
            alumni_token = (cursorObj.fetchone())['token']

            """POST request for the itinerary"""
            response = requests.post(
                settings.USER_ITINERARY_URL,
                json=body,
                headers={
                    "Authorization": f'Token {alumni_token}'  # Token og the Ucarpooling app
                }
            )

            if response.status_code == 201:
                helper.success_message(f'Uploaded successfully itinerary for alumni {alumni[settings.FIELDNAME_UUID.lower()]}')
            else:
                helper.error_message(f'Error uploading itinerary for alumni {alumni[settings.FIELDNAME_UUID.lower()]} '
                                     f'---- status code: {response.status_code}: {response.reason}')

    except Error:

        print(Error)

    finally:

        """Closing the database connection"""
        con.close()


if __name__ == "__main__":
    upload_users_itinerary()
