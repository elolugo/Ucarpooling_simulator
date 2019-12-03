import csv

import settings
import helper


def distribute_eloquence():

    print('=========================DISTRIBUTING ELOQUENCE=========================')

    """Count how many cars and the percentage of the total"""
    with open(settings.CSV_FORMDATA_INPUT_FILE_PATH, newline='', encoding=settings.FORM_FILE_ENCODING, errors='ignore') as csv_input_formdata:

        row_reader = csv.DictReader(csv_input_formdata, delimiter=settings.FORM_DELIMITER)

        total_records_form, eloquence_distribution = helper.count_distribution(settings.FIELDNAME_ELOQUENCE, row_reader)

    """Assign the range of probability for each option of values"""
    helper.calculate_range_distribution(eloquence_distribution)

    """Distribute the car and not car ownership"""
    with open(settings.CSV_USERDATA_INPUT_FILE_PATH, newline='', encoding=settings.SAPIENTIA_FILE_ENCODING) as csv_input_userdata, \
         open(settings.CSV_ASSIGNED_ELOQUENCE_FILE_PATH, 'w', newline='', encoding=settings.ASSIGNED_FILES_ENCODING) as csv_output_file:

        row_reader = csv.DictReader(csv_input_userdata, delimiter=settings.ASSIGNED_FILES_DELIMITER)

        """Writing the headers of the output file"""
        output_csv_fieldnames = row_reader.fieldnames
        output_csv_fieldnames.append(settings.FIELDNAME_ELOQUENCE)
        output_csv_writer = csv.DictWriter(csv_output_file, fieldnames=output_csv_fieldnames, delimiter=settings.ASSIGNED_FILES_DELIMITER)
        output_csv_writer.writeheader()

        """Actually apply the calculated distribution to the data"""
        helper.assign_distribution_to_alumni_data(
            row_reader=row_reader,
            csv_writer=output_csv_writer,
            distribution=eloquence_distribution,
            column=settings.FIELDNAME_ELOQUENCE
        )


if __name__ == "__main__":
    distribute_eloquence()
