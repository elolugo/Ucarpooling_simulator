"""
Helper functions that are used throughout all files on the project
"""

import datetime
from scripts import settings



def get_alumni_sapientia(row):

    alumni = {
        settings.FIELDNAME_UUID: row['UUID'],
        'SEXO': row['SEXO'],
        'CARRERA': row['CARRERA'],
        'DIRECCION': row['DIRECCION'],
        settings.FIELDNAME_LATITUDE: float(row['LATITUD']),
        settings.FIELDNAME_LONGITUDE: float(row['LONGITUD']),
    }

    return alumni

def get_alumni_form(row):

    alumni = {
        settings.FIELDNAME_UUID: str(row['UUID_FORM']),
        'CAREER': row['CAREER'],
        settings.FIELDNAME_TOA: datetime.datetime.strptime(row['TIME_OF_ARRIVAL'], '%H:%M:%S'),
        settings.FIELDNAME_TOD: datetime.datetime.strptime(row['TIME_OF_DEPARTURE'], '%H:%M:%S'),
        'SEX': row['SEX'],
        'SMOKER': row['SMOKER'],
        'ELOQUENCE_LEVEL': row['ELOQUENCE_LEVEL'],
        'IMPORTANCE_SMOKER': row['IMPORTANCE_SMOKER'],
        'IMPORTANCE_ELOQUENCE': row['IMPORTANCE_ELOQUENCE'],
        'IMPORTANCE_MUSIC': row['IMPORTANCE_MUSIC'],
        'IMPORTANCE_SEX': row['IMPORTANCE_SEX'],
        settings.FIELDNAME_TRANSPORT: row['TRANSPORT'],
        'MUSIC': row['MUSIC'],
        'CARPOOL': row['CARPOOL']
    }

    return alumni
