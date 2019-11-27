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
    distribute_mean_transportation()



