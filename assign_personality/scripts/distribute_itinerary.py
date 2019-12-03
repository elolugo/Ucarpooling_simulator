import csv
import random

import settings
import helper


def distribute_itinerary():
    """
    Check the distribution of time of arrival and time of departure for every career of the form data.
    Apply that distribution to the sapientia data according to the career
    """

    print('=========================DISTRIBUTING ITINERARY=========================')

    careers = {}

    """Count the different careers"""
    with open(settings.CSV_FORMDATA_INPUT_FILE_PATH, newline='', encoding=settings.FORM_FILE_ENCODING,
              errors='ignore') as csv_input_formdata:

        row_reader = csv.DictReader(csv_input_formdata, delimiter=settings.FORM_DELIMITER)

        for row in row_reader:  # For each row in the original CSV

            alumni = helper.get_alumni_form(row)

            career = alumni[settings.FIELDNAME_CAREER]

            if career in careers:
                careers[career] = careers[career] + 1
            else:
                careers[career] = 1



    """Count the itineraries per career"""
    print("---------------------------------FORM DATA----------------------------------------")
    distribution = {}

    for career in careers:  # For each career

        with open(settings.CSV_FORMDATA_INPUT_FILE_PATH, newline='', encoding=settings.FORM_FILE_ENCODING,
                  errors='ignore') as csv_input_formdata:

            row_reader = csv.DictReader(csv_input_formdata, delimiter=settings.FORM_DELIMITER)

            distribution[career] = {}

            total_records = 0

            for row in row_reader:  # For each row in the original CSV

                alumni = helper.get_alumni_form(row)

                if alumni[settings.FIELDNAME_CAREER] == career:
                    total_records = total_records + 1

                    record_value = (alumni[settings.FIELDNAME_TOA], alumni[settings.FIELDNAME_TOD])

                    if record_value in distribution[career]:
                        distribution[career][record_value] = distribution[career][record_value] + 1
                    else:
                        distribution[career][record_value] = 1

            # Printing the results
            print(f'total records for {career}: {total_records}')
            for key in distribution[career]:
                count = distribution[career][key]
                distribution[career][key] = {
                    'count': count,
                    'percentage': count / total_records
                }



    """Calculating the range for each itinerary"""

    for career in careers:  # For each career
        career_itineraries = distribution[career]
        ordered_options = sorted(career_itineraries.items(), key=lambda kv: kv[1]['count'], reverse=False)

        # Assign range for distribution
        min = 0
        max = 0
        for item in ordered_options:
            item_percentage = item[1]['percentage']
            min = max
            max = min + item_percentage

            option = item[0]
            distribution[career][option]['min'] = min
            distribution[career][option]['max'] = max



    """Applying the distribution to the sapientia data"""

    with open(
            settings.CSV_USERDATA_INPUT_FILE_PATH,
            newline='',
            encoding=settings.SAPIENTIA_FILE_ENCODING,
            errors='ignore') as csv_input_userdata, \
            open(
                settings.CSV_OUTPUT_ITINERARY_FILE_PATH,
                'w', newline='',
                encoding=settings.OUTPUT_FILES_ENCODING) as csv_output_file:

        row_reader = csv.DictReader(csv_input_userdata, delimiter=settings.OUTPUT_FILES_DELIMITER)

        """Writing the headers of the output file"""
        output_csv_fieldnames = row_reader.fieldnames
        output_csv_fieldnames.append(settings.FIELDNAME_TOA)
        output_csv_fieldnames.append(settings.FIELDNAME_TOD)
        output_csv_writer = csv.DictWriter(csv_output_file, fieldnames=output_csv_fieldnames, delimiter=';')
        output_csv_writer.writeheader()

        for row in row_reader:  # For each row in the original CSV

            alumni = helper.get_alumni_sapientia(row)

            alumni_career = alumni[settings.FIELDNAME_CAREER]

            career_itineraries = distribution[alumni_career]

            # Generating random value from 0 to 1
            random_value = random.random()

            for option in career_itineraries:

                if career_itineraries[option]['min'] < random_value <= career_itineraries[option]['max']:

                    alumni[settings.FIELDNAME_TOA] = option[0].time().strftime('%H:%M:%S')
                    alumni[settings.FIELDNAME_TOD] = option[1].time().strftime('%H:%M:%S')

                    output_csv_writer.writerow(alumni)
                    break

            # If it didnt enter in the if clause
            alumni[settings.FIELDNAME_TOA] = option[0].time().strftime('%H:%M:%S')
            alumni[settings.FIELDNAME_TOD] = option[1].time().strftime('%H:%M:%S')

            output_csv_writer.writerow(alumni)

    print("=================================================")
    print("Finished distributing itineraries")

if __name__ == "__main__":
    distribute_itinerary()
