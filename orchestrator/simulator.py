import requests
import random
import time

import sqlite3
from sqlite3 import Error

from pypika import Query, Table
from chronometer import Chronometer

import settings
import helper


def get_matcher_url(user_itinerary_id):
    """Returns the matcher URL for the alumni"""

    matcher_url = f'{settings.USER_ITINERARY_URL}{user_itinerary_id}/matches'

    return matcher_url

def get_requesters():
    """
    Returns the sorted list of people that will request
    a match from the server and will request a carpool partner.
    """

    try:
        con = sqlite3.connect(settings.DATABASE)
        con.row_factory = sqlite3.Row

        cursorObj = con.cursor()
        cars = Table(settings.DATABASE_TABLE_CARS)
        """Building the query for retrieving all the users and their assigned profiles"""
        querystring = Query \
            .from_(Table(settings.DATABASE_TABLE_ALUMNI)) \
            .join(cars) \
            .on_field('uuid') \
            .join(Table(settings.DATABASE_TABLE_AUTH)) \
            .on_field('uuid') \
            .join(Table(settings.DATABASE_TABLE_USER_ITINERARY)) \
            .on_field('uuid') \
            .select('*') \
            .where(cars.transport == 'Car') \
            .limit(settings.LIMIT_USERS)

        """Executing the query"""
        rows = cursorObj.execute(querystring.get_sql()).fetchall()

        return rows

    except Error:
        print(Error)


def get_carpooling_partner(matched_poolers):
    """Calculate which if any of the matched pooler the user is going to go"""

    carpoolers = []
    poolers_in_carpool = 1

    """Iterates through all matched users"""
    for matched_pooler in matched_poolers:

        """If the carpooling is already at max capacity"""
        if poolers_in_carpool > settings.POOLERS_LIMIT_PER_CAR:
            break

        """Acceptance probability according to the simulation configurarions"""
        acceptance_probability = matched_pooler['match_percentage'] * settings.TOLERANCE_PERCENTAGE

        if acceptance_probability > settings.ACCEPTANCE_THRESHOLD:
            carpoolers.append(matched_pooler)
            poolers_in_carpool += 1

    return carpoolers


def create_carpool(alumni_id, partners, alumni_useritinerary_id):
    """Creates in the back-end a carpooling containing the user and his partners"""
    poolers_id = []

    for partner in partners:
        poolers_id.append(partner['user_id'])

    """Building the body in a json-like format for the boy of the POST request"""
    body = {
        "driver": alumni_id,
        "poolers": poolers_id,
        "route": alumni_useritinerary_id
    }

    "POST the carpooling data to the API to create a carpool in the back-end"
    response = requests.post(
        url=settings.CARPOOL_URL,
        json=body,
        headers={
            "Authorization": f'Token {settings.BACKEND_STAFF_TOKEN}'
        }
    )

    if response.status_code == 201:
        helper.success_message(f'Uploaded created carpool successfully for alumni {alumni_id} in back-end')
    else:
        helper.error_message(f'Error creating carpool for alumni {alumni_id} in back-end '
                             f'---- status code: {response.status_code}: {response.reason}')


def simulator():
    """
    Simulates the use of the Ucarpooling app
    """

    """Variables for statistics in the simulation"""
    max_time = 0
    total_time = 0
    total_errors = 0

    """Get the set of people that will request a carpooling partner"""
    rows = get_requesters()

    helper.info_message(f'==============STARTING SIMULATION=====================')

    """Iteraring for each row in the database for alumni"""
    with Chronometer() as time_simulation:
        for alumni in rows:

            print('=========================================')

            alumni_token = alumni['token']
            alumni_id = alumni[settings.FIELDNAME_UUID.lower()]
            alumni_ucarpooling_id = alumni['ucarpoolingprofile_id']
            alumni_useritinerary_id = alumni['useritinerary_id']

            "GET the matches for the alumni"
            with Chronometer() as time_matching:
                response = requests.get(
                    url=get_matcher_url(alumni_useritinerary_id),
                    headers={
                        "Authorization": f'Token {alumni_token}'
                    }
                )

            """Time statistics for the matcher of the back-end"""
            match_time = float(time_matching)
            helper.detail_message('Match for {} took {:.3f} seconds'.format(alumni_id, match_time))
            total_time += match_time
            max_time = match_time if max_time < match_time else max_time

            if response.status_code == 200:
                body_response = response.json()
                partners = get_carpooling_partner(body_response)
                if partners:
                    create_carpool(alumni_ucarpooling_id, partners, alumni_useritinerary_id)
                else:
                    helper.warning_message(f'{alumni_id} had matches but did not travel with poolers')
            else:
                """The server did not respond a good result"""
                total_errors += 1
                if response.status_code == 420:
                    helper.warning_message(f'{alumni_id} is already in a carpool')
                elif response.status_code == 204:
                    helper.no_matches_message(f'{alumni_id} did not have any matches')
                else:

                    helper.error_message(f'Error getting matches for alumni {alumni_id} '
                                         f'---- status code: {response.status_code}: {response.reason}')

        """The simulation ended"""
        helper.info_message('=================SIMULATION ENDED=====================')
        helper.detail_message(f'There was a total of {total_errors} errors')
        helper.detail_message(f'Max total match time: {max_time} seconds')
        helper.detail_message('Simulation runtime: {:.3f} seconds'.format(float(time_simulation)))



if __name__ == "__main__":
    simulator()


