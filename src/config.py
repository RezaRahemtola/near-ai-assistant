import os
from dotenv import load_dotenv

class _Config:
    debug: bool

    def __init__(self):
        load_dotenv()

        self.debug = os.getenv("DEBUG", "False") == "True"

env = _Config()
