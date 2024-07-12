import os
import yaml
from dotenv import load_dotenv

class _Config:
    debug: bool
    ai_config: dict

    def __init__(self):
        load_dotenv()

        self.debug = os.getenv("DEBUG", "False") == "True"

        ai_config_path = os.getenv("GENERAL_CONFIG_PATH", "config/general.yaml")
        with open(ai_config_path) as ai_config_file:
            self.ai_config = yaml.safe_load(ai_config_file)

env = _Config()
