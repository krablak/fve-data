import data_writer
import requests
import logging


def process(azrouter_ip: str, azrouter_user: str, azrouter_password: str, writer: data_writer.DataWriter):
    logging.info(f"Processing AZRouter ip:'{azrouter_ip}' user:'{azrouter_user}'")
    # Login to router
    login_resp = requests.post(f"http://{azrouter_ip}/api/v1/login", json={"data": {"username": azrouter_user, "password": azrouter_password}})
    if login_resp.status_code != 200:
        logging.error(f"Failed to login into AZRouter at {azrouter_ip} as '{azrouter_user}' with response: {login_resp.status_code}:{login_resp.text}")
        return
    # Get authorization token for next request
    auth_token = login_resp.text
    power_resp = requests.get(f"http://{azrouter_ip}/api/v1/power", headers={"Authorization": auth_token})
    if power_resp.status_code != 200:
        logging.error(f"Failed to get power data from AZRouter at {azrouter_ip} as '{azrouter_user}' with response: {power_resp.status_code}:{power_resp.text}")
        return
    power_data = power_resp.json()
    fields = {
        "power": power_data['input']['power'][0]['value'],
        "voltage": power_data['input']['voltage'][0]['value'],
        "current": power_data['input']['current'][0]['value']
    }
    writer.write(db="fve", measurement="azrouter00", fields=fields)
    logging.info(f"Processing AZRouter DONE")
