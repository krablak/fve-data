from config_types import AppConfig


# Provides application config
# Default implementation using values in source code
def get_config():
    return AppConfig(
        inverter_ip='192.168.1.204',
        storage_ip='192.168.1.205',
        azrouter_ip='azrouter.local',
        azrouter_user='xxxxx',
        azrouter_pass='xxxxx'
    )
