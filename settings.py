import os


ASSIGN_PERSONALITY_DIRECTORY = 'assign_personality'
PROJECT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

SOURCE_DIRECTORY = 'source_data'
OUTPUT_DIRECTORY = 'output_data'


CSV_FORMDATA_INPUT_FILE_PATH = os.path.join(
    PROJECT_DIRECTORY,
    ASSIGN_PERSONALITY_DIRECTORY,
    SOURCE_DIRECTORY,
    'Form_data.csv'
)
FORM_DELIMITER = ','
FORM_FILE_ENCODING = 'utf-8'

CSV_USERDATA_INPUT_FILE_PATH = os.path.join(
    PROJECT_DIRECTORY,
    ASSIGN_PERSONALITY_DIRECTORY,
    SOURCE_DIRECTORY,
    'Sapientia_data.csv'
)
SAPIENTIA_DELIMITER = ';'
SAPIENTIA_FILE_ENCODING = 'utf-8-sig'


"""Assigned files path"""
OUTPUT_FILES_DELIMITER = ';'
OUTPUT_FILES_ENCODING = 'utf-8'
CSV_OUTPUT_TRANSPORT_FILE_PATH = os.path.join(
    PROJECT_DIRECTORY,
    ASSIGN_PERSONALITY_DIRECTORY,
    OUTPUT_DIRECTORY,
    'Alumnos_profiles_car_ownership.csv'
)
CSV_OUTPUT_SMOKER_FILE_PATH = os.path.join(
    PROJECT_DIRECTORY,
    ASSIGN_PERSONALITY_DIRECTORY,
    OUTPUT_DIRECTORY,
    'Alumnos_profiles_smoker.csv'
)
CSV_OUTPUT_ELOQUENCE_FILE_PATH = os.path.join(
    PROJECT_DIRECTORY,
    ASSIGN_PERSONALITY_DIRECTORY,
    OUTPUT_DIRECTORY,
    'Alumnos_profiles_eloquence.csv'
)
CSV_OUTPUT_MUSIC_TASTE_FILE_PATH = os.path.join(
    PROJECT_DIRECTORY,
    ASSIGN_PERSONALITY_DIRECTORY,
    OUTPUT_DIRECTORY,
    'Alumnos_profiles_music_taste.csv'
)
CSV_OUTPUT_ITINERARY_FILE_PATH = os.path.join(
    PROJECT_DIRECTORY,
    ASSIGN_PERSONALITY_DIRECTORY,
    OUTPUT_DIRECTORY,
    'Alumnos_profiles_itinerary.csv'
)


"""Field names"""
FIELDNAME_UUID = 'UUID'
FIELDNAME_CAREER = 'CAREER'
FIELDNAME_SEX = 'SEX'
FIELDNAME_ADDRESS = 'ADDRESS'
FIELDNAME_LATITUDE = 'LATITUDE'
FIELDNAME_LONGITUDE = 'LONGITUDE'
FIELDNAME_TRANSPORT = 'TRANSPORT'
FIELDNAME_TOA = 'TIME_OF_ARRIVAL'
FIELDNAME_TOD = 'TIME_OF_DEPARTURE'
FIELDNAME_SMOKER = 'SMOKER'
FIELDNAME_ELOQUENCE = 'ELOQUENCE_LEVEL'
FIELDNAME_MUSIC_TASTE = 'MUSIC'