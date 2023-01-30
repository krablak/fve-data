import config
import process_sensors
import process_azrouter
import data_writer
import logging

logging.basicConfig(filename='logs/app.log', level=logging.DEBUG, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    logging.info("Running data gathering round")
    # Read configuration
    cfg = config.get_config()

    # Prepare writer
    writer = data_writer.DataWriter(host=cfg.storage_ip).connect()

    # Get and write FVE inverter data - production
    try:
        process_sensors.process(inverter_ip=cfg.inverter_ip, writer=writer)
    except:
        logging.exception('Failed to read and process inverter data.')

    # Get and write AZ Router data - consumption
    try:
        process_azrouter.process(azrouter_ip=cfg.azrouter_ip, azrouter_user=cfg.azrouter_user, azrouter_password=cfg.azrouter_pass, writer=writer)
    except:
        logging.exception('Failed to read and process AZ Router data.')

    logging.info("Data gathering round completed.")
