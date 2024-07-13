import os
import yaml
from dotenv import load_dotenv

class _Config:
    debug: bool
    ai_config: dict

    oxylabs_username: str
    oxylabs_password: str

    near_rpc_url: str
    near_account_id: str
    near_account_private_key: str

    def __init__(self):
        load_dotenv()

        self.debug = os.getenv("DEBUG", "False") == "True"

        ai_config_path = os.getenv("GENERAL_CONFIG_PATH", "config/general.yaml")
        with open(ai_config_path) as ai_config_file:
            self.ai_config = yaml.safe_load(ai_config_file)

        self.oxylabs_username = os.getenv("OXYLABS_USERNAME")
        self.oxylabs_password = os.getenv("OXYLABS_PASSWORD")

        self.near_rpc_url = os.getenv("NEAR_RPC_URL")
        self.near_account_id = os.getenv("NEAR_ACCOUNT_ID")
        self.near_account_private_key = os.getenv("NEAR_ACCOUNT_PRIVATE_KEY")

env = _Config()
