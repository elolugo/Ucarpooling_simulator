import requests
import csv
import json

import settings
import helper



URL = 'https://api.github.com'

def upload_users():


    with open(settings.CSV_ASSIGNED_SMOKER_FILE_PATH,
              newline='',
              encoding=settings.ASSIGNED_FILES_ENCODING) as profile_smoker:

        row_reader = csv.DictReader(profile_smoker, delimiter=settings.ASSIGNED_FILES_DELIMITER)

        interestingrows = [row for idx, row in enumerate(row_reader) if idx == 28]
        # for row in row_reader:
        #
        #     print(row)
        #     #requests.post(URL, data=myobj)
        print(interestingrows)

if __name__ == "__main__":
    upload_users()
