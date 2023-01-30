# Defines structure and types of app configuration
class AppConfig:

    def __init__(self,
                 inverter_ip: str,
                 storage_ip: str,
                 azrouter_ip: str,
                 azrouter_user: str,
                 azrouter_pass: str,
                 ):
        self.inverter_ip = inverter_ip
        self.storage_ip = storage_ip
        self.azrouter_ip = azrouter_ip
        self.azrouter_user = azrouter_user
        self.azrouter_pass = azrouter_pass