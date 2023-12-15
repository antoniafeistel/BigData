import csv
import re
from config import config
import os
import hashlib
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Funktion zum Encoden der CSV-Daten
def encode_csv(input_path, output_path):
    encoding = 'utf-8-sig'  # Encoding Methode

    with open(input_path, 'r', encoding=encoding) as csv_in, \
         open(output_path, 'w', encoding=encoding, newline='') as csv_out:

        reader = csv.reader(csv_in, delimiter='|')
        writer = csv.writer(csv_out, delimiter='|')

        for source_row in reader:

            transformed_row = []
            indizies_of_relevant_columns = []

            
            # relevant_columns = ['gender', 'state', 'city_pop', 'job', 'profile', 'trans_date', 
            #                   'unix_time', 'category', 'amt', 'is_fraud', 'merchant' ]

            indizies_of_relevant_columns = [4, 7, 11, 12, 15, 17, 19, 20, 21, 22, 23]

            indizies_to_simple_encode = [0, 1, 3, 5, 7, 10]

            # kürzen der Liste, nur relevante Spalten verwenden
            for index in indizies_of_relevant_columns:
                    # Appenden der relevanten Spalten
                    transformed_row.append(source_row[index])

            if transformed_row[0] == 'gender':
                # Schreibe die Spaltendefinition in die Ausgabe-Datei
                writer.writerow(transformed_row)
            else:

                # Simple encoding
                for column_index_to_encode in indizies_to_simple_encode:
                    transformed_row[column_index_to_encode] = hash_int(transformed_row[column_index_to_encode])

                # encode profile
                transformed_row[4] = extract_number_from_string(transformed_row[4])

                # Schreibe die aktualisierte Zeile in die Ausgabedatei
                writer.writerow(transformed_row)

            

def extract_number_from_string(input_string):
    # Verwende einen regulären Ausdruck, um die Nummer aus dem String zu extrahieren
    match = re.search(r'\d+', input_string)
    
    # Überprüfe, ob eine Übereinstimmung gefunden wurde
    if match:
        return int(match.group())
    else:
        return 25

# Funktion zum Hashen von Strings für die Encodierung
def hash_int(input_string):
    # Hier wird ein einfacher MD5-Hash verwendet, du kannst auch andere Hash-Algorithmen verwenden
    hash_object = hashlib.md5(input_string.encode())
    hex_hash = hash_object.hexdigest()

    # Extrahiere die unteren 8 Bytes des Hexadezimal-Hash-Werts und interpretiere sie als Integer
    hash_int = int(hex_hash[-5:], 16)

    return hash_int

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
                output_file = os.path.join(config.OUTPUT_FOLDER, f"encoded_{time.time()}.csv")

                # Encode die CSV-Daten
                encode_csv(event.src_path, output_file)


# Funktion zur Überwachung des Folders
def watch_folder(input_folder_path):
    if not os.path.exists(input_folder_path):
        print(f"Das Verzeichnis existiert nicht")
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