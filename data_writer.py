import logging
from influxdb import InfluxDBClient


# Component responsible for writing data into storage
# Provides unified API for data writing
class DataWriter:

    def __init__(self, host='localhost', port=8086):
        logging.info('Initializing data writer for host: %s port: %s' % (host, port))
        self.host = host
        self.port = port
        self.client: InfluxDBClient = None

    def connect(self):
        logging.info('Connecting to %s:%s' % (self.host, self.port))
        self.client = InfluxDBClient(host=self.host, port=self.port)
        logging.info('Connected')
        logging.info('Listing databases: ')
        dbs = self.client.get_list_database()
        for cur_db in dbs:
            logging.info(cur_db)
        return self

    def write(self, db: str, measurement: str, fields: dict):
        self.client.switch_database(db)
        self.client.write_points(
            [
                {
                    "measurement": measurement,
                    "tags": {},
                    "fields": normalize_data(fields)
                }
            ]
        )


def normalize_data(data: dict):
    result = {}
    for key in data:
        if isinstance(data[key], (str, int, float)):
            result[key] = data[key]
        else:
            result[key] = str(data[key])
    return result
