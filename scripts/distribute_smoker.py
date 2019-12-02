import csv

from scripts import settings
from scripts import helper

def distribute_smoker():

    """Count how many cars and the percentage of the total"""
    with open(settings.CSV_FORMDATA_INPUT_FILE_PATH, newline='', encoding='ascii', errors='ignore') as csv_input_formdata:

        row_reader = csv.DictReader(csv_input_formdata, delimiter=settings.FORM_DELIMITER)

        total_records_form, smoker_distribution = helper.count_distribution(settings.FIELDNAME_SMOKER, row_reader)

    """Assign the range of probability for each option of values"""
    helper.calculate_range_distribution(smoker_distribution)

    """Distribute the car and not car ownership"""
    with open(settings.CSV_USERDATA_INPUT_FILE_PATH, newline='', encoding='utf-8') as csv_input_userdata, \
         open(settings.CSV_OUTPUT_SMOKER_FILE_PATH, 'w', newline='', encoding='utf-8') as csv_output_file:

        row_reader = csv.DictReader(csv_input_userdata, delimiter=settings.OUTPUT_FILES_DELIMITER)

        """Writing the headers of the output file"""
        output_csv_fieldnames = row_reader.fieldnames
        output_csv_fieldnames.append(settings.FIELDNAME_SMOKER)
        output_csv_writer = csv.DictWriter(csv_output_file, fieldnames=output_csv_fieldnames, delimiter=';')
        output_csv_writer.writeheader()

        """Actually apply the calculated distribution to the data"""
        helper.assign_distribution_to_alumni_data(
            row_reader=row_reader,
            csv_writer=output_csv_writer,
            distribution=smoker_distribution,
            column=settings.FIELDNAME_SMOKER
        )


if __name__ == "__main__":
    distribute_smoker()
