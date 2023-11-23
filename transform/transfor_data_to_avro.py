import csv
import pandas as pd
import fastavro
import config
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

avro_schema = {
    "type": "record",
    "name": "Data",
    "fields": [
        {"name": "gender", "type": ["null", "int"]},
        {"name": "state", "type": ["null", "int"]},
        {"name": "city_pop", "type": ["null", "int"]},
        {"name": "job", "type": ["null", "int"]},
        {"name": "profile", "type": ["null", "int"]},
        {"name": "trans_date", "type": ["null", "int"]},
        {"name": "unix_time", "type": ["null", "int"]},
        {"name": "category", "type": ["null", "int"]},
        {"name": "amt", "type": ["null", "int"]},
        {"name": "is_fraud", "type": ["null", "int"]},
        {"name": "merchant", "type": ["null", "int"]}
    ]
}

def csv_to_avro(raw_data_path, avro_file_path):
    encoding = 'utf-8-sig'  # Encoding Methode
    # Use a context manager to open the Avro file
    with open(avro_file_path, 'wb') as out, \
         open(raw_data_path, 'r', encoding=encoding) as csv_in:
        reader = csv.reader(csv_in, delimiter='|')

        # das kann man doch auch mit Spark machen und das gesamte File einlesen und dann in jedem Spark Node den Code ausführen

        for row in reader:
            # Convert the chunk to dictionary format
            data_chunk = row.to_dict('records')

            if first_chunk:
                # Write the schema and first chunk of data
                fastavro.writer(out, avro_schema, data_chunk)
                first_chunk = False
            else:
                # Write subsequent chunks
                data_chunk.map()
                fastavro.writer(out, avro_schema, data_chunk, schemaless=True)


# Event Handler für die Überwachung von Dateiänderungen
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            # Änderung an einem Verzeichnis
            return

        else:
            if event.src_path.lower().endswith('.csv'):
                print(f"Neue Datei erstellt: {event.src_path}")
                
                # Erzeuge einen eindeutigen Dateinamen für die Ausgabe
                output_file = os.path.join(config.OUTPUT_FOLDER, f"encoded_{time.time()}.avro")

                # Encode die CSV-Daten
                csv_to_avro(event.src_path, output_file)



# Funktion zur Überwachung des Folders
def watch_folder(input_folder_path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=input_folder_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

watch_folder(config.INPUT_FOLDER)