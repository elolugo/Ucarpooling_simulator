import requests
import json
import csv
import sys
import os
import shutil
import googlemaps
from datetime import datetime


CURRENT_DIRECTORY = os.getcwd()
CSV_FORMDATA_INPUT_FILE_PATH = "source_data\Formulario.csv"
CSV_USERDATA_INPUT_FILE_PATH = "source_data\Alumnos_Campus_Geocoded.csv"
CSV_OUTPUT_FILE_PATH = "output_data\Alumnos_profiles.csv"


def clean():

    """ Limpia los archivos de las coordenadas que estan fuera de Asuncion"""
    path = os.path.join(CURRENT_DIRECTORY, CSV_USERDATA_INPUT_FILE_PATH)

    with open(CSV_FORMDATA_INPUT_FILE_PATH, newline='', encoding='utf-8') as csv_input_formdata, \
         open(CSV_USERDATA_INPUT_FILE_PATH, newline='', encoding='utf-8') as csv_input_userdata, \
         open(CSV_OUTPUT_FILE_PATH, 'w', newline='', encoding='utf-8') as csv_output_file:

        row_reader = csv.DictReader(csv_input_userdata, delimiter=';')

        # preparing the csv file for success geocoding rows
        fieldnames = ['UUID', 'SEXO', 'CARRERA', 'DIRECCION', 'LONGITUD', 'LATITUD']
        output_csv_writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames, delimiter=';')
        output_csv_writer.writeheader()

        nopy = 0
        py = 0

        for row in row_reader:  # For each row in the original CSV

            alumni_uuid = row['UUID']
            alumni_sex = row['SEXO']
            alumni_career = row['CARRERA']
            alumni_address = row['DIRECCION']
            alumni_longitude = float(row['LONGITUD'])
            alumni_latitude = float(row['LATITUD'])

            if -25.084644 > alumni_latitude > -25.541974 and -57.325033 > alumni_longitude > -57.680855:
                print(f'{alumni_uuid} esta en py')
                py=py+1

                output_csv_writer.writerow(
                    {
                    'UUID': alumni_uuid,
                    'SEXO': alumni_sex,
                    'CARRERA': alumni_career,
                    'DIRECCION': alumni_address,
                    'LATITUD': alumni_longitude,
                    'LONGITUD': alumni_latitude
                    }
                )

            else:
                print(f'{alumni_uuid} NO esta en py')
                nopy = nopy + 1

        print(f'En Paraguay estan {py} personas')
        print(f'No estan en Py {nopy} personas')

def distribute_mean_transportation():

    with open(CSV_FORMDATA_INPUT_FILE_PATH, newline='', encoding='utf-8') as csv_input_formdata, \
         open(CSV_USERDATA_INPUT_FILE_PATH, newline='', encoding='utf-8') as csv_input_userdata, \
         open(CSV_OUTPUT_FILE_PATH, 'w', newline='', encoding='utf-8') as csv_output_file:

        row_reader = csv.DictReader(csv_input, delimiter=';')

        #preparing the csv file for success geocoding rows
        fieldnames = ['UUID','SEXO','CARRERA','DIRECCION','LATITUD','LONGITUD']
        output_csv_writer = csv.DictWriter(csv_output, fieldnames=fieldnames, delimiter=';')
        output_csv_writer.writeheader()

        # preparing the csv file for failed geocoding rows
        fieldnames = ['UUID', 'SEXO', 'CARRERA', 'DIRECCION']
        output_failed_csv_writer = csv.DictWriter(csv_output_failed, fieldnames=fieldnames, delimiter=';')
        output_failed_csv_writer.writeheader()


        for row in row_reader: #For each row in the original CSV

            alumni_uuid = row['UUID']
            alumni_sex = row['SEXO']
            alumni_career = row['CARRERA']
            alumni_address = row['DIRECCION']


            if(alumni_address[0]=='-'):#check if it has latitude and longitude already
                # Geocoded already
                print(alumni_uuid + " Geocoded already")

                #get the latitude and longitude
                latitudeAndLongitude = alumni_address.split(',')

                json_dict = {
                    'UUID': alumni_uuid,
                    'SEXO': alumni_sex,
                    'CARRERA': alumni_career,
                    'DIRECCION': "Geocoded Address",
                    'LATITUD': latitudeAndLongitude[0],
                    'LONGITUD': latitudeAndLongitude[1].strip()
                }
                output_csv_writer.writerow(json_dict)

            else: # Not Geocoded already

                #Google API query
                geocode_result = gmaps.geocode(alumni_address)

                if not geocode_result:  # Check if the Geocode response is empty
                    # Geocode response is empty
                    print(alumni_uuid + " Geocode does not exist")
                    # save into failed csv

                    json_dict = {
                        'UUID': alumni_uuid,
                        'SEXO': alumni_sex,
                        'CARRERA': alumni_career,
                        'DIRECCION': alumni_address
                    }

                    #write into the failed address csv file
                    output_failed_csv_writer.writerow(json_dict)

                else:
                    # Geocode response is not empty
                    print(alumni_uuid + " Geocode does exist")


                    # save into output csv
                    latitude = geocode_result[0]['geometry']['location']['lat']
                    longitude = geocode_result[0]['geometry']['location']['lng']

                    json_dict = {
                        'UUID': alumni_uuid,
                        'SEXO': alumni_sex,
                        'CARRERA': alumni_career,
                        'DIRECCION': alumni_address,
                        'LATITUD': latitude,
                        'LONGITUD': longitude
                    }

                    output_csv_writer.writerow(json_dict)


                    # save into json list
                    json_dict = {
                        'UUID': alumni_uuid,
                        'SEXO': alumni_sex,
                        'CARRERA': alumni_career,
                        'RESPONSE': geocode_result[0]
                    }
                    json_responses_list.append(json_dict)

        #Dump all the json responses in a json file
        json.dump(json_responses_list, json_output, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    clean()