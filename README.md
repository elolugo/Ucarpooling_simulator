# Orquestador Ucarpooling

Este es el repositorio para el simulador del sistema de carpooling con los datos de sapientia

## Para empezar

Estas instruccion te ayudaran a copiar el proyecto y correrlo en tu maquina local para desarrollo o pruebas de testing.

### Pre-requisitos

- `python 3.7+`

### Instalacion

Mejor si se trabajo con pip

`pip install -r requirements.txt`

## Guia de uso

primero incializar las bases de datos y poblarlas con datos de las personas

`python createdb.py`

## Estrucura del proyecto
```bash
│   .gitignore
│   alumni.sqlite3
│   createdb.py
│   helper.py
│   LICENSE.md
│   README.md
│   requirements.txt
│   settings.py
│   __init__.py
│
├───.idea
│   │   dataSources.local.xml
│   │   dataSources.xml
│   │   markdown-navigator-enh.xml
│   │   markdown-navigator.xml
│   │   misc.xml
│   │   modules.xml
│   │   sqldialects.xml
│   │   Ucarpooling_simulator.iml
│   │   vcs.xml
│   │   workspace.xml
│   │
│   ├───dataSources
│   │       c842a4ce-51f3-46ab-b6c3-a7e0bba80d9d.xml
│   │
│   └───inspectionProfiles
│           profiles_settings.xml
│
├───assign_personality
│   │   Workbook_form_data.twb
│   │   Workbook_sapientia_data.twb
│   │
│   ├───output_data
│   │       Alumnos_profiles_car_ownership.csv
│   │       Alumnos_profiles_eloquence.csv
│   │       Alumnos_profiles_itinerary.csv
│   │       Alumnos_profiles_music_taste.csv
│   │       Alumnos_profiles_smoker.csv
│   │
│   ├───scripts
│   │       check_integrity_file.py
│   │       distribute_cars.py
│   │       distribute_eloquence.py
│   │       distribute_itinerary.py
│   │       distribute_music.py
│   │       distribute_smoker.py
│   │
│   └───source_data
│           Form_data.csv
│           Sapientia_data.csv
│
├───orchestrator
│       uploader_user.py
│       uploader_user_itinerary.py
│
└───__pycache__
        helper.cpython-37.pyc
        settings.cpython-37.pyc
```


## Autor

- Alejandro Lugo
