import requests

import sqlite3
from sqlite3 import Error

from pypika import Query, Table

import settings
import helper


def get_eloquence_level(eloquence_in_string):
    """Converts from string into integer"""
    if eloquence_in_string == "Extrovertido":
        return 3
    elif eloquence_in_string == "Medio":
        return 2
    else:
        return 1

def get_token(con, cursorObj, alumni):
    """Get the tokens for each alumni created"""

    """Building the body in a json-like format for the boy of the POST request"""
    body = {
        "username": f"{alumni[settings.FIELDNAME_UUID.lower()]}@mail.com",
        "password": "12345678"
    }

    "POST the alumni data to the API"
    response = requests.post(
        settings.AUTH_TOKEN_URL,
        json=body,
        headers={
            "Authorization": f'Token {settings.UCARPOOLING_APP_TOKEN}'  # Token of the Ucarpooling app
        }
    )

    body_response = response.json()

    alumni_auth = Table(settings.DATABASE_TABLE_AUTH)

    querystring = Query.into(alumni_auth).insert(
        alumni[settings.FIELDNAME_UUID.lower()],  # uuid
        body_response['ucarpoolingrofile'],  # ucprofile
        body_response['token']  # token
    )

    cursorObj.execute(querystring.get_sql())
    con.commit()


def create_auth_database():
    """Create the database for storing tokens and ids"""

    try:
        con = sqlite3.connect(settings.DATABASE)
        con.row_factory = sqlite3.Row

        cursorObj = con.cursor()
        cursorObj.execute('drop table if exists ' + settings.DATABASE_TABLE_AUTH)
        cursorObj.execute(
            "CREATE TABLE " + settings.DATABASE_TABLE_AUTH + "(uuid integer PRIMARY KEY, ucarpoolingprofile_id text, token text)")
        con.commit()
        helper.warning_message("Created auth database")


    except Error:

        print(Error)


def upload_users():
    """
    Uploads all the generated users profile to api/ucarpooling/users/
    """

    try:
        con = sqlite3.connect(settings.DATABASE)
        con.row_factory = sqlite3.Row

        cursorObj = con.cursor()

        """Building the query for retrieving all the users and their assigned profiles"""
        querystring = Query \
            .from_(Table(settings.DATABASE_TABLE_ALUMNI)) \
            .join(Table(settings.DATABASE_TABLE_ELOQUENCE)) \
            .on_field('uuid') \
            .join(Table(settings.DATABASE_TABLE_SMOKER)) \
            .on_field('uuid') \
            .join(Table(settings.DATABASE_TABLE_MUSIC)) \
            .on_field('uuid') \
            .select('*')\
            .limit(20)

        """Executing the query"""
        rows = cursorObj.execute(querystring.get_sql()).fetchall()

        """Iteraring for each row in the database for alumni"""
        for alumni in rows:


            """Building the body in a json-like format for the boy of the POST request"""
            body = {
                "email": f"{alumni[settings.FIELDNAME_UUID.lower()]}@mail.com",
                "password": "12345678",
                "first_name": str(alumni[settings.FIELDNAME_UUID.lower()]),
                "last_name": str(alumni[settings.FIELDNAME_UUID.lower()]),
                "ucarpoolingprofile": {
                    "sex": alumni[settings.FIELDNAME_SEX.lower()],
                    "smoker": True if alumni[settings.FIELDNAME_SMOKER.lower()] == 'Si' else False,
                    "musicTaste": alumni[settings.FIELDNAME_MUSIC_TASTE.lower()].split(", "),
                    "eloquenceLevel": get_eloquence_level(alumni[settings.FIELDNAME_ELOQUENCE.lower()])
                }
            }

            "POST the alumni data to the API"
            response = requests.post(
                settings.USER_URL,
                json=body,
                headers={
                    "Authorization": f'Token {settings.UCARPOOLING_APP_TOKEN}'  # Token of the Ucarpooling app
                }
            )

            if response.status_code == 201:
                helper.success_message(f'Uploaded successfully alumni {alumni[settings.FIELDNAME_UUID.lower()]}')

                get_token(con, cursorObj, alumni)

            else:
                helper.error_message(f'Error uploading alumni {alumni[settings.FIELDNAME_UUID.lower()]} '
                                     f'---- status code: {response.status_code}: {response.reason}')

    except Error:

        print(Error)

    finally:

        """Closing the database connection"""
        con.close()


if __name__ == "__main__":
    create_auth_database()
    upload_users()


