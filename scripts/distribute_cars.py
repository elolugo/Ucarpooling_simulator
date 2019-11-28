import csv
import random

from scripts import settings
from scripts import helper

def distribute_mean_transportation():

    """Count how many cars and the percentage of the total"""
    with open(settings.CSV_FORMDATA_INPUT_FILE_PATH, newline='', encoding='ascii', errors='ignore') as csv_input_formdata:

        row_reader = csv.DictReader(csv_input_formdata, delimiter=settings.FORM_DELIMITER)

        car_count = 0
        not_car_count= 0

        for row in row_reader:  # For each row in the original CSV

            alumni = helper.get_alumni_form(row)
            mean_transportation = alumni[settings.FIELDNAME_TRANSPORT]
            if (mean_transportation == 'Car'):
                car_count = car_count + 1
            else:
                not_car_count = not_car_count + 1

        car_ownership_percentage = car_count / (car_count+not_car_count)
        not_car_ownership_percentage = 1 - car_ownership_percentage
        print(f'Hay {car_count+not_car_count} personas en el registro')
        print(f'Hay {car_count} personas que tienen auto contando con el {car_ownership_percentage*100}%')
        print(f'Hay {not_car_count} personas que no tienen auto contando con el {not_car_ownership_percentage*100}%')

    """Count how many rows are to be assigned"""
    with open(settings.CSV_USERDATA_INPUT_FILE_PATH, newline='', encoding='utf-8') as csv_input_userdata:

        row_reader = csv.DictReader(csv_input_userdata, delimiter=settings.SAPIENTIA_DELIMITER)

        total_rows = 0
        for row in row_reader:  # For each row in the original CSV
            total_rows = total_rows + 1

    """Distribute the car and not car ownership"""
    with open(settings.CSV_USERDATA_INPUT_FILE_PATH, newline='', encoding='utf-8') as csv_input_userdata, \
         open(settings.CSV_OUTPUT_FILE_PATH, 'w', newline='', encoding='utf-8') as csv_output_file:

        row_reader = csv.DictReader(csv_input_userdata, delimiter=settings.OUTPUT_FILES_DELIMITER)

        """Writing the headers of the output file"""
        output_csv_fieldnames = row_reader.fieldnames
        output_csv_fieldnames.append(settings.FIELDNAME_TRANSPORT)
        output_csv_writer = csv.DictWriter(csv_output_file, fieldnames=output_csv_fieldnames, delimiter=';')
        output_csv_writer.writeheader()

        total_cars = 0

        for row in row_reader:  # For each row in the original CSV

            alumni = helper.get_alumni_sapientia(row)


            # Random assign according to distribution
            if random.random() <= car_ownership_percentage:
                # it has a car
                total_cars = total_cars + 1

                alumni[settings.FIELDNAME_TRANSPORT] = 'Car'

            else:

                alumni[settings.FIELDNAME_TRANSPORT] = 'No Car'

            output_csv_writer.writerow(alumni)

        print(f'EN TOTAL DE {total_rows}, {total_cars} TINEN AUTO QUE CONSTA EL {(total_cars/total_rows)*100}%')


if __name__ == "__main__":
    distribute_mean_transportation()



