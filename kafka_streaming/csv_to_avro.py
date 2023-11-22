import pandas as pd
import fastavro

import config


# Define Avro schema (must match CSV structure)
# This is a basic schema for demonstration
# You need to update your schema based on your csv
avro_schema = {
    "type": "record",
    "name": "Data",
    "fields": [
        {"name": "field1", "type": ["null", "string"]},
        {"name": "field2", "type": ["null", "int"]}
    ]
}


def csv_to_avro(csv_file_path, avro_file_path):
    # Use a context manager to open the Avro file
    with open(avro_file_path, 'wb') as out:
        # Define the CSV chunk size
        chunksize = 10 ** 6

        # Create a variable to signify the first chunk
        first_chunk = True

        for chunk in pd.read_csv(csv_file_path, chunksize=chunksize):
            # Convert the chusnk to dictionary format
            data_chunk = chunk.to_dict('records')

            if first_chunk:
                # Write the schema and first chunk of data
                fastavro.writer(out, avro_schema, data_chunk)
                first_chunk = False
            else:
                # Write subsequent chunks
                fastavro.writer(out, avro_schema, data_chunk, schemaless=True)


csv_to_avro(config.CSV_FILE_PATH, config.AVRO_FILE_PATH)
