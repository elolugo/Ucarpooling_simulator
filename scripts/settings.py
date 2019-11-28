import os

PROJECT_DIRECTORY = os.path.dirname(os.getcwd())


SOURCE_DIRECTORY = 'source_data'
OUTPUT_DIRECTORY = 'output_data'


CSV_FORMDATA_INPUT_FILE_PATH = os.path.join(PROJECT_DIRECTORY, SOURCE_DIRECTORY, 'Formulario.csv')
CSV_USERDATA_INPUT_FILE_PATH = os.path.join(PROJECT_DIRECTORY, SOURCE_DIRECTORY, 'Alumnos_Campus_Geocoded.csv')
CSV_OUTPUT_FILE_PATH = os.path.join(PROJECT_DIRECTORY, OUTPUT_DIRECTORY, 'Alumnos_profiles_car_ownership.csv')