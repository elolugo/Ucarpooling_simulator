import csv
import sys
import os
import random


PROJECT_DIRECTORY = os.path.dirname(os.getcwd())


SOURCE_DIRECTORY = 'source_data'
OUTPUT_DIRECTORY = 'output_data'


CSV_FORMDATA_INPUT_FILE_PATH = os.path.join(PROJECT_DIRECTORY, SOURCE_DIRECTORY, 'Formulario.csv')
CSV_USERDATA_INPUT_FILE_PATH = os.path.join(PROJECT_DIRECTORY, SOURCE_DIRECTORY, 'Alumnos_Campus_Geocoded.csv')
CSV_OUTPUT_FILE_PATH = os.path.join(PROJECT_DIRECTORY, OUTPUT_DIRECTORY, 'Alumnos_profiles_car_ownership.csv')


def distribute_mean_transportation():

    """Count how many cars and the percentage of the total"""
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
        print(f'Hay {car_count} personas que tienen auto contando con el {car_ownership_percentage*100}%')
        print(f'Hay {not_car_count} personas que no tienen auto contando con el {not_car_ownership_percentage*100}%')

    """Count how many rows are to be assigned"""
    with open(CSV_USERDATA_INPUT_FILE_PATH, newline='', encoding='utf-8') as csv_input_userdata:

        row_reader = csv.DictReader(csv_input_userdata, delimiter=';')

        total_rows = 0
        for row in row_reader:  # For each row in the original CSV
            total_rows = total_rows + 1

    """Distribute the car and not car ownership"""
    with open(CSV_USERDATA_INPUT_FILE_PATH, newline='', encoding='utf-8') as csv_input_userdata, \
         open(CSV_OUTPUT_FILE_PATH, 'w', newline='', encoding='utf-8') as csv_output_file:

        row_reader = csv.DictReader(csv_input_userdata, delimiter=';')

        """Writing the headers of the output file"""
        output_csv_fieldnames = row_reader.fieldnames
        output_csv_fieldnames.append('MEANS_TRANSPORTATION')
        output_csv_writer = csv.DictWriter(csv_output_file, fieldnames=output_csv_fieldnames, delimiter=';')
        output_csv_writer.writeheader()

        total_cars = 0

        for row in row_reader:  # For each row in the original CSV

            alumni = {
                'UUID': row['UUID'],
                'SEXO': row['SEXO'],
                'CARRERA': row['CARRERA'],
                'DIRECCION': row['DIRECCION'],
                'LATITUD': float(row['LATITUD']),
                'LONGITUD': float(row['LONGITUD']),
                'MEANS_TRANSPORTATION': 'NULL'
            }

            # Random assign according to distribution
            if random.random() <= car_ownership_percentage:
                # it has a car
                total_cars = total_cars + 1

                alumni['MEANS_TRANSPORTATION'] = 'Car'

            else:

                alumni['MEANS_TRANSPORTATION'] = 'No Car'

            output_csv_writer.writerow(alumni)

        print(f'EN TOTAL DE {total_rows}, {total_cars} TINEN AUTO QUE CONSTA EL {(total_cars/total_rows)*100}%')


if __name__ == "__main__":
    distribute_mean_transportation()



