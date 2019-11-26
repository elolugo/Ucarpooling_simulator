import csv
import sys
import os
import random


CURRENT_DIRECTORY = os.getcwd()
CSV_FORMDATA_INPUT_FILE_PATH = "source_data\Formulario.csv"
CSV_USERDATA_INPUT_FILE_PATH = "source_data\Alumnos_Campus_Geocoded.csv"
CSV_OUTPUT_FILE_PATH = "output_data\Alumnos_profiles_car_ownership.csv"
CSV_CLEANED_FILE_PATH = "output_data\Alumnos_Campus_Geocoded_CLEANED.csv"


def clean():

    """ Limpia los archivos de las coordenadas que estan fuera de Asuncion"""

    with open(CSV_USERDATA_INPUT_FILE_PATH, newline='', encoding='utf-8') as csv_input_userdata, \
         open(CSV_CLEANED_FILE_PATH, 'w', newline='', encoding='utf-8') as csv_output_file:

        row_reader = csv.DictReader(csv_input_userdata, delimiter=';')

        # preparing the csv file for success geocoding rows
        fieldnames = ['UUID', 'SEXO', 'CARRERA', 'DIRECCION', 'LATITUD', 'LONGITUD']
        output_csv_writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames, delimiter=';')
        output_csv_writer.writeheader()

        nopy = 0
        py = 0

        for row in row_reader:  # For each row in the original CSV

            alumni_uuid = row['UUID']
            alumni_sex = row['SEXO']
            alumni_career = row['CARRERA']
            alumni_address = row['DIRECCION']
            alumni_latitude = float(row['LATITUD'])
            alumni_longitude = float(row['LONGITUD'])


            if -25.084644 > alumni_latitude > -25.541974 and -57.325033 > alumni_longitude > -57.680855:
                print(f'{alumni_uuid} esta en py')
                py=py+1

                output_csv_writer.writerow(
                    {
                    'UUID': alumni_uuid,
                    'SEXO': alumni_sex,
                    'CARRERA': alumni_career,
                    'DIRECCION': alumni_address,
                    'LATITUD': alumni_latitude,
                    'LONGITUD': alumni_longitude
                    }
                )

            else:
                print(f'{alumni_uuid} NO esta en py')
                nopy = nopy + 1

        print(f'En Paraguay estan {py} personas')
        print(f'No estan en Py {nopy} personas')




def distribute_mean_transportation():

    with open(CSV_FORMDATA_INPUT_FILE_PATH, newline='', encoding='ascii', errors='ignore') as csv_input_formdata:

        row_reader = csv.DictReader(csv_input_formdata, delimiter=';')

        car_count = 0
        not_car_count= 0

        for row in row_reader:  # For each row in the original CSV
            mean_transportation = row['MODO_TRANSPORTE']
            if (mean_transportation == 'Manejo en auto'):
                car_count = car_count + 1
            elif (mean_transportation == 'Me traen en auto'):
                car_count = car_count + 1
            else:
                not_car_count = not_car_count + 1

        car_ownership_percentage = car_count / (car_count+not_car_count)
        not_car_ownership_percentage = 1 - car_ownership_percentage
        print(f'Hay {car_count+not_car_count} personas en el registro')
        print(f'Hay {car_count} personas que tienen auto contando con el {car_ownership_percentage*100}')
        print(f'Hay {not_car_count} personas que no tienen auto contando con el {not_car_ownership_percentage*100}')

    """Distribute the car and not car ownership"""
    with open(CSV_USERDATA_INPUT_FILE_PATH, newline='', encoding='utf-8') as csv_input_userdata, \
         open(CSV_OUTPUT_FILE_PATH, 'w', newline='', encoding='utf-8') as csv_output_file:


        row_reader = csv.DictReader(csv_input_userdata, delimiter=';')

        """Writing the headers of the output file"""
        fieldnames = ['UUID', 'MEANS_TRANSPORTATION']
        output_csv_writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames, delimiter=';')
        output_csv_writer.writeheader()

        total_cars = 0
        total_rows = 0
        for row in row_reader:  # For each row in the original CSV
            total_rows = total_rows + 1
            alumni_uuid = row['UUID']

            # Random assign according to distribution
            if random.random() <= car_ownership_percentage:
                # it has a car
                total_cars = total_cars + 1

                output_csv_writer.writerow(
                    {
                        'UUID': alumni_uuid,
                        'MEANS_TRANSPORTATION': 'Car',
                    }
                )

            else:

                output_csv_writer.writerow(
                    {
                        'UUID': alumni_uuid,
                        'MEANS_TRANSPORTATION': 'No car',
                    }
                )

        print(f'EN TOTAL DE {total_rows}, {total_cars} TINEN AUTO QUE CONSTA EL {(total_cars/total_rows)*100}%')


if __name__ == "__main__":
    #clean()
    distribute_mean_transportation()



