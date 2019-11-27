import csv

import os



PROJECT_DIRECTORY = os.path.dirname(os.getcwd())

SOURCE_DIRECTORY = 'source_data'

CSV_USERDATA_INPUT_FILE_PATH = os.path.join(PROJECT_DIRECTORY, SOURCE_DIRECTORY, 'Alumnos_Campus_Geocoded.csv')


def check_fields_null(alumni):
    """Check if any field is null"""

    if not alumni['latitude'] or not alumni['longitude']:
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


def check_file():
    """Checks the integrity of the source .csv file"""
    alumni = {}

    uuid_rows = []

    file_integrated = True

    with open(CSV_USERDATA_INPUT_FILE_PATH, newline='', encoding='utf-8') as csv_input_userdata:

        row_reader = csv.DictReader(csv_input_userdata, delimiter=';')

        for row in row_reader:

            """The current alumni being read from the original CSV"""
            alumni = {
                'uuid': row['UUID'],
                'sex': row['SEXO'],
                'career': row['CARRERA'],
                'address': row['DIRECCION'],
                'latitude': float(row['LATITUD']),
                'longitude': float(row['LONGITUD']),
            }

            if (check_fields_null(alumni) == True):
                file_integrated = False

                print(str(alumni['uuid']) + " has null fields")

            if (check_bounds(alumni['latitude'], alumni['longitude']) == False):

                file_integrated = False

                print(str(alumni['uuid']) + " is outside of bounds")

            if (check_repeated_row(alumni['uuid'], uuid_rows) == True):

                file_integrated = False

                print(str(alumni['uuid']) + " record is repeated")

    if (file_integrated):
        print("The file has no problems and is ready to be proccessed")



if __name__ == "__main__":

    check_file()



