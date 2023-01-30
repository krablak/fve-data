import asyncio
import goodwe
import data_writer
import logging

async def get_runtime_data(inverter_ip: str):
    logging.info(f"Processing inverter at ip:'{inverter_ip}'")
    try:
        inverter = await goodwe.connect(inverter_ip)
        runtime_data = await inverter.read_runtime_data()
        result_data = {}
        for sensor in inverter.sensors():
            # Read all data from sensor
            if sensor.id_ in runtime_data:
                logging.info(f"{sensor.id_}: \t\t {sensor.name} = {runtime_data[sensor.id_]} {sensor.unit}")
                result_data[sensor.id_] = runtime_data[sensor.id_]
        logging.info(f"Processing inverter at ip:'{inverter_ip}' DONE")
        return result_data
    except OSError as e:
        if e.errno in (65, 64, 61):
            logging.warning("No connection to inverter %s" % inverter_ip)
            return None
        else:
            logging.error("Unexpected error occurred when connecting to inverter: %s" % e)
            raise e


def process(inverter_ip: str, writer: data_writer.DataWriter):
    # Read data from inverter sensors
    data = asyncio.run(get_runtime_data(inverter_ip=inverter_ip))
    if data is not None:
        writer.write(db="fve", measurement="inverter00", fields=data)
