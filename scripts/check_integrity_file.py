import datetime
import csv

from scripts import settings
from scripts import helper

def check_fields_null(alumni):
    """Check if any field is null"""

    if not alumni[settings.FIELDNAME_LATITUDE] or not alumni[settings.FIELDNAME_LONGITUDE]:
        return True
    else:
        return False


def check_repeated_row(uuid, uuid_rows):
    """Check if there are any repeated record in the source file"""

    if (uuid in uuid_rows):
        return True
    else:
        uuid_rows.append(uuid)
        return False


def check_bounds(latitude, longitude):
    """Checks if the row is inside useful bounds"""

    if -25.084644 > latitude > -25.541974 and -57.325033 > longitude > -57.680855:
        return True
    else:
        return False

def check_congruent_times(time_of_arrival, time_of_departure):
    """Checks if the time of the arrival is earlier that the departure"""

    TimeDifference = time_of_departure - time_of_arrival

    if (TimeDifference.days < 0):
        return False
    else:
        return True


def check_sapientia_file():
    """Checks the integrity of the source sapientia .csv file"""

    print("---------------CHECKING SAPIENTIA FILES---------------------")
    alumni = {}

    uuid_rows = []

    file_integrated = True

    with open(settings.CSV_USERDATA_INPUT_FILE_PATH, newline='', encoding='utf-8') as csv_input_userdata:

        row_reader = csv.DictReader(csv_input_userdata, delimiter=';')

        for row in row_reader:

            """The current alumni being read from the original CSV"""
            alumni = helper.get_alumni_sapientia(row)

            if (check_fields_null(alumni) == True):
                file_integrated = False

                print(str(alumni[settings.FIELDNAME_UUID]) + " has null fields")

            if (check_bounds(alumni[settings.FIELDNAME_LATITUDE], alumni[settings.FIELDNAME_LONGITUDE]) == False):

                file_integrated = False

                print(str(alumni[settings.FIELDNAME_UUID]) + " is outside of bounds")

            if (check_repeated_row(alumni[settings.FIELDNAME_UUID], uuid_rows) == True):

                file_integrated = False

                print(str(alumni[settings.FIELDNAME_UUID]) + " record is repeated")


    if (file_integrated):
        print("The sapientia file has no problems and is ready to be proccessed")


def check_form_file():
    """Checks the integrity of the source form .csv file"""
    print("---------------CHECKING FORM FILES---------------------")


    alumni = {}

    uuid_rows = []

    file_integrated = True

    with open(settings.CSV_FORMDATA_INPUT_FILE_PATH, newline='', encoding='utf-8') as csv_input_userdata:

        row_reader = csv.DictReader(csv_input_userdata, delimiter=',')

        for row in row_reader:

            """The current alumni being read from the CSV"""

            alumni = helper.get_alumni_form(row)

            if (check_congruent_times(alumni[settings.FIELDNAME_TOA], alumni[settings.FIELDNAME_TOD]) == False):

                file_integrated = False

                print(alumni[settings.FIELDNAME_UUID] + " has incongruent time")

    if (file_integrated):
        print("The form file has no problems and is ready to be proccessed")


if __name__ == "__main__":

    check_sapientia_file()

    check_form_file()



